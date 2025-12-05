"""
Live Voxel Viewer: 3D visualization of compiled schematics
"""
import sys
from pathlib import Path
from typing import Optional

# Ensure src is in path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

try:
    from ursina import Ursina, camera, held_keys, Vec3 as UrsVec3, window, color, Text
    from ursina.prefabs.first_person_controller import FirstPersonController
    URSINA_AVAILABLE = True
except ImportError:
    URSINA_AVAILABLE = False

from redscript.compiler.voxel_grid import VoxelGrid
from redscript.viewer.renderer import VoxelRenderer
from redscript.viewer.controls import SpectatorController

class VoxelViewer:
    """3D viewer for voxel grids using Ursina"""
    
    def __init__(self, width: int = 1280, height: int = 720):
        if not URSINA_AVAILABLE:
            raise ImportError("Ursina not installed. Install with: pip install ursina")
        
        self.app = Ursina(title="RedScript Voxel Viewer", size=(width, height))
        window.color = color.rgb(135, 206, 235)  # Sky blue background
        
        self.voxel_entities = []
        self.controls = None
        self.border_entity = None
        
        # UI Info text (black text on light background)
        self.info_text = Text(
            text="Controls: WASD Move | Space/Shift Up/Down | Mouse Look | Scroll Speed | ESC Unlock",
            position=(-0.85, 0.45),
            scale=1,
            color=color.black
        )
        
        # Position and Look-at Info
        self.pos_text = Text(
            text="Pos: (0, 0, 0)",
            position=(-0.85, -0.40),
            scale=1,
            color=color.black
        )
        self.look_text = Text(
            text="Looking at: None",
            position=(-0.85, -0.45),
            scale=1,
            color=color.black
        )
    
    def load_grid(self, voxel_grid: VoxelGrid) -> None:
        """Load a voxel grid for visualization"""
        # Clear existing entities
        for e in self.voxel_entities:
            if e:
                try:
                    e.disable()
                except:
                    pass
        self.voxel_entities = []
        
        if self.border_entity:
            try:
                self.border_entity.disable()
            except:
                pass
        
        # Calculate bounds
        if voxel_grid.blocks:
            xs = [x for x, _, _ in voxel_grid.blocks.keys()]
            ys = [y for _, y, _ in voxel_grid.blocks.keys()]
            zs = [z for _, _, z in voxel_grid.blocks.keys()]
            
            min_x, max_x = min(xs), max(xs)
            min_y, max_y = min(ys), max(ys)
            min_z, max_z = min(zs), max(zs)
            
            center = (
                (min_x + max_x) / 2,
                (min_y + max_y) / 2,
                (min_z + max_z) / 2
            )
            
            size = (
                max_x - min_x + 1,
                max_y - min_y + 1,
                max_z - min_z + 1
            )
        else:
            center = (0, 0, 0)
            size = (1, 1, 1)

        # Create a parent entity to hold the grid and center it
        from ursina import Entity, Vec3
        self.grid_parent = Entity()
        
        # Render new grid attached to parent
        self.voxel_entities = VoxelRenderer.render_grid(voxel_grid, parent_entity=self.grid_parent)
        
        # Create border
        self.border_entity = Entity(
            parent=self.grid_parent,
            model='wireframe_cube',
            position=center,
            scale=size,
            color=color.cyan
        )
        
        # Shift the parent so the grid center is at (0,0,0)
        self.grid_parent.position = -Vec3(*center)
            
        # Setup controls to look at origin (0,0,0)
        if self.controls is None:
            self.controls = SpectatorController(
                pos_text=self.pos_text,
                look_text=self.look_text
            )
            
        # Camera looks at (0,0,0)
        self.controls.setup_for_grid((0, 0, 0))

    def run(self):
        """Run the viewer application"""
        self.app.run()

def launch_viewer(file_path: str):
    """Launch the viewer for a given file"""
    path = Path(file_path)
    
    if path.suffix == '.rs':
        print(f"Compiling {path} for viewing...")
        from redscript.compiler.compiler import compile_file
        # Compile to memory (no output file needed if we just want the grid)
        result = compile_file(str(path), None)
        if not result.success:
            raise RuntimeError(f"Compilation failed: {result.errors}")
        grid = result.schematic.voxel_grid
    elif path.suffix == '.litematic':
        raise NotImplementedError("Viewing .litematic files is not yet supported. Please provide a .rs file.")
    else:
        raise ValueError(f"Unsupported file format: {path.suffix}")
        
    viewer = VoxelViewer()
    viewer.load_grid(grid)
    viewer.run()
