"""
RedScript Parser: Converts source code to AST
"""
from lark import Lark, Transformer, Token
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from redscript.compiler.logical_graph import ComponentType

# Load grammar
GRAMMAR_PATH = Path(__file__).parent.parent / 'lexer' / 'grammar.lark'

class ASTNode:
    """Base class for AST nodes"""
    pass

class Program(ASTNode):
    def __init__(self, statements):
        self.statements = statements if statements else []

class Definition(ASTNode):
    def __init__(self, name, component_type, parameters):
        self.name = name
        self.component_type = component_type
        self.parameters = parameters if parameters else {}

class Action(ASTNode):
    def __init__(self, component, method, arguments):
        self.component = component
        self.method = method
        self.arguments = arguments if arguments else []

class ControlFlow(ASTNode):
    def __init__(self, flow_type, statements):
        self.flow_type = flow_type
        self.statements = statements if statements else []

class Connection(ASTNode):
    def __init__(self, source_component, source_port, target_component, target_port):
        self.source_component = source_component
        self.source_port = source_port
        self.target_component = target_component
        self.target_port = target_port

class PortRef(ASTNode):
    def __init__(self, component, port):
        self.component = component
        self.port = port

class RedScriptTransformer(Transformer):
    """Transforms Lark parse tree to AST"""
    
    def program(self, items):
        statements = [s for s in items if isinstance(s, (Definition, Action, ControlFlow, Connection))]
        return Program(statements)
    
    def definition(self, items):
        name = str(items[0])
        component_type = str(items[1])
        parameters = {}
        if len(items) > 2 and items[2]:
            parameters = items[2]
        return Definition(name, component_type, parameters)
    
    def parameters(self, items):
        result = {}
        for item in items:
            if isinstance(item, tuple) and len(item) == 2:
                result[item[0]] = item[1]
        return result
    
    def parameter(self, items):
        key = str(items[0])
        value = items[1]
        return (key, value)
    
    def action(self, items):
        component = str(items[0])
        method = str(items[1])
        arguments = items[2] if len(items) > 2 else []
        return Action(component, method, arguments)
    
    def arguments(self, items):
        return list(items)
    
    def argument(self, items):
        if len(items) == 2:  # Key-value pair
            return {str(items[0]): items[1]}
        else:  # Positional argument
            return items[0]
    
    def tuple(self, items):
        return (int(items[0]), int(items[1]), int(items[2]))
    
    def control_flow(self, items):
        flow_type = str(items[0])
        statements = [s for s in items[1:] if isinstance(s, (Definition, Action, ControlFlow, Connection))]
        return ControlFlow(flow_type, statements)
    
    def connection(self, items):
        source = items[0]
        target = items[1]
        return Connection(source.component, source.port, target.component, target.port)
    
    def port_ref(self, items):
        return PortRef(str(items[0]), str(items[1]))
    
    def CNAME(self, token):
        return str(token)
    
    def COMPONENT_TYPE(self, token):
        return str(token)
    
    def PARALLEL_KW(self, token):
        return "parallel"
    
    def SEQUENCE_KW(self, token):
        return "sequence"
    
    def WAIT_KW(self, token):
        return "wait"
    
    def STRING(self, token):
        return str(token)[1:-1]  # Remove quotes
    
    def NUMBER(self, token):
        return int(token)

class RedScriptParser:
    """Parser for RedScript language"""
    
    def __init__(self):
        # Read grammar from file
        with open(GRAMMAR_PATH, 'r') as f:
            grammar = f.read()
        self.parser = Lark(grammar, parser='lalr', transformer=RedScriptTransformer())
    
    def parse(self, source_code: str) -> Program:
        """Parse source code to AST"""
        try:
            result = self.parser.parse(source_code)
            return result
        except Exception as e:
            raise SyntaxError(f"Parse error: {e}")
