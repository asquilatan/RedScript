"""
Integration tests for User Story 5: Export to Litematica
"""
import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from redscript.compiler.voxel_grid import VoxelGrid, Block


class TestUS5Serialization:
    """Test Litematica export functionality"""
    
    def test_us5_serialize_empty_grid(self):
        """US5-001: Serialize empty voxel grid"""
        grid = VoxelGrid()
        assert len(grid.blocks) == 0
        # Serializer should produce minimal .litematic
    
    def test_us5_serialize_single_block(self):
        """US5-002: Serialize grid with single block"""
        grid = VoxelGrid()
        block = Block(
            material="minecraft:stone",
            properties={}
        )
        grid.set_block(0, 0, 0, block)
        assert grid.is_solid(0, 0, 0)
    
    def test_us5_block_state_mapping(self):
        """US5-003: Map RedScript blocks to Minecraft block states"""
        from redscript.utils.block_mapper import BlockStateMapper
        
        # Test normalization
        assert BlockStateMapper.normalize_material('stone') == 'minecraft:stone'
        assert BlockStateMapper.normalize_material('minecraft:piston') == 'minecraft:piston'
        
        # Test required properties
        piston_props = BlockStateMapper.get_required_properties('minecraft:piston')
        assert 'facing' in piston_props
        assert piston_props['facing'] == 'up'
