# Feature Specification: Extended Redstone Blocks & Camera Controls

## 1. Overview
This feature expands the Redstone HDL language and compiler to support a wider range of Minecraft redstone components and mechanics. It also enhances the built-in 3D viewer with better camera controls for easier inspection of generated structures.

## 2. Functional Requirements

### 2.1 Camera Controls
- Implement "Spectator Mode" style controls.
- **Movement**: WASD for horizontal movement, Space/Shift for vertical movement (Up/Down).
- **Speed**: Scroll wheel to adjust movement speed.
- **Look**: Mouse look (already partially implemented, ensure it's smooth and toggleable if needed).

### 2.2 New Components
The following components must be added to the language grammar, compiler, and viewer:

#### 2.2.1 Logic & Timing
- **Repeater**:
  - Properties: `delay` (1-4 ticks), `locked` (boolean).
  - Functionality: Signal amplification, delay, locking mechanism.
- **Comparator**:
  - Properties: `mode` (compare/subtract).
  - Functionality: Signal comparison, subtraction, container inventory reading (if applicable, though containers might be out of scope for now, just signal processing).
- **Redstone Torch**:
  - Functionality: Signal inversion, vertical transmission (torch towers).

#### 2.2.2 Mechanical & Structural
- **Slime Block**:
  - Functionality: Sticky behavior (moves adjacent blocks).
- **Honey Block** (Moveable):
  - Functionality: Similar to slime but doesn't stick to slime.
- **Immovable Blocks**:
  - Examples: Obsidian, Bedrock (if creative), Glazed Terracotta.
  - Functionality: Cannot be pushed/pulled by pistons.
- **Target Block**:
  - Functionality: Redirects redstone wire into it.

#### 2.2.3 Inputs
- **Pressure Plate**:
  - Types: Stone, Wood, Heavy (Iron), Light (Gold).
  - Functionality: Emits signal when entity is on top (simulation might just treat it as a source).
- **Button**:
  - Types: Stone, Wood.
  - Functionality: Emits temporary pulse.

## 3. Technical Requirements
- **Grammar**: Update `grammar.lark` to include new component types and properties.
- **Compiler**:
  - Update `ComponentType` enum.
  - Update `Compiler.COMPONENT_BLOCKS` mapping.
  - Update `KinematicSequencer` and `KinematicSafety` to handle new block interactions (especially Slime/Honey connectivity).
- **Viewer**:
  - Add rendering support for new blocks (colors/models).
  - Update `CameraControls` class.

## 4. Constraints
- Must adhere to "Vanilla Survival Purity" (no command blocks).
- Must respect "Physics-First Logic" (QC, update order).
- "Time as Semantics": Repeater delays must be accurately modeled in the timing engine.

