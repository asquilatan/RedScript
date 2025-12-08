"""
Unit tests for parser
"""
import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'src'))

from redscript.compiler.parser.parser import RedScriptParser
from redscript.compiler.parser.parser import Program, Definition, Action

def test_parse_simple_definition():
    """Test parsing a simple component definition"""
    parser = RedScriptParser()
    code = 'piston = Piston()'
    ast = parser.parse(code)
    
    assert isinstance(ast, Program)
    assert len(ast.statements) == 1
    assert isinstance(ast.statements[0], Definition)
    assert ast.statements[0].name == 'piston'

def test_parse_definition_with_parameters():
    """Test parsing definition with parameters"""
    parser = RedScriptParser()
    code = 'door = Door(width=3, height=3)'
    ast = parser.parse(code)
    
    assert len(ast.statements) == 1
    defn = ast.statements[0]
    assert defn.name == 'door'
    assert 'width' in defn.parameters or 'height' in defn.parameters

def test_parse_action():
    """Test parsing an action"""
    parser = RedScriptParser()
    code = '''
door = Door()
door.open()
'''
    ast = parser.parse(code)
    
    assert len(ast.statements) >= 1

def test_parse_invalid_syntax():
    """Test that invalid syntax raises SyntaxError"""
    parser = RedScriptParser()
    code = 'invalid @#$ syntax!!!'
    
    with pytest.raises(SyntaxError):
        parser.parse(code)
