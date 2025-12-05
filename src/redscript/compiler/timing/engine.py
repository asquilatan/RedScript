"""
Timing Engine: Calculates and inserts repeaters for synchronization
"""
from typing import Dict, List, Tuple
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from redscript.compiler.logical_graph import LogicalGraph, Connection, Component, ComponentType

class TimingEngine:
    """Calculates signal propagation delays and inserts repeaters"""
    
    SIGNAL_PROPAGATION_DELAY = 1  # Redstone signal propagates 1 block per tick
    REPEATER_DELAY = 1  # 1 tick minimum per repeater
    REPEATER_MAX_DELAY = 4  # 4 ticks maximum per repeater
    
    def __init__(self):
        self.graph: LogicalGraph = None
    
    def get_component_delay(self, component: Component) -> int:
        """Get the signal delay introduced by a component in ticks"""
        if component.type == ComponentType.REPEATER:
            return int(component.properties.get('delay', 1))
        elif component.type == ComponentType.COMPARATOR:
            return 1
        elif component.type == ComponentType.REDSTONE_TORCH:
            return 1
        elif component.type == ComponentType.OBSERVER:
            return 1
        return 0

    def calculate_delays(self, graph: LogicalGraph) -> Dict[str, int]:
        """
        Calculate required delays for each connection.
        
        Returns:
            Dict mapping connection_id -> required_delay_ticks
        """
        delays = {}
        
        for conn_id, conn in graph.connections.items():
            # Calculate path length (simplified)
            # Real implementation would use actual path from routing
            path_length = 16  # Default assumption
            
            # Calculate propagation delay
            prop_delay = (path_length + self.SIGNAL_PROPAGATION_DELAY - 1) // self.SIGNAL_PROPAGATION_DELAY
            
            # Apply user-specified constraints
            required_delay = max(prop_delay, conn.min_delay)
            required_delay = min(required_delay, conn.max_delay)
            
            delays[conn_id] = required_delay
        
        return delays
    
    def insert_repeaters(self, graph: LogicalGraph, path_length: int, 
                        required_delay: int) -> List[Tuple[int, int, int]]:
        """
        Calculate repeater positions and delays needed for a path.
        
        Args:
            graph: Logical graph
            path_length: Number of blocks in the path
            required_delay: Target delay in ticks
        
        Returns:
            List of (x, y, z, delay) tuples for repeaters
        """
        repeater_positions = []
        
        # Calculate how many repeaters are needed
        min_repeaters = required_delay // self.REPEATER_MAX_DELAY
        remainder_delay = required_delay % self.REPEATER_MAX_DELAY
        
        # Distribute repeaters along the path
        repeater_spacing = path_length // (min_repeaters + 1) if min_repeaters > 0 else path_length
        
        for i in range(min_repeaters + 1):
            pos = i * repeater_spacing
            delay = self.REPEATER_MAX_DELAY if i < min_repeaters else remainder_delay
            if delay > 0:
                repeater_positions.append((pos, i, 0, delay))  # (position_in_path, repeater_index, reserved, delay)
        
        return repeater_positions
    
    def synchronize_parallel_actions(self, graph: LogicalGraph) -> Dict[str, int]:
        """
        Find parallel actions and synchronize their timing.
        Returns adjusted delays for each connection to ensure they fire in the same tick.
        """
        adjusted_delays = {}
        
        # Find groups of parallel connections
        # (Simplified: connections between same components)
        
        for conn_id, conn in graph.connections.items():
            # For each connection, ensure it's synchronized with others
            # This is a placeholder; real implementation would traverse the graph
            adjusted_delays[conn_id] = conn.min_delay
        
        return adjusted_delays
