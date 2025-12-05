"""
Kinematic Sequencer: Transforms AST to Logical Graph
"""
from typing import Dict, List
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from redscript.compiler.logical_graph import (
    LogicalGraph, Component, Connection, ComponentType, Port, SignalType
)
from redscript.compiler.parser.parser import (
    Program, Definition, Action, ControlFlow, ASTNode, Connection as ASTConnection
)

class KinematicSequencer:
    """Transforms parsed AST into a logical graph of components"""
    
    def __init__(self):
        self.graph = LogicalGraph()
        self.component_map: Dict[str, str] = {}  # name -> component_id
    
    def transform(self, ast: Program) -> LogicalGraph:
        """Transform AST to LogicalGraph"""
        for statement in ast.statements:
            self._process_statement(statement)
        
        return self.graph
    
    def _process_statement(self, statement: ASTNode) -> None:
        """Process a single statement"""
        if isinstance(statement, Definition):
            self._process_definition(statement)
        elif isinstance(statement, Action):
            self._process_action(statement)
        elif isinstance(statement, ControlFlow):
            self._process_control_flow(statement)
        elif isinstance(statement, ASTConnection):
            self._process_connection(statement)
    
    def _process_definition(self, defn: Definition) -> None:
        """Process a component definition"""
        component_type = self._get_component_type(defn.component_type)
        
        component = Component(
            type=component_type,
            properties=defn.parameters
        )
        
        component_id = self.graph.add_component(component)
        self.component_map[defn.name] = component_id
    
    def _process_action(self, action: Action) -> None:
        """Process an action (method call on component)"""
        component_id = self.component_map.get(action.component)
        if not component_id:
            raise ValueError(f"Component '{action.component}' not defined")
        
        # Actions can modify properties or create internal connections
        # For now, just log the action
        # TODO: Implement action semantics (extend, retract, etc.)
    
    def _process_connection(self, conn: ASTConnection) -> None:
        """Process a signal connection (source -> target)"""
        source_comp_id = self.component_map.get(conn.source_component)
        target_comp_id = self.component_map.get(conn.target_component)
        
        if not source_comp_id:
            raise ValueError(f"Source component '{conn.source_component}' not defined")
        if not target_comp_id:
            raise ValueError(f"Target component '{conn.target_component}' not defined")
        
        # Get components
        source_comp = self.graph.components[source_comp_id]
        target_comp = self.graph.components[target_comp_id]
        
        # Get or create ports
        source_port = self._get_or_create_port(source_comp, conn.source_port, is_output=True)
        target_port = self._get_or_create_port(target_comp, conn.target_port, is_output=False)
        
        # Create connection
        connection = Connection(
            source_port_id=source_port.id,
            target_port_id=target_port.id,
            signal_strength=15,
            min_delay=0
        )
        self.graph.add_connection(connection)
    
    def _get_or_create_port(self, component: Component, port_name: str, is_output: bool) -> Port:
        """Get an existing port or create a new one"""
        ports = component.outputs if is_output else component.inputs
        
        # Check existing ports
        for port in ports:
            if port.name == port_name:
                return port
        
        # Create new port
        port = Port(
            name=port_name,
            signal_type=SignalType.REDSTONE,
            strength=15
        )
        
        if is_output:
            component.outputs.append(port)
        else:
            component.inputs.append(port)
        
        return port
    
    def _process_control_flow(self, flow: ControlFlow) -> None:
        """Process control flow (parallel, sequence)"""
        for statement in flow.statements:
            self._process_statement(statement)
    
    def _get_component_type(self, type_str: str) -> ComponentType:
        """Map string to ComponentType"""
        type_map = {
            'Piston': ComponentType.PISTON,
            'StickyPiston': ComponentType.STICKY_PISTON,
            'Repeater': ComponentType.REPEATER,
            'Lever': ComponentType.LEVER,
            'Lamp': ComponentType.LAMP,
            'Observer': ComponentType.OBSERVER,
            'Dropper': ComponentType.DROPPER,
            'Door': ComponentType.PISTON,  # 3x3 door uses pistons
            'Comparator': ComponentType.COMPARATOR,
            'Hopper': ComponentType.HOPPER,
            'Target': ComponentType.TARGET,
            'SlimeBlock': ComponentType.SLIME_BLOCK,
            'HoneyBlock': ComponentType.HONEY_BLOCK,
            'RedstoneTorch': ComponentType.REDSTONE_TORCH,
            'PressurePlate': ComponentType.PRESSURE_PLATE,
            'Button': ComponentType.BUTTON,
        }
        return type_map.get(type_str, ComponentType.PISTON)
        return type_map.get(type_str, ComponentType.PISTON)
