"""
Python wrapper for C++ Solver
"""
import sys
from pathlib import Path
from typing import List, Tuple, Optional

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

# Try to import C++ solver, fall back to Python implementation
CPP_AVAILABLE = False
try:
    from redscript.solver._solver import SpatialSolver as CppSolver, Vec3, PathRequest, PathResult
    CPP_AVAILABLE = True
except ImportError:
    pass

class Vec3:
    """3D vector for positions"""
    def __init__(self, x: int = 0, y: int = 0, z: int = 0):
        self.x = x
        self.y = y
        self.z = z
    
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z
    
    def __hash__(self):
        return hash((self.x, self.y, self.z))
    
    def __repr__(self):
        return f"Vec3({self.x}, {self.y}, {self.z})"


class PythonSolver:
    """Pure Python A* solver as fallback when C++ is not available"""
    
    def __init__(self):
        self.grid = {}  # (x,y,z) -> is_solid
        self.width = 64
        self.height = 64
        self.depth = 64
    
    def load_grid(self, grid_data: bytes, width: int, height: int, depth: int):
        """Load voxel grid from serialized data"""
        self.width = width
        self.height = height
        self.depth = depth
        self.grid = {}
        
        # Parse grid data (1 byte per voxel)
        for i, byte in enumerate(grid_data):
            if byte != 0:
                x = i // (height * depth)
                y = (i // depth) % height
                z = i % depth
                self.grid[(x, y, z)] = True
    
    def is_walkable(self, x: int, y: int, z: int) -> bool:
        """Check if position is walkable (air)"""
        if x < 0 or x >= self.width or y < 0 or y >= self.height or z < 0 or z >= self.depth:
            return False
        return (x, y, z) not in self.grid
    
    def find_path(self, start: Tuple[int, int, int], end: Tuple[int, int, int]) -> Tuple[bool, List[Tuple[int, int, int]]]:
        """A* pathfinding between two points"""
        import heapq
        
        def heuristic(a, b):
            return abs(a[0] - b[0]) + abs(a[1] - b[1]) + abs(a[2] - b[2])
        
        # Priority queue: (f_cost, g_cost, position)
        open_set = [(heuristic(start, end), 0, start)]
        came_from = {}
        g_scores = {start: 0}
        closed_set = set()
        
        # 6-directional neighbors
        directions = [(1,0,0), (-1,0,0), (0,1,0), (0,-1,0), (0,0,1), (0,0,-1)]
        
        while open_set:
            _, g, current = heapq.heappop(open_set)
            
            if current in closed_set:
                continue
            
            if current == end:
                # Reconstruct path
                path = [end]
                while current in came_from:
                    current = came_from[current]
                    path.append(current)
                path.reverse()
                return True, path
            
            closed_set.add(current)
            
            for dx, dy, dz in directions:
                neighbor = (current[0] + dx, current[1] + dy, current[2] + dz)
                
                if neighbor in closed_set:
                    continue
                
                if not self.is_walkable(*neighbor) and neighbor != end:
                    continue
                
                # Vertical movement costs more
                move_cost = 2 if dy != 0 else 1
                tentative_g = g + move_cost
                
                if neighbor not in g_scores or tentative_g < g_scores[neighbor]:
                    came_from[neighbor] = current
                    g_scores[neighbor] = tentative_g
                    f = tentative_g + heuristic(neighbor, end)
                    heapq.heappush(open_set, (f, tentative_g, neighbor))
        
        return False, []


class SolverInterface:
    """High-level interface to the Spatial Solver (C++ or Python fallback)"""
    
    def __init__(self):
        if CPP_AVAILABLE:
            self.solver = CppSolver()
            self.use_cpp = True
        else:
            self.solver = PythonSolver()
            self.use_cpp = False
        self._grid_loaded = False
    
    def load_grid(self, voxel_grid: 'VoxelGrid') -> None:
        """Load a voxel grid into the solver"""
        grid_data = voxel_grid.serialize()
        self.solver.load_grid(grid_data, voxel_grid.width, voxel_grid.height, voxel_grid.depth)
        self._grid_loaded = True
    
    def route_signal(self, start: Tuple[int, int, int], end: Tuple[int, int, int],
                    signal_strength: int = 15, delay: int = 0) -> Tuple[bool, List[Tuple[int, int, int]]]:
        """
        Route a redstone signal between two points.
        
        Returns:
            (success, path) where path is list of coordinates
        """
        if self.use_cpp:
            request = PathRequest()
            request.start = Vec3(start[0], start[1], start[2])
            request.end = Vec3(end[0], end[1], end[2])
            request.signal_strength = signal_strength
            request.min_delay = delay
            request.max_delay = delay
            
            result = self.solver.find_path(request)
            
            # Convert result path to tuples
            path_tuples = [(v.x, v.y, v.z) for v in result.path]
            
            return result.success, path_tuples
        else:
            # Use Python fallback
            return self.solver.find_path(start, end)
    
    def validate_placement(self, position: Tuple[int, int, int], block_type: str) -> bool:
        """Check if a block can be placed without violating constraints"""
        if self.use_cpp:
            pos = Vec3(position[0], position[1], position[2])
            return not self.solver.check_qc_violation(pos, block_type)
        else:
            # Python fallback - simple check
            return True
