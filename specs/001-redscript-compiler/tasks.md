---
description: "Task list for RedScript Compiler implementation"
---

# Tasks: RedScript Compiler

**Input**: Design documents from `/specs/001-redscript-compiler/`
**Prerequisites**: plan.md, spec.md, data-model.md, contracts/

**Tests**: Tests are included as requested by the "Independent Test" sections in spec.md.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing.

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and environment setup.

- [x] T001 Create project directory structure (`src/redscript`, `src/cpp`, `tests`)
- [x] T002 Create `requirements.txt` with `lark`, `ursina`, `litemapy`, `numpy`, `pybind11`
- [x] T003 Create `setup.py` for building C++ extensions with `pybind11`
- [x] T004 Create `src/redscript/cli/main.py` skeleton with argument parsing
- [x] T005 Create `tests/conftest.py` and basic test configuration

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core data structures and language bindings required by all stories.

- [x] T006 [P] Implement `VoxelGrid` and `Block` classes in `src/redscript/compiler/voxel_grid.py`
- [x] T007 [P] Implement `Component` and `LogicalGraph` classes in `src/redscript/compiler/logical_graph.py`
- [x] T008 Implement C++ `SpatialSolver` class skeleton in `src/cpp/solver.cpp` and `src/cpp/solver.h`
- [x] T009 Bind C++ `SpatialSolver` to Python using `pybind11` in `src/cpp/bindings.cpp`
- [x] T010 Verify Python-C++ communication with a simple "Hello World" test in `tests/unit/test_bindings.py` (Requires Build)

## Phase 3: User Story 1 - Define Kinematic Intent (P1)

**Goal**: Parse RedScript and generate a logical graph of components.

- [x] T011 [US1] Define Lark grammar for RedScript in `src/redscript/compiler/lexer/grammar.lark`
- [x] T012 [US1] Implement `RedScriptParser` to generate AST in `src/redscript/compiler/parser/parser.py`
- [x] T013 [US1] Implement `KinematicSequencer` to transform AST to `LogicalGraph` in `src/redscript/compiler/sequencer/sequencer.py`
- [x] T037 [US1] Implement `KinematicSafety` checks (e.g., push limit) in `src/redscript/compiler/safety.py` to validate LogicalGraph
- [x] T014 [US1] Implement unit tests for parsing simple actions (e.g., `piston.extend`) in `tests/unit/test_parser.py`
- [x] T015 [US1] Implement integration test: Compile script to LogicalGraph and verify component existence in `tests/integration/test_us1.py`

## Phase 4: User Story 2 - Auto-Route Wiring (P1)

**Goal**: Route redstone signals between components using C++ A* solver.

- [x] T016 [US2] Implement `load_grid` in C++ `SpatialSolver` to ingest voxel data
- [x] T017 [US2] Implement 3D A* pathfinding algorithm in `src/cpp/pathfinder/astar.cpp`
- [x] T018 [US2] Implement `check_qc_violation` in `src/cpp/constraints/qc.cpp`
- [x] T019 [US2] Implement `find_path` in `SpatialSolver` to use A* and constraints
- [x] T020 [US2] Create Python wrapper `SolverInterface` in `src/redscript/solver/interface.py`
- [ ] T021 [US2] Integrate Solver with Compiler: Route connections in `LogicalGraph` and update `VoxelGrid` (Verify with C++)
- [ ] T022 [US2] Implement integration test: Route two distant components and verify connection in `tests/integration/test_us2.py` (Verify with C++)

## Phase 5: User Story 3 - Synchronize Actions (P2)

**Goal**: Insert repeaters for timing synchronization.

- [x] T023 [US3] Implement `TimingEngine` to calculate required delays in `src/redscript/compiler/timing/engine.py`
- [x] T024 [US3] Update C++ `PathRequest` struct to accept delay parameters
- [x] T025 [US3] Update C++ A* cost function to handle repeater placement (delay cost)
- [x] T026 [US3] Integrate Timing Engine with Solver calls in `src/redscript/compiler/compiler.py`
- [x] T027 [US3] Implement integration test: Verify repeater insertion for delayed actions in `tests/integration/test_us3.py`

## Phase 6: User Story 4 - Visual Inspection (P2)

**Goal**: Render the compiled VoxelGrid in 3D using Ursina.

- [x] T028 [P] [US4] Create Ursina app skeleton in `src/redscript/viewer/app.py`
- [x] T029 [P] [US4] Implement `VoxelRenderer` to convert `VoxelGrid` to Ursina entities in `src/redscript/viewer/renderer.py`
- [x] T030 [P] [US4] Add camera controls (orbit, pan, zoom) in `src/redscript/viewer/controls.py`
- [x] T031 [US4] Add CLI command `view` to launch viewer with a schematic
- [x] T032 [US4] Manual Test: Launch viewer with generated schematic and verify navigation

## Phase 7: User Story 5 - Export to Litematica (P3)

**Goal**: Export VoxelGrid to .litematic file.

- [x] T033 [P] [US5] Implement `LitematicaSerializer` using `litemapy` in `src/redscript/utils/serializer.py`
- [x] T034 [US5] Map internal `Block` types to Minecraft block states (e.g., facing, power)
- [x] T035 [US5] Add CLI command `compile --output` to trigger export
- [x] T036 [US5] Implement integration test: Export design and verify file creation in `tests/integration/test_us5.py`

## Final Phase: Polish & Cross-Cutting

**Purpose**: Error handling and optimization.

- [x] T038 Implement error reporting for "Routing Failed" and "Timing Violation"
- [x] T039 Optimize C++ A* heuristic for larger grids
- [ ] T040 Final end-to-end test: Compile complex script (3x3 door), view, and export

## Dependencies

1.  **Setup** -> **Foundational**
2.  **Foundational** -> **US1**, **US2**, **US4**, **US5**
3.  **US1** -> **US2** (Routing needs Logical Graph)
4.  **US2** -> **US3** (Timing modifies Routing)
5.  **US2** -> **US5** (Export needs routed grid)

## Parallel Execution Examples

- **US1 (Parser)** and **US4 (Viewer)** can be developed in parallel by different developers once Phase 2 is done.
- **US5 (Export)** can be developed in parallel with **US2 (Routing)** using mock VoxelGrids.
