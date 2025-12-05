"""
Unit tests for extended parser features
"""
import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'src'))

from redscript.compiler.parser.parser import RedScriptParser, Definition
from redscript.compiler.sequencer.sequencer import KinematicSequencer
from redscript.compiler.logical_graph import ComponentType

class TestExtendedParser:
    """Test parsing of new component types"""
    
    def setup_method(self):
        self.parser = RedScriptParser()
        self.sequencer = KinematicSequencer()

    def test_parse_comparator(self):
        """Test parsing Comparator definition"""
        code = 'comp = Comparator(mode: "subtract")'
        ast = self.parser.parse(code)
        graph = self.sequencer.transform(ast)
        
        assert len(graph.components) == 1
        comp = list(graph.components.values())[0]
        assert comp.type == ComponentType.COMPARATOR
        assert comp.properties['mode'] == 'subtract'

    def test_parse_slime_block(self):
        """Test parsing SlimeBlock definition"""
        code = 'slime = SlimeBlock()'
        ast = self.parser.parse(code)
        graph = self.sequencer.transform(ast)
        
        assert len(graph.components) == 1
        comp = list(graph.components.values())[0]
        assert comp.type == ComponentType.SLIME_BLOCK

    def test_parse_target_block(self):
        """Test parsing Target definition"""
        code = 'target = Target()'
        ast = self.parser.parse(code)
        graph = self.sequencer.transform(ast)
        
        assert len(graph.components) == 1
        comp = list(graph.components.values())[0]
        assert comp.type == ComponentType.TARGET

    def test_parse_redstone_torch(self):
        """Test parsing RedstoneTorch definition"""
        code = 'torch = RedstoneTorch(facing: up)'
        ast = self.parser.parse(code)
        graph = self.sequencer.transform(ast)
        
        assert len(graph.components) == 1
        comp = list(graph.components.values())[0]
        assert comp.type == ComponentType.REDSTONE_TORCH
        assert comp.properties['facing'] == 'up'

    def test_parse_pressure_plate(self):
        """Test parsing PressurePlate definition"""
        code = 'plate = PressurePlate(type: "heavy")'
        ast = self.parser.parse(code)
        graph = self.sequencer.transform(ast)
        
        assert len(graph.components) == 1
        comp = list(graph.components.values())[0]
        assert comp.type == ComponentType.PRESSURE_PLATE
        assert comp.properties['type'] == 'heavy'

    def test_parse_button(self):
        """Test parsing Button definition"""
        code = 'btn = Button(type: "stone", face: "wall")'
        ast = self.parser.parse(code)
        graph = self.sequencer.transform(ast)
        
        assert len(graph.components) == 1
        comp = list(graph.components.values())[0]
        assert comp.type == ComponentType.BUTTON
        assert comp.properties['type'] == 'stone'
        assert comp.properties['face'] == 'wall'
