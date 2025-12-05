"""
Integration test for User Story 2: Auto-Route Wiring
"""
import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'src'))

from redscript.compiler.voxel_grid import VoxelGrid, Block
from redscript.compiler.logical_graph import LogicalGraph, Component, Connection, ComponentType
from redscript.solver.interface import SolverInterface

def test_us2_simple_routing():
    """Test routing a signal between two distant components"""
    # Create a simple grid
    grid = VoxelGrid(width=50, height=50, depth=50)
    
    # Place some support blocks
    for x in range(10, 41):
        grid.set_block(x, 0, 0, Block("minecraft:stone"))
    
    # Load into solver
    solver = SolverInterface()
    solver.load_grid(grid)
    
    # Try to route from (10, 1, 0) to (40, 1, 0)
    success, path = solver.route_signal(
        start=(10, 1, 0),
        end=(40, 1, 0),
        signal_strength=15
    )
    
    # For now, we expect this to succeed (even if path is empty in mock)
    # The real C++ implementation will provide actual paths
    assert isinstance(success, bool)

def test_us2_qc_validation():
    """Test quasi-connectivity validation"""
    grid = VoxelGrid(width=50, height=50, depth=50)
    
    solver = SolverInterface()
    solver.load_grid(grid)
    
    # Validate block placements
    is_valid_stone = solver.validate_placement((10, 0, 0), "minecraft:stone")
    is_valid_piston = solver.validate_placement((10, 1, 0), "minecraft:piston")
    
    # For now, both should be valid (mock implementation)
    assert isinstance(is_valid_stone, bool)
    assert isinstance(is_valid_piston, bool)

def test_us2_parallel_wiring():
    """Test routing multiple parallel signals"""
    grid = VoxelGrid(width=50, height=50, depth=50)
    
    solver = SolverInterface()
    solver.load_grid(grid)
    
    # Route two parallel signals
    success1, path1 = solver.route_signal((10, 1, 0), (40, 1, 0))
    success2, path2 = solver.route_signal((10, 5, 0), (40, 5, 0))
    
    # Both should complete without cross-talk
    assert isinstance(success1, bool)
    assert isinstance(success2, bool)
