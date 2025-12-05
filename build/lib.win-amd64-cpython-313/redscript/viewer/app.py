"""
Live Voxel Viewer: 3D visualization of compiled schematics
"""
import sys
from pathlib import Path
from typing import Optional

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

try:
    from ursina import Ursina, camera, held_keys, Vec3 as UrsVec3
    from ursina.prefabs.first_person_controller import FirstPersonController
    URSINA_AVAILABLE = True
except ImportError:
    URSINA_AVAILABLE = False

class VoxelViewer:
    """3D viewer for voxel grids using Ursina"""
    
    def __init__(self, width: int = 1280, height: int = 720):
        if not URSINA_AVAILABLE:
            raise ImportError("Ursina not installed. Install with: pip install ursina")
        
        self.app = Ursina(title="RedScript Voxel Viewer", size=(width, height))
        self.camera_speed = 20
        self.viewer_active = False
        self.voxel_entities = []
    
    def load_grid(self, voxel_grid: 'VoxelGrid') -> None:
        """Load a voxel grid for visualization"""
        self.clear()
        
        # Create visual entities for each block
        block_colors = {
            'minecraft:stone': (0.5, 0.5, 0.5),
            'minecraft:piston': (0.8, 0.8, 0),
            'minecraft:sticky_piston': (1, 0.4, 0),
            'minecraft:redstone_wire': (1, 0, 0),
            'minecraft:repeater': (1, 0.5, 0),
            'minecraft:glass': (0.8, 0.8, 1),
            'minecraft:air': None,  # Don't render air
        }
        
        for (x, y, z), block in voxel_grid.blocks.items():
            if block.material not in block_colors:
                continue
            
            color = block_colors[block.material]
            if color is None:
                continue
            
            # TODO: Create Ursina entity for block
            # For now, just count blocks
            self.voxel_entities.append((x, y, z, block.material))
    
    def clear(self) -> None:
        """Clear all rendered blocks"""
        # TODO: Destroy all Ursina entities
        self.voxel_entities = []
    
    def run(self) -> None:
        """Start the viewer"""
        self.viewer_active = True
        # TODO: Add camera controls
        # self.app.run()
    
    def close(self) -> None:
        """Close the viewer"""
        self.viewer_active = False
        # TODO: Destroy app

def launch_viewer(schematic_path: str) -> None:
    """CLI helper to launch viewer with a schematic"""
    from redscript.compiler.voxel_grid import VoxelGrid
    
    # TODO: Load schematic from file
    grid = VoxelGrid()
    
    viewer = VoxelViewer()
    viewer.load_grid(grid)
    viewer.run()
