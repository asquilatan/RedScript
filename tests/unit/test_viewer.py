"""
Test Viewer Logic
"""
import pytest
from unittest.mock import MagicMock, patch
from redscript.viewer.app import VoxelViewer, launch_viewer
from redscript.compiler.voxel_grid import VoxelGrid, Block

def test_viewer_initialization():
    """Test that viewer initializes correctly"""
    with patch('redscript.viewer.app.Ursina') as mock_ursina, \
         patch('redscript.viewer.app.window') as mock_window:
        viewer = VoxelViewer()
        assert viewer.app is not None
        mock_ursina.assert_called_once()

def test_load_grid():
    """Test loading a grid into the viewer"""
    with patch('redscript.viewer.app.Ursina'), \
         patch('redscript.viewer.app.window'):
        viewer = VoxelViewer()
        
        grid = VoxelGrid()
        grid.set_block(0, 0, 0, Block('minecraft:stone'))
        
        with patch('redscript.viewer.renderer.Entity') as mock_entity:
            viewer.load_grid(grid)
            assert len(viewer.voxel_entities) == 1
            mock_entity.assert_called()

def test_launch_viewer_rs():
    """Test launch_viewer with .rs file"""
    with patch('redscript.viewer.app.VoxelViewer') as MockViewer:
        with patch('redscript.compiler.compiler.compile_file') as mock_compile:
            mock_result = MagicMock()
            mock_result.grid = VoxelGrid()
            mock_compile.return_value = mock_result
            
            launch_viewer("test.rs")
            
            mock_compile.assert_called_with("test.rs", None)
            MockViewer.return_value.load_grid.assert_called()
            MockViewer.return_value.run.assert_called()

