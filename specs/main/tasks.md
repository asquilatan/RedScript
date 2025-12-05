# Tasks: Extended Redstone Features

**Feature**: Extended Redstone Features
**Status**: In Progress

## Phase 1: Foundational (Grammar & Data Structures)
**Goal**: Update the core language and compiler structures to support new component types.
**Independent Test**: `pytest tests/unit/test_parser.py` should pass with new syntax.

- [x] T001 [P] Update `grammar.lark` with new component tokens (Repeater, Comparator, Slime, etc.)
- [x] T002 [P] Update `ComponentType` enum in `src/redscript/compiler/logical_graph.py`
- [x] T003 [P] Update `Compiler.COMPONENT_BLOCKS` mapping in `src/redscript/compiler/compiler.py`
- [x] T004 Create unit tests for parsing new components in `tests/unit/test_parser_extended.py`

## Phase 2: Camera Controls (Viewer)
**Goal**: Implement Spectator Mode controls for the 3D viewer.
**Independent Test**: Launch viewer and verify WASD/Space/Shift movement.

- [x] T005 [P] Implement `SpectatorController` class in `src/redscript/viewer/controls.py`
- [x] T006 Update `VoxelViewer` in `src/redscript/viewer/app.py` to use `SpectatorController`
- [x] T007 Add scroll wheel speed adjustment to `SpectatorController`

## Phase 3: Logic Components (Repeater, Comparator, Torch)
**Goal**: Implement logic and rendering for Repeaters, Comparators, and Torches.
**Independent Test**: Compile and view a circuit with these components.

- [x] T008 [P] Update `VoxelRenderer` in `src/redscript/viewer/renderer.py` to render Repeaters/Comparators
- [x] T009 [P] Update `TimingEngine` in `src/redscript/compiler/timing/engine.py` to handle Repeater delays
- [x] T010 Create integration test `tests/integration/test_logic_components.py`

## Phase 4: Mechanical Components (Slime, Honey)
**Goal**: Implement sticky block mechanics and safety checks.
**Independent Test**: Compile a slime block flying machine (or simple pusher).

- [x] T011 [P] Implement recursive cluster finding in `src/redscript/compiler/safety.py`
- [x] T012 Implement push limit check (12 blocks) in `src/redscript/compiler/safety.py`
- [x] T013 Update `VoxelRenderer` to render transparent Slime/Honey blocks
- [x] T014 Create integration test `tests/integration/test_mechanics.py`

## Phase 5: Input & Target Components
**Goal**: Implement inputs (Buttons, Plates) and Target Blocks.
**Independent Test**: Compile a circuit using buttons and target blocks.

- [x] T015 [P] Update `VoxelRenderer` for Buttons, Plates, and Target Blocks
- [x] T016 Update `SolverInterface` to handle Target Block connectivity (if applicable)
- [x] T017 Create demo script `examples/extended_features.rs`

## Phase 6: Polish & Verification
**Goal**: Ensure all features work together and performance is acceptable.

- [x] T018 Run full regression suite `pytest tests/`
- [x] T019 Verify viewer performance with large schematic
- [x] T020 Update `README.md` with new features

## Dependencies
- Phase 1 blocks Phase 3, 4, 5.
- Phase 2 is independent of Phase 1 (mostly).
- Phase 3, 4, 5 can be done in parallel.

## Implementation Strategy
1. Start with Phase 1 to unblock the compiler.
2. Implement Phase 2 (Viewer) early to help debug Phase 3-5.
3. Implement Phase 3, 4, 5 incrementally.
