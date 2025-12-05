#!/usr/bin/env python3
"""Debug script to understand EditorCamera behavior"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

try:
    from ursina import Ursina, Entity, camera, EditorCamera, color, Vec3, window
    
    app = Ursina()
    window.color = color.rgb(30, 30, 30)
    
    # Create some test cubes around position (10, 5, 10)
    test_positions = [
        (10, 5, 10),
        (11, 5, 10),
        (10, 5, 11),
        (11, 5, 11),
    ]
    
    for pos in test_positions:
        Entity(
            model='cube',
            color=color.orange,
            position=pos,
            scale=1.0,
        )
    
    # Setup EditorCamera
    ec = EditorCamera()
    
    # Set pivot to center of blocks
    center = Vec3(10.5, 5, 10.5)
    ec.position = center
    
    # Set initial rotation to look from above/behind
    ec.rotation = (30, -45, 0)
    
    print(f"Camera position: {camera.position}")
    print(f"Camera world_position: {camera.world_position}")
    print(f"EditorCamera position: {ec.position}")
    
    app.run()
    
except ImportError as e:
    print(f"Import error: {e}")
