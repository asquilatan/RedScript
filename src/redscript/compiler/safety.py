"""
Kinematic Safety: Validates logical graph for safe mechanical operations
"""
from typing import Tuple, List, Set
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from redscript.compiler.logical_graph import LogicalGraph, Component, ComponentType
from redscript.compiler.voxel_grid import VoxelGrid

class KinematicSafety:
    """Validates logical graph to prevent self-destructing configurations"""
    
    @staticmethod
    def validate(graph: LogicalGraph) -> Tuple[bool, List[str]]:
        """
        Validate the logical graph for kinematic safety (logical checks).
        """
        errors = []
        
        # Check piston configurations
        for comp_id, component in graph.components.items():
            if component.type in [ComponentType.PISTON, ComponentType.STICKY_PISTON]:
                # Check for problematic connections
                connections = graph.get_connections_for_component(comp_id)
                
                for conn in connections:
                    # Check for 1-tick pulses to sticky pistons
                    if component.type == ComponentType.STICKY_PISTON:
                        if conn.min_delay == 1 and conn.max_delay == 1:
                            errors.append(
                                f"Component {comp_id}: 1-tick pulse to sticky piston "
                                f"may cause block spitting (Connection {conn.id})"
                            )
        
        return len(errors) == 0, errors

    @staticmethod
    def validate_physical(grid: VoxelGrid, graph: LogicalGraph) -> Tuple[bool, List[str]]:
        """
        Validate physical constraints (push limits, immovable blocks).
        """
        errors = []
        
        # Iterate over grid blocks to find pistons
        for pos, block in grid.blocks.items():
            if block.material in ['minecraft:piston', 'minecraft:sticky_piston']:
                # Determine push direction
                facing = block.properties.get('facing', 'up')
                direction = KinematicSafety._get_direction_vector(facing)
                
                # Calculate pushed blocks
                pushed_count, immovable_hit = KinematicSafety._calculate_push_load(grid, pos, direction)
                
                if immovable_hit:
                    errors.append(f"Piston at {pos} pushing into immovable block")
                elif pushed_count > 12:
                    errors.append(f"Piston at {pos} exceeds push limit ({pushed_count} > 12)")
                    
        return len(errors) == 0, errors

    @staticmethod
    def _get_direction_vector(facing: str) -> Tuple[int, int, int]:
        dirs = {
            'north': (0, 0, -1), 'south': (0, 0, 1),
            'east': (1, 0, 0), 'west': (-1, 0, 0),
            'up': (0, 1, 0), 'down': (0, -1, 0)
        }
        return dirs.get(facing, (0, 1, 0))

    @staticmethod
    def _calculate_push_load(grid: VoxelGrid, piston_pos: Tuple[int, int, int], 
                           direction: Tuple[int, int, int]) -> Tuple[int, bool]:
        """
        Calculate how many blocks are being pushed.
        Returns (count, hit_immovable)
        """
        # Start with the block directly in front of the piston head
        start_pos = (
            piston_pos[0] + direction[0],
            piston_pos[1] + direction[1],
            piston_pos[2] + direction[2]
        )
        
        if start_pos not in grid.blocks:
            return 0, False
            
        # BFS/Recursive search for attached blocks
        pushed_blocks = set()
        queue = [start_pos]
        pushed_blocks.add(start_pos)
        
        while queue:
            current_pos = queue.pop(0)
            if current_pos not in grid.blocks:
                continue
                
            block = grid.blocks[current_pos]
            
            if block.material == 'minecraft:air':
                continue
                
            if KinematicSafety._is_immovable(block.material):
                return len(pushed_blocks), True
            
            # Check block in front (always pushed)
            next_pos = (
                current_pos[0] + direction[0],
                current_pos[1] + direction[1],
                current_pos[2] + direction[2]
            )
            if next_pos in grid.blocks and next_pos not in pushed_blocks:
                pushed_blocks.add(next_pos)
                queue.append(next_pos)
            
            # If slime/honey, check attached blocks
            if block.material in ['minecraft:slime_block', 'minecraft:honey_block']:
                # Check all 6 neighbors
                neighbors = [
                    (current_pos[0]+1, current_pos[1], current_pos[2]),
                    (current_pos[0]-1, current_pos[1], current_pos[2]),
                    (current_pos[0], current_pos[1]+1, current_pos[2]),
                    (current_pos[0], current_pos[1]-1, current_pos[2]),
                    (current_pos[0], current_pos[1], current_pos[2]+1),
                    (current_pos[0], current_pos[1], current_pos[2]-1)
                ]
                
                for neighbor in neighbors:
                    if neighbor in grid.blocks and neighbor not in pushed_blocks:
                        neighbor_block = grid.blocks[neighbor]
                        if neighbor_block.material == 'minecraft:air':
                            continue
                            
                        # Slime doesn't stick to Honey and vice versa
                        if block.material == 'minecraft:slime_block' and neighbor_block.material == 'minecraft:honey_block':
                            continue
                        if block.material == 'minecraft:honey_block' and neighbor_block.material == 'minecraft:slime_block':
                            continue
                            
                        # Glazed terracotta doesn't stick
                        if 'glazed_terracotta' in neighbor_block.material:
                            continue
                            
                        pushed_blocks.add(neighbor)
                        queue.append(neighbor)
            
            if len(pushed_blocks) > 12:
                return len(pushed_blocks), False
                
        return len(pushed_blocks), False

    @staticmethod
    def _is_immovable(material: str) -> bool:
        immovable = [
            'minecraft:obsidian', 'minecraft:bedrock', 
            'minecraft:barrier', 'minecraft:command_block',
            'minecraft:end_portal_frame', 'minecraft:spawner'
        ]
        return material in immovable
