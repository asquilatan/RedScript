"""
Test Python-C++ bindings
"""
import pytest

def test_vec3_creation():
    """Test Vec3 creation from Python"""
    try:
        from redscript.solver._solver import Vec3
        v = Vec3(1, 2, 3)
        assert v.x == 1
        assert v.y == 2
        assert v.z == 3
    except ImportError:
        pytest.skip("C++ extensions not built yet")

def test_path_request_creation():
    """Test PathRequest structure"""
    try:
        from redscript.solver._solver import PathRequest, Vec3
        req = PathRequest()
        req.start = Vec3(0, 0, 0)
        req.end = Vec3(10, 10, 10)
        req.signal_strength = 15
        assert req.start.x == 0
        assert req.end.x == 10
    except ImportError:
        pytest.skip("C++ extensions not built yet")

def test_solver_creation():
    """Test SpatialSolver creation"""
    try:
        from redscript.solver._solver import SpatialSolver
        solver = SpatialSolver()
        assert solver is not None
    except ImportError:
        pytest.skip("C++ extensions not built yet")
