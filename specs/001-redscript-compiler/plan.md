# Implementation Plan: RedScript Compiler

**Branch**: `001-redscript-compiler` | **Date**: 2025-12-06 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/001-redscript-compiler/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

The RedScript Compiler translates high-level kinematic intent into optimized 3D voxel schematics. It features a Kinematic Sequencer for motion primitives, a 3D Auto-Router for signal pathfinding, a Timing Engine for synchronization, and a Live Voxel Viewer for visual verification. The architecture uses Python for orchestration and UI, with **C++ extensions (via pybind11)** for high-performance 3D A* pathfinding and constraint solving.

## Technical Context

**Language/Version**: Python 3.11+ (Orchestrator, UI), C++17 (Pathfinding/Solver extensions)
**Primary Dependencies**: `lark` (Parser), `ursina` (Visualization), `numpy` (Voxel grid), `litemapy` (Export), `pybind11` (C++ bindings)
**Storage**: File-based (`.rs` source, `.litematic` output)
**Testing**: `pytest` (Python), `catch2` (C++ unit tests), `tox` (Integration)
**Target Platform**: Windows/Linux/macOS (Desktop)
**Project Type**: Python Project with C++ extensions
**Performance Goals**: < 1s compile time for standard doors, > 60 FPS visualization
**Constraints**: Vanilla Minecraft mechanics (QC, BUD, Sub-tick)
**Scale/Scope**: Single-user desktop application

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- [x] **Vanilla Survival Purity**: Does the design rely on command blocks or admin tools? (Must be NO) - Confirmed NO.
- [x] **Physics-First Logic**: Does the design account for QC, BUD, and sub-tick order? - Yes, via Kinematic Sequencer.
- [x] **Time as Semantics**: Are tick delays treated as functional data? - Yes, via Timing Engine.
- [x] **Spatial Isolation**: Is cross-talk prevention considered? - Yes, via Auto-Router.
- [x] **Kinematic Safety**: Are pulse limiters and safety mechanisms included? - Yes, via Safety Check.
- [x] **Immediate Visual Verification**: Is 3D preview supported? - Yes, via Live Voxel Viewer.

## Project Structure

### Documentation (this feature)

```text
specs/001-redscript-compiler/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output
└── tasks.md             # Phase 2 output
```

### Source Code (repository root)

```text
src/
├── redscript/
│   ├── compiler/        # Core logic
│   │   ├── lexer/       # Lark grammar and lexer
│   │   ├── parser/      # AST generation
│   │   ├── sequencer/   # Kinematic Sequencer
│   │   └── timing/      # Timing Engine
│   ├── solver/          # C++ extensions (bindings)
│   │   ├── _solver.pyd  # Compiled extension
│   │   └── interface.py # Python wrapper
│   ├── viewer/          # Visualization
│   │   ├── app.py       # Ursina/ModernGL app
│   │   └── renderer.py  # Voxel rendering
│   ├── cli/             # Command line interface
│   └── utils/           # Helpers (Litematica export)
└── cpp/                 # C++ source
    ├── pathfinder/      # A* implementation
    ├── constraints/     # QC/BUD constraints
    └── bindings.cpp     # Pybind11 bindings

tests/
├── unit/                # Python unit tests
├── integration/         # End-to-end compiler tests
└── cpp/                 # C++ unit tests
```

**Structure Decision**: Hybrid Python/C++ structure. Python handles the high-level logic, AST, and UI. C++ handles the computationally intensive 3D pathfinding and constraint solving.


## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., 4th project] | [current need] | [why 3 projects insufficient] |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient] |
