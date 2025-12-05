"""
Integration tests for Logic Components (Repeater, Comparator, Torch)
"""
import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'src'))

from redscript.compiler.compiler import Compiler
from redscript.compiler.voxel_grid import VoxelGrid

class TestLogicComponents:
    """Test compilation of logic components"""
    
    def setup_method(self):
        self.compiler = Compiler()

    def test_compile_repeater(self):
        """Test compiling a Repeater with delay"""
        code = """
        rep = Repeater(delay: 3)
        """
        result = self.compiler.compile(code)
        assert result.success
        
        # Find the repeater block
        repeater_found = False
        for block in result.schematic.voxel_grid.blocks.values():
            if block.material == 'minecraft:repeater':
                repeater_found = True
                assert block.properties['delay'] == '3'
                break
        assert repeater_found

    def test_compile_comparator(self):
        """Test compiling a Comparator with mode"""
        code = """
        comp = Comparator(mode: "subtract")
        """
        result = self.compiler.compile(code)
        assert result.success
        
        # Find the comparator block
        comp_found = False
        for block in result.schematic.voxel_grid.blocks.values():
            if block.material == 'minecraft:comparator':
                comp_found = True
                assert block.properties['mode'] == 'subtract'
                break
        assert comp_found

    def test_compile_torch(self):
        """Test compiling a Redstone Torch"""
        code = """
        torch = RedstoneTorch()
        """
        result = self.compiler.compile(code)
        assert result.success
        
        # Find the torch block
        torch_found = False
        for block in result.schematic.voxel_grid.blocks.values():
            if block.material == 'minecraft:redstone_torch':
                torch_found = True
                break
        assert torch_found
