"""
Integration tests for User Story 1: Define Kinematic Intent
"""
import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'src'))

from redscript.compiler.parser.parser import RedScriptParser
from redscript.compiler.sequencer.sequencer import KinematicSequencer
from redscript.compiler.safety import KinematicSafety
from redscript.compiler.logical_graph import Component, ComponentType, LogicalGraph
from redscript.compiler.voxel_grid import VoxelGrid, Block

def test_us1_simple_piston():
    """Test compiling a simple piston script"""
    code = '''
piston = Piston()
piston.extend()
'''
    
    parser = RedScriptParser()
    ast = parser.parse(code)
    
    sequencer = KinematicSequencer()
    graph = sequencer.transform(ast)
    
    # Verify component was added
    assert len(graph.components) >= 1
    
    # Validate safety
    is_valid, errors = KinematicSafety.validate(graph)
    assert is_valid

def test_us1_door_script():
    """Test compiling a door script"""
    code = '''
door = Door()
door.open()
door.close()
'''
    
    parser = RedScriptParser()
    ast = parser.parse(code)
    
    sequencer = KinematicSequencer()
    graph = sequencer.transform(ast)
    
    # Door should create at least one component
    assert len(graph.components) >= 1
    
    # Validate safety
    is_valid, errors = KinematicSafety.validate(graph)
    assert is_valid, f"Safety check failed: {errors}"

def test_safety_check_piston_push_limit():
    """Test that safety check detects push limit violations"""
    # Create a grid with a piston that has too many blocks
    grid = VoxelGrid()
    graph = LogicalGraph()
    
    # Piston at (0,0,0) facing East
    grid.set_block(0, 0, 0, Block("minecraft:piston", {"facing": "east"}))
    
    # 13 Stone blocks in front (1,0,0) to (13,0,0)
    for x in range(1, 14):
        grid.set_block(x, 0, 0, Block("minecraft:stone"))
    
    is_valid, errors = KinematicSafety.validate_physical(grid, graph)
    assert not is_valid
    assert any('push limit' in error.lower() for error in errors)
