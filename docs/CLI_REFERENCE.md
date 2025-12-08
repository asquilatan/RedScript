# CLI Reference

The RedScript Command Line Interface (CLI) is the primary tool for compiling and managing RedScript projects.

## Installation

Ensure you have the required dependencies installed:

```bash
pip install -r requirements.txt
```

## Usage

```bash
python -m redscript.cli.main [COMMAND] [OPTIONS]
```

## Commands

### `compile`

Compiles a `.rs` file into a `.litematic` schematic.

**Usage:**
```bash
redscript compile <input_file> [options]
```

**Options:**
- `--output`, `-o`: Specify the output file path. Defaults to input filename with `.litematic` extension.
- `--view`, `-v`: Open the 3D viewer immediately after compilation.
- `--debug`: Enable debug mode (prints AST and verbose logs).
- `--no-optimize`: Disable route optimization.

**Example:**
```bash
redscript compile designs/door.rs -o build/door.litematic --view
```

### `view`

Opens the 3D viewer for an existing `.litematic` file.

**Usage:**
```bash
redscript view <file>
```

**Example:**
```bash
redscript view build/door.litematic
```

### `check` (Planned)

Validates the syntax and safety of a script without generating output.

**Usage:**
```bash
redscript check <input_file>
```
