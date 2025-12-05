#!/usr/bin/env python3
"""
Demo script: Compile a 2x2 piston door
"""
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from redscript.compiler.compiler import Compiler, CompileOptions

# Read the example file
with open("examples/2x2_door.rs", "r") as f:
    source = f.read()

print("=== Source Code ===")
print(source)
print()

# Compile with verbose output
compiler = Compiler()
options = CompileOptions(verbose=True)
result = compiler.compile(source, options)

print()
print("=== Compilation Result ===")
print(f"Success: {result.success}")
print(f"Errors: {result.errors}")
print(f"Warnings: {result.warnings}")

if result.success and result.schematic:
    print(f"Block Count: {result.schematic.get_block_count()}")
    print()
    print("=== Placed Blocks ===")
    for (x, y, z), block in sorted(result.schematic.voxel_grid.blocks.items()):
        print(f"  ({x:2d}, {y:2d}, {z:2d}): {block.material} {block.properties}")
else:
    print("Compilation failed!")
    for err in result.errors:
        print(f"  ERROR: {err}")
