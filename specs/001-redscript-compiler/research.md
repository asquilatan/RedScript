# Research: Redstone HDL Compiler Dependencies & Algorithms

## 1. Python 3D Visualization

### Comparison
We compared **Ursina**, **ModernGL**, and **Pyglet** for rendering a 3D voxel grid (target: 10k+ blocks).

| Feature | **Ursina** | **ModernGL** | **Pyglet** |
| :--- | :--- | :--- | :--- |
| **Backend** | Panda3D (High-level) | OpenGL 3.3+ Core (Low-level wrapper) | OpenGL (via ctypes) |
| **Performance** | Good (batched), but overhead of full engine. | **Best**. Direct GPU control, minimal overhead. | Moderate. Pure Python, depends on optimization. |
| **Ease of Use** | **Easiest**. Pythonic, minimal boilerplate. | Moderate. Requires GLSL shader knowledge. | Moderate/Hard. Low-level windowing/GL handling. |
| **Dependencies** | Heavy (`panda3d`, `pillow`, etc.) | Lightweight (`moderngl`, `glcontext`) | **Lightest**. No external C deps (pure python). |
| **Voxel Suitability**| Good for rapid prototyping. | Excellent for massive instance rendering. | Good, but requires manual mesh generation. |

### Recommendation
**Decision**: Use **Ursina** for the MVP "Live Voxel Viewer", but architect the renderer to allow swapping to **ModernGL** if performance bottlenecks (FPS < 30 at 10k blocks) occur.

**Rationale**:
*   **Ursina** allows extremely fast iteration. We can get a viewer running in <100 lines of code.
*   It handles input, camera, and windowing out of the box.
*   For a "compiler" tool, the viewer is a secondary debug feature, so "Ease of use" > "Raw Performance" initially.
*   **ModernGL** is the backup plan if we need to render 100k+ blocks smoothly, as it allows using Geometry Shaders or Instanced Rendering efficiently.

---

## 2. Litematica Export

### Findings
*   **Library**: `litemapy` (https://github.com/SmylerMC/litemapy)
*   **Status**: Active. Supports reading/writing `.litematic` format.
*   **Features**:
    *   Full support for Regions (essential for multi-section builds).
    *   Block state handling (e.g., `minecraft:redstone_wire[power=15]`).
    *   Metadata support (Author, Description).
*   **Compatibility**: Supports modern Minecraft versions (1.13+ format, compatible with 1.20+).

### Recommendation
**Decision**: Use **`litemapy`**.

**Rationale**:
*   It is the standard Python library for this specific file format.
*   It abstracts the complex NBT structure of `.litematic` files.
*   Allows us to focus on generating the *logic* (block placement) rather than the *binary format*.

---

## 3. 3D Routing Algorithms

### Findings
*   **Problem**: Routing redstone signals in 3D space is a **Pathfinding with Constraints** problem.
*   **Constraints**:
    *   **Support**: Redstone dust requires a solid block beneath it.
    *   **Verticality**: Signals travel up/down via specific mechanisms (Glass towers, Torches, Slabs).
    *   **Isolation**: Lines cannot be adjacent (Manhattan distance > 1 for parallel lines) to avoid cross-talk, unless insulated.
*   **Algorithms**:
    *   **A* (A-Star)**: Best for point-to-point. Needs a custom `neighbors()` function to enforce Redstone mechanics.
    *   **Channel Routing**: Used in silicon chips. Might be applicable if we enforce a "layer" structure (e.g., X-axis on y=0, Z-axis on y=2).

### Recommendation
**Decision**: Implement **3D A*** in **C++** using **pybind11**.

**Rationale**:
*   **Performance**: Pathfinding on large voxel grids (100x100x100) is computationally expensive. Python's overhead for the A* loop (millions of iterations) is too high for interactive feedback.
*   **Scalability**: C++ allows us to handle complex constraints (QC, BUD) without performance penalties.
*   **Integration**: `pybind11` provides seamless integration with Python, allowing us to keep the high-level logic in Python while offloading the heavy lifting.

### Proposed Routing Strategy
1.  **Layering**: Dedicate Y-levels to specific directions if possible (heuristic).
2.  **Cost Function**:
    *   Wire: Low cost.
    *   Repeater: Medium cost (adds delay).
    *   Vertical transmission: High cost (complexity).
    *   Cross-talk risk: Infinite cost (forbidden).

---

## 4. C++ Build System

### Findings
*   **Options**: `setuptools` (with `Extension`), `scikit-build` (CMake wrapper), `meson`.
*   **Requirements**: Cross-platform (Windows/Linux), easy integration with `pip`.

### Recommendation
**Decision**: Use **`setuptools`** with a custom `Extension` class or **`scikit-build`**.
For simplicity in this project, we will use **`setuptools`** with standard `Extension` if dependencies are minimal, or **CMake** if we need complex include paths.
Given we are using `pybind11`, a simple `setup.py` with `pybind11.setup_helpers` is sufficient and standard.

**Rationale**:
*   `pybind11` includes helpers for `setuptools`.
*   Avoids needing a full CMake setup for a single extension.

