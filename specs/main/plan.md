# Implementation Plan: Extended Redstone Features

**Branch**: `main` | **Date**: 2025-12-06 | **Spec**: [specs/main/spec.md](specs/main/spec.md)
**Input**: Feature specification from `specs/main/spec.md`

## Summary

This plan covers the implementation of extended Redstone components (Repeaters, Comparators, Slime Blocks, etc.) and improved Camera Controls for the Viewer. The goal is to reach feature parity with common Redstone engineering needs and provide a better user experience for inspecting generated schematics.

## Technical Context

**Language/Version**: Python 3.13
**Primary Dependencies**: Lark (Parsing), Ursina (Viewer/3D), Pytest (Testing)
**Storage**: File-based (.rs source, .litematic output)
**Testing**: pytest (Unit & Integration)
**Target Platform**: Windows, Linux, macOS
**Project Type**: Single Python Package (CLI + GUI)
**Performance Goals**: Viewer should handle 10k+ blocks at 60fps. Compiler should process complex circuits in <5s.
**Constraints**: Must run on standard Python environment. Viewer requires OpenGL support (via Ursina).

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- [x] **Vanilla Survival Purity**: Does the design rely on command blocks or admin tools? (NO - uses standard blocks)
- [x] **Physics-First Logic**: Does the design account for QC, BUD, and sub-tick order? (YES - new blocks must be integrated into safety checks)
- [x] **Time as Semantics**: Are tick delays treated as functional data? (YES - Repeater delays are explicit)
- [x] **Spatial Isolation**: Is cross-talk prevention considered? (YES - Target blocks and Slime blocks introduce new connectivity rules)
- [x] **Kinematic Safety**: Are pulse limiters and safety mechanisms included? (YES - Slime block push limits must be checked)
- [x] **Immediate Visual Verification**: Is 3D preview supported? (YES - Viewer update is part of this plan)

## Project Structure

### Documentation (this feature)

```text
specs/main/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
└── tasks.md             # Phase 2 output
```

### Source Code (repository root)

```text
src/redscript/
├── compiler/
│   ├── lexer/
│   │   └── grammar.lark           # Update: Add new tokens
│   ├── compiler.py                # Update: Block mappings
│   ├── logical_graph.py           # Update: Component definitions
│   ├── safety.py                  # Update: Slime/Piston push limits
│   └── timing/                    # Update: Repeater delays
└── viewer/
    ├── app.py                     # Update: Input handling
    ├── controls.py                # Update: Camera logic
    └── renderer.py                # Update: New block models/colors
```

**Structure Decision**: Extending existing single-package structure.
