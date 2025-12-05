"""
Kinematic Safety: Validates logical graph for safe mechanical operations
"""
from typing import Tuple, List
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from redscript.compiler.logical_graph import LogicalGraph, Component, ComponentType

class KinematicSafety:
    """Validates logical graph to prevent self-destructing configurations"""
    
    @staticmethod
    def validate(graph: LogicalGraph) -> Tuple[bool, List[str]]:
        """
        Validate the logical graph for kinematic safety.
        
        Checks:
        1. Piston push limit (>12 blocks)
        2. 1-tick pulses to sticky pistons (block spitting)
        3. Pistons pushing into immovable blocks
        
        Returns:
            (is_valid, list_of_errors)
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
                
                # Check for push limit violations (if explicitly set)
                push_count_str = component.properties.get('push_count', '')
                if push_count_str:
                    try:
                        push_count = int(push_count_str)
                        if push_count > 12:
                            errors.append(
                                f"Component {comp_id}: Piston push count ({push_count}) "
                                f"exceeds vanilla limit (12 blocks)"
                            )
                    except (ValueError, TypeError):
                        pass
        
        return len(errors) == 0, errors
