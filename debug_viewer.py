#!/usr/bin/env python3
"""Debug script to test viewer rendering"""
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from redscript.compiler.compiler import compile_file

# Compile the file
result = compile_file("examples/2x2_door.rs", None)
print(f"Compilation success: {result.success}")

if result.success:
    grid = result.schematic.voxel_grid
    print(f"Number of blocks in grid: {len(grid.blocks)}")
    print("\nBlocks in grid:")
    for (x, y, z), block in grid.blocks.items():
        print(f"  ({x}, {y}, {z}): {block.material}")
    
    # Calculate center
    xs = [x for x, _, _ in grid.blocks.keys()]
    ys = [y for _, y, _ in grid.blocks.keys()]
    zs = [z for _, _, z in grid.blocks.keys()]
    center = (
        (min(xs) + max(xs)) / 2,
        (min(ys) + max(ys)) / 2,
        (min(zs) + max(zs)) / 2
    )
    print(f"\nGrid center: {center}")
    print(f"X range: {min(xs)} - {max(xs)}")
    print(f"Y range: {min(ys)} - {max(ys)}")
    print(f"Z range: {min(zs)} - {max(zs)}")
else:
    print(f"Errors: {result.errors}")
