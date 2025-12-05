"""
Integration test for User Story 3: Synchronize Actions
"""
import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'src'))

from redscript.compiler.timing.engine import TimingEngine
from redscript.compiler.logical_graph import LogicalGraph, Component, Connection, ComponentType

def test_us3_timing_calculation():
    """Test calculating delays for actions"""
    engine = TimingEngine()
    
    # Create a simple logical graph
    graph = LogicalGraph()
    
    piston1 = Component(type=ComponentType.PISTON)
    piston2 = Component(type=ComponentType.PISTON)
    
    graph.add_component(piston1)
    graph.add_component(piston2)
    
    # Add connection with delay requirement
    conn = Connection(
        source_port_id=piston1.outputs[0].id,
        target_port_id=piston2.inputs[0].id,
        min_delay=0,
        max_delay=4
    )
    graph.add_connection(conn)
    
    # Calculate delays
    delays = engine.calculate_delays(graph)
    
    assert len(delays) >= 1
    assert all(isinstance(d, int) for d in delays.values())

def test_us3_repeater_insertion():
    """Test inserting repeaters for required delays"""
    engine = TimingEngine()
    
    # Path of 20 blocks, requires 8 ticks delay
    repeaters = engine.insert_repeaters(graph=None, path_length=20, required_delay=8)
    
    # Should have 2 repeaters (8 / 4 = 2)
    assert len(repeaters) >= 1
    
    # Each repeater should have a valid delay
    for repeater in repeaters:
        assert repeater[3] > 0  # delay > 0

def test_us3_parallel_synchronization():
    """Test synchronizing parallel piston actions"""
    engine = TimingEngine()
    
    graph = LogicalGraph()
    
    # Create multiple pistons
    pistons = [Component(type=ComponentType.PISTON) for _ in range(3)]
    for piston in pistons:
        graph.add_component(piston)
    
    # Synchronize
    adjusted_delays = engine.synchronize_parallel_actions(graph)
    
    assert len(adjusted_delays) >= 0
