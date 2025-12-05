"""
Test configuration and fixtures
"""
import pytest
import sys
from pathlib import Path

# Add src to path for imports
project_root = Path(__file__).parent.parent
src_path = project_root / 'src'
sys.path.insert(0, str(src_path))

@pytest.fixture
def test_data_dir():
    """Return the test data directory"""
    return Path(__file__).parent / 'data'

@pytest.fixture
def temp_schematic(tmp_path):
    """Create a temporary schematic directory"""
    return tmp_path / 'test_schematic'

@pytest.fixture
def sample_2x2_door_source():
    """Return sample RedScript for a 2x2 piston door"""
    return """
    // 2x2 Piston Door
    piston1 = Piston(position: (10, 5, 10), facing: up)
    piston2 = Piston(position: (11, 5, 10), facing: up)
    piston3 = Piston(position: (10, 5, 11), facing: up)
    piston4 = Piston(position: (11, 5, 11), facing: up)
    """

@pytest.fixture  
def compiler():
    """Return a configured compiler instance"""
    from redscript.compiler.compiler import Compiler
    return Compiler()
