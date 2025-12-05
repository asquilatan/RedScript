# Quickstart: RedScript Compiler

## Prerequisites

- **Python 3.11+**
- **C++ Compiler** (MSVC on Windows, GCC/Clang on Linux/macOS) for extensions.
- **Minecraft 1.20+** (for using exported schematics).
- **Litematica Mod** (fabric) installed in Minecraft.

## Installation

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/your-repo/redstone-hdl.git
    cd redstone-hdl
    ```

2.  **Install Python dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Build C++ Extensions**:
    ```bash
    # Uses setuptools/pybind11 to compile the solver
    pip install .
    ```

## Usage

### 1. Write a Script
Create a file named `door.rs`:

```redscript
// Define a 3x3 Piston Door
door = PistonDoor(width=3, height=3)

// Action
door.open()
wait(20)
door.close()
```

### 2. Compile
Run the compiler CLI:

```bash
python -m redscript.cli compile door.rs --output door.litematic
```

### 3. Visualize (Optional)
Preview the build before exporting:

```bash
python -m redscript.cli view door.litematic
```

### 4. Build in Minecraft
1.  Move `door.litematic` to your Minecraft `schematics` folder.
2.  In-game, press `M` -> `Load Schematics`.
3.  Paste the schematic.
