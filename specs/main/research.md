# Research: Extended Redstone Features

## 1. Camera Controls (Ursina)
**Decision**: Implement a custom `SpectatorController` class.
**Rationale**: The built-in `FirstPersonController` enforces gravity and collision, which is undesirable for inspecting large redstone circuits. `EditorCamera` is orbital, which is good for objects but bad for flying through circuits.
**Implementation Details**:
- Inherit from `Entity`.
- Update position based on `held_keys` (w, a, s, d, space, shift).
- Update rotation based on mouse input.
- Speed multiplier with scroll wheel.

## 2. Redstone Mechanics
### 2.1 Slime & Honey Blocks
**Decision**: Implement a recursive "Block Cluster" finder in `KinematicSafety`.
**Rationale**: Piston pushes are limited to 12 blocks. Slime/Honey blocks recursively pull/push attached blocks.
**Rules**:
- Slime sticks to Slime and non-slime blocks.
- Honey sticks to Honey and non-honey blocks.
- Slime does NOT stick to Honey.
- Glazed Terracotta, Obsidian, Bedrock, etc. are non-sticky/immovable.

### 2.2 Target Blocks
**Decision**: Treat Target Blocks as "strongly powered" components that attract wire connections.
**Rationale**: In Minecraft, redstone wire automatically redirects to point at a Target Block. The `Solver` (A*) needs to cost connections to Target Blocks favorably or explicitly route to them.

### 2.3 Repeaters & Comparators
**Decision**:
- **Repeater**: Model as a directed component with `delay` (1-4) and `locked` state.
- **Comparator**: Model as a component with `mode` (compare/subtract).
**Rationale**: Essential for logic gates and timing.

## 3. Unknowns Resolved
- **Immovable Blocks**: Defined list (Obsidian, Bedrock, etc.).
- **Moveable Blocks**: All standard blocks + Honey/Slime special interactions.
- **Viewer Performance**: Instancing is handled by Ursina's `Mesh` or `Entity` parenting. For 10k blocks, we might need to combine meshes if performance drops, but individual entities are fine for now.

