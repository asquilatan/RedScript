# Redstone_HDL Development Guidelines

Auto-generated from all feature plans. Last updated: 2025-12-06

## Active Technologies
- Python 3.13 + Lark (Parsing), Ursina (Viewer/3D), Pytest (Testing) (main)
- File-based (.rs source, .litematic output) (main)

- Python 3.11+ + Lark, Ursina, Pybind11 (001-redscript-compiler)
- C++ (Pathfinding Extensions)

## Project Structure

```text
src/
├── redscript/
│   ├── compiler/
│   ├── solver/
│   ├── viewer/
│   └── cli/
└── cpp/
tests/
```

## Commands

pip install .; pytest; tox

## Code Style

Python: PEP 8, Type Hints
C++: Google Style Guide

## Recent Changes
- main: Added Python 3.13 + Lark (Parsing), Ursina (Viewer/3D), Pytest (Testing)
- main: Added Python 3.13 + Lark (Parsing), Ursina (Viewer/3D), Pytest (Testing)

- 001-redscript-compiler: Added Python 3.11+, C++, Lark, Ursina, Pybind11

<!-- MANUAL ADDITIONS START -->
<!-- MANUAL ADDITIONS END -->
