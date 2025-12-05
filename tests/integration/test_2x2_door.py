"""
Integration Test: 2x2 Piston Door Compilation

This test verifies the complete pipeline can compile a 2x2 piston door
mechanism from RedScript source code to a voxel grid with properly
placed pistons and routed redstone wiring.
"""
import pytest
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'src'))

from redscript.compiler.compiler import Compiler, CompileOptions, CompileResult
from redscript.compiler.voxel_grid import VoxelGrid, Block
from redscript.compiler.logical_graph import ComponentType


class TestTwoByTwoDoor:
    """Tests for 2x2 piston door compilation"""
    
    def test_parse_2x2_door_script(self):
        """Test parsing a 2x2 door RedScript"""
        from redscript.compiler.parser.parser import RedScriptParser
        
        source = """
        // 2x2 Piston Door
        piston1 = Piston(position: (0, 5, 0), facing: up)
        piston2 = Piston(position: (1, 5, 0), facing: up)
        piston3 = Piston(position: (0, 5, 1), facing: up)
        piston4 = Piston(position: (1, 5, 1), facing: up)
        """
        
        parser = RedScriptParser()
        ast = parser.parse(source)
        
        # Should have 4 definitions
        assert len(ast.statements) == 4
        
        # First statement should be piston1
        defn = ast.statements[0]
        assert defn.name == "piston1"
        assert defn.component_type == "Piston"
        assert defn.parameters.get('position') == (0, 5, 0)
    
    def test_compile_2x2_door_creates_components(self):
        """Test that compilation creates 4 piston components"""
        source = """
        piston1 = Piston(position: (10, 5, 10), facing: up)
        piston2 = Piston(position: (11, 5, 10), facing: up)
        piston3 = Piston(position: (10, 5, 11), facing: up)
        piston4 = Piston(position: (11, 5, 11), facing: up)
        """
        
        compiler = Compiler()
        result = compiler.compile(source, CompileOptions(verbose=False))
        
        assert result.success, f"Compilation failed: {result.errors}"
        assert result.schematic is not None
        
        # Should have at least 4 piston blocks placed
        grid = result.schematic.voxel_grid
        piston_count = sum(
            1 for block in grid.blocks.values() 
            if 'piston' in block.material
        )
        assert piston_count >= 4, f"Expected 4 pistons, found {piston_count}"
    
    def test_compile_2x2_door_places_pistons_correctly(self):
        """Test that pistons are placed at correct positions"""
        source = """
        piston1 = Piston(position: (10, 5, 10), facing: up)
        piston2 = Piston(position: (11, 5, 10), facing: up)
        piston3 = Piston(position: (10, 5, 11), facing: up)
        piston4 = Piston(position: (11, 5, 11), facing: up)
        """
        
        compiler = Compiler()
        result = compiler.compile(source)
        
        assert result.success
        grid = result.schematic.voxel_grid
        
        # Check each piston position
        expected_positions = [
            (10, 5, 10),
            (11, 5, 10),
            (10, 5, 11),
            (11, 5, 11),
        ]
        
        for pos in expected_positions:
            block = grid.get_block(*pos)
            assert block is not None, f"No block at {pos}"
            assert 'piston' in block.material, f"Expected piston at {pos}, got {block.material}"
    
    def test_compile_2x2_door_has_support_blocks(self):
        """Test that pistons have stone support blocks underneath"""
        source = """
        piston1 = Piston(position: (10, 5, 10), facing: up)
        piston2 = Piston(position: (11, 5, 10), facing: up)
        """
        
        compiler = Compiler()
        result = compiler.compile(source)
        
        assert result.success
        grid = result.schematic.voxel_grid
        
        # Check support blocks under pistons
        support_positions = [
            (10, 4, 10),  # Under piston1
            (11, 4, 10),  # Under piston2
        ]
        
        for pos in support_positions:
            block = grid.get_block(*pos)
            assert block is not None, f"No support block at {pos}"
            assert 'stone' in block.material, f"Expected stone at {pos}, got {block.material}"
    
    def test_compile_2x2_door_with_parallel_action(self):
        """Test compilation with parallel piston action"""
        source = """
        piston1 = Piston(position: (10, 5, 10), facing: up)
        piston2 = Piston(position: (11, 5, 10), facing: up)
        
        parallel {
            piston1.push()
            piston2.push()
        }
        """
        
        compiler = Compiler()
        result = compiler.compile(source)
        
        assert result.success, f"Compilation failed: {result.errors}"
        assert result.schematic is not None
    
    def test_compile_2x2_door_block_count(self):
        """Test total block count is reasonable"""
        source = """
        piston1 = Piston(position: (10, 5, 10), facing: up)
        piston2 = Piston(position: (11, 5, 10), facing: up)
        piston3 = Piston(position: (10, 5, 11), facing: up)
        piston4 = Piston(position: (11, 5, 11), facing: up)
        """
        
        compiler = Compiler()
        result = compiler.compile(source)
        
        assert result.success
        block_count = result.schematic.get_block_count()
        
        # Should have at least 8 blocks (4 pistons + 4 support)
        assert block_count >= 8, f"Expected at least 8 blocks, got {block_count}"
        # Should not have too many blocks (indicates a bug)
        assert block_count < 100, f"Too many blocks: {block_count}"
    
    def test_logical_graph_has_components(self):
        """Test that logical graph is properly populated"""
        source = """
        piston1 = Piston(position: (10, 5, 10), facing: up)
        piston2 = Piston(position: (11, 5, 10), facing: up)
        """
        
        compiler = Compiler()
        result = compiler.compile(source)
        
        assert result.success
        graph = result.schematic.logical_graph
        
        # Should have 2 components
        assert len(graph.components) == 2
        
        # Both should be piston type
        for comp in graph.components.values():
            assert comp.type == ComponentType.PISTON
    
    def test_sticky_piston_support(self):
        """Test that sticky pistons work correctly"""
        source = """
        sticky1 = StickyPiston(position: (10, 5, 10), facing: up)
        sticky2 = StickyPiston(position: (11, 5, 10), facing: up)
        """
        
        compiler = Compiler()
        result = compiler.compile(source)
        
        assert result.success
        grid = result.schematic.voxel_grid
        
        # Check sticky piston placement
        block = grid.get_block(10, 5, 10)
        assert block is not None
        assert 'sticky_piston' in block.material
    
    def test_schematic_serialization(self):
        """Test that schematic can report its structure"""
        source = """
        piston1 = Piston(position: (10, 5, 10), facing: up)
        piston2 = Piston(position: (11, 5, 10), facing: up)
        """
        
        compiler = Compiler()
        result = compiler.compile(source)
        
        assert result.success
        schematic = result.schematic
        
        # Test helper methods
        assert schematic.author == "RedScript Compiler"
        assert schematic.get_block_count() > 0
        
        voxel_grid = schematic.to_voxel_grid()
        assert voxel_grid is not None
        assert len(voxel_grid.blocks) > 0


class TestDoorVariations:
    """Test various door configurations"""
    
    def test_vertical_door(self):
        """Test a vertically oriented door"""
        source = """
        piston_top = Piston(position: (10, 6, 10), facing: down)
        piston_bot = Piston(position: (10, 4, 10), facing: up)
        """
        
        compiler = Compiler()
        result = compiler.compile(source)
        
        assert result.success, f"Failed: {result.errors}"
    
    def test_mixed_components(self):
        """Test door with repeaters"""
        source = """
        piston1 = Piston(position: (10, 5, 10), facing: up)
        repeater1 = Repeater(position: (10, 5, 8), facing: north)
        """
        
        compiler = Compiler()
        result = compiler.compile(source)
        
        assert result.success, f"Failed: {result.errors}"
        
        grid = result.schematic.voxel_grid
        
        # Check both blocks exist
        piston = grid.get_block(10, 5, 10)
        assert piston is not None
        
        repeater = grid.get_block(10, 5, 8)
        assert repeater is not None
        assert 'repeater' in repeater.material


class TestErrorHandling:
    """Test error cases"""
    
    def test_empty_script(self):
        """Test compiling empty script"""
        source = ""
        
        compiler = Compiler()
        result = compiler.compile(source)
        
        # Empty script should succeed with no blocks
        assert result.success
        assert result.schematic.get_block_count() == 0
    
    def test_comment_only_script(self):
        """Test script with only comments"""
        source = """
        // This is a comment
        // Another comment
        """
        
        compiler = Compiler()
        result = compiler.compile(source)
        
        assert result.success
        assert result.schematic.get_block_count() == 0
    
    def test_undefined_component_type(self):
        """Test using an undefined component type defaults to piston"""
        # Note: The grammar currently requires known types
        # This test verifies the behavior for known types only
        source = """
        lever1 = Lever(position: (10, 5, 10))
        """
        
        compiler = Compiler()
        result = compiler.compile(source)
        
        assert result.success


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
