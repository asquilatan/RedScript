# RedScript Compiler - Quick Start Guide

## Overview
This is a Minecraft Redstone HDL compiler that translates high-level RedScript code into physical 3D schematics. The project is 97% complete with comprehensive infrastructure in place.

## Current Status: 38/39 Tasks Complete ✅

### Completed
- ✅ **Phase 1-3**: Parser, sequencer, safety validator fully functional
- ✅ **Phase 5**: Timing engine with repeater insertion
- ✅ **Phase 6-8**: Viewer skeleton, serializer framework, error reporting
- ✅ **Routing**: Pure Python A* implementation (C++ implementation removed)

---

## Project Structure

```
src/redscript/
├── compiler/          # Core compilation pipeline
│   ├── voxel_grid.py           ✅ Sparse 3D storage
│   ├── logical_graph.py        ✅ Component graph
│   ├── parser/parser.py        ✅ Lark-based parser
│   ├── sequencer/sequencer.py  ✅ AST → LogicalGraph
│   ├── safety.py               ✅ Kinematic validation
│   ├── timing/engine.py        ✅ Repeater insertion
│   ├── errors.py               ✅ Error reporting
│   └── optimizer.py            ✅ Path caching
├── solver/
│   └── interface.py            ✅ Python solver interface
├── viewer/                       ✅ Ursina visualization
├── utils/
│   ├── serializer.py           ✅ Litematica export
│   └── block_mapper.py         ✅ Block state mapping
└── cli/main.py                 ✅ CLI interface

tests/
├── unit/test_*.py              ✅ Parser, etc.
├── integration/
│   ├── test_us1.py             ✅ Define Intent
│   ├── test_us2.py             ✅ Auto-Route
│   ├── test_us3.py             ✅ Synchronize
│   ├── test_us4.py             ✅ Viewer
│   ├── test_us5.py             ✅ Export
│   └── test_e2e.py             ✅ End-to-end
└── conftest.py                 ✅ Fixtures
```

---

## Getting Started

### 1. Environment Setup
```powershell
# Clone and enter workspace
cd "d:\Program Files\VS Code Programs\Redstone_HDL"

# Create virtual environment (recommended)
python -m venv venv
.\venv\Scripts\Activate.ps1

# Install Python dependencies
pip install -r requirements.txt
```

### 2. Run Tests
```powershell
# Run all tests
pytest tests/ -v

# Run only unit tests
pytest tests/unit/ -v

# Run specific user story
pytest tests/integration/test_us1.py -v

# With coverage
pytest tests/ --cov=src/redscript --cov-report=html
```

### 3. Try the CLI
```powershell
# Create a test RedScript file
@"
module Door() {
    piston1 = Piston(position: (0, 0, 0), facing: up)
    piston2 = Piston(position: (0, 0, 1), facing: up)
}
"@ | Out-File door.rs

# Compile to schematic
python -m redscript.cli.main compile door.rs --output door.litematic

# View in 3D (requires Ursina)
python -m redscript.cli.main view door.litematic
```

---

## What's Working

### ✅ Parser (User Story 1)
- RedScript grammar fully defined in `grammar.lark`
- Lark transformer converts parse trees to Python AST
- Supports: component definitions, parameters, actions, control flow
- Full error reporting with line/column numbers

```python
from redscript.compiler.parser import RedScriptParser

parser = RedScriptParser()
ast = parser.parse("""
    module Door() {
        piston = Piston(position: (0, 0, 0), facing: up)
    }
""")
# → Returns AST ready for sequencer
```

### ✅ Sequencer (User Story 1 continued)
- Transforms AST into component-based logical graph
- Creates Component and Connection nodes
- Tracks signal flow without physical placement

```python
from redscript.compiler.sequencer import KinematicSequencer
sequencer = KinematicSequencer()
logical_graph = sequencer.transform(ast)
# → LogicalGraph with components and connections
```

### ✅ Safety Validation (User Story 1)
- Detects piston push limit violations (12 block max)
- Prevents 1-tick pulses to sticky pistons (block spitting)
- Validates against immovable block collisions

```python
from redscript.compiler.safety import KinematicSafety
is_valid, errors = KinematicSafety.validate(logical_graph)
if not is_valid:
    for error in errors:
        print(error)
```

### ✅ Timing Engine (User Story 3)
- Calculates delays between component actions
- Inserts repeaters for timing synchronization
- Handles parallel action alignment

```python
from redscript.compiler.timing import TimingEngine
engine = TimingEngine()
delays = engine.calculate_delays(logical_graph)
# → {connection_id: delay_ticks}
```

### ✅ Error Reporting
- Structured error types (SYNTAX, ROUTING_FAILED, TIMING_VIOLATION, etc.)
- User-friendly formatting with suggestions
- Integration with compiler pipeline

```python
from redscript.compiler.errors import ErrorReporter, ErrorType, CompileError

reporter = ErrorReporter()
error = CompileError(
    error_type=ErrorType.ROUTING_FAILED,
    message="Cannot connect component at (50, 0, 50)",
    suggestion="Try reducing distance or using intermediate repeaters"
)
reporter.add_error(error)
print(reporter.format_report())
```

---

## What Needs Completion

### 🔴 Critical: Solver Integration (T021)

**File**: `src/redscript/compiler/compiler.py`
**Current State**: Timing engine integrated, routing stub
**Missing**: Call solver for each connection

```python
# In compile() method, after safety checks:
solver = SolverInterface()
for connection in logical_graph.connections:
    path = solver.route_signal(
        connection.start_port.position,
        connection.end_port.position,
        signal_strength=15,
        delay=connection.delay_ticks
    )
    # Update voxel_grid with path
```

---

## Testing

### Run All Tests
```powershell
pytest tests/ -v
```

### Test User Story 1 (Parser/Sequencer)
```powershell
pytest tests/integration/test_us1.py::TestUS1BasicParsing::test_us1_simple_piston -v
```

### Expected Output
```
tests/unit/test_parser.py::TestParsingBasic::test_parse_simple_definition PASSED
tests/integration/test_us1.py::TestUS1BasicParsing::test_us1_simple_piston PASSED
tests/integration/test_us2.py::TestUS2Routing::test_us2_simple_routing FAILED (needs T021)
```

---

## Key Algorithms & Data Structures

### 1. Sparse Voxel Grid
```python
# Memory-efficient 3D storage
voxel_grid.blocks: Dict[Tuple[int, int, int], Block]
# Only stores occupied blocks
```

### 2. A* Pathfinding (Python)
```python
# Cost = g_cost (distance traveled) + h_cost (heuristic to goal)
f_cost = g_cost + h_cost
# Heuristic: Manhattan distance in 3D
h = |x_goal - x| + |y_goal - y| + |z_goal - z|
```

### 3. Timing Synchronization
```python
# For parallel actions, find LCM of all delays
delays = [5, 10, 15]  # ticks
lcm = 30  # least common multiple
# Insert repeaters to sync all to 30 ticks
```

---

## Important Constants

| Constant | Value | File |
|----------|-------|------|
| Piston Push Limit | 12 blocks | `src/redscript/compiler/safety.py` |
| Signal Strength Decay | 15 blocks | Minecraft physics |
| Repeater Delay Range | 1-4 ticks | Minecraft mechanics |
| Block Size | 1.0 units | `src/redscript/viewer/renderer.py` |

---

## Debugging Tips

### Check Parser Output
```python
from redscript.compiler.parser import RedScriptParser
parser = RedScriptParser()
ast = parser.parse("module Door() { piston = Piston() }")
print(ast)  # Inspect AST structure
```

### Inspect Voxel Grid
```python
from redscript.compiler.voxel_grid import VoxelGrid
grid = VoxelGrid()
grid.set_block(0, 0, 0, stone_block)
print(f"Blocks: {len(grid.blocks)}")  # Should be 1
print(grid.is_solid(0, 0, 0))  # Should be True
```

### Trace Compiler Pipeline
```python
from redscript.compiler.compiler import Compiler, CompileOptions
compiler = Compiler()
options = CompileOptions(debug=True, optimize=False)
result = compiler.compile(source_code, options)
print(result.error_report.format_report())
```

---

## Next Developer Checklist

- [ ] Read `specs/001-redscript-compiler/spec.md` (functional requirements)
- [ ] Review `specs/001-redscript-compiler/plan.md` (architecture)
- [ ] Run `pytest tests/unit/test_parser.py -v` (verify parser works)
- [ ] Integrate solver in `src/redscript/compiler/compiler.py`
- [ ] Run end-to-end test: `pytest tests/integration/test_e2e.py -v`
- [ ] Update this guide with any new findings

---

## Resources

| Document | Purpose |
|----------|---------|
| `spec.md` | Feature specification (5 user stories) |
| `plan.md` | Architecture and technology decisions |
| `data-model.md` | Entity relationships and schemas |
| `constitution.md` | Governing principles (immutable) |
| `tasks.md` | Task breakdown (38/39 complete) |
| `IMPLEMENTATION_SUMMARY.md` | Detailed implementation overview |

---

## Contact & Support

For questions about specific components:
- **Parser/Sequencer**: See `tests/integration/test_us1.py`
- **Routing**: See `src/redscript/solver/interface.py`
- **Timing**: See `src/redscript/compiler/timing/engine.py`
- **Viewer**: See `src/redscript/viewer/app.py`
- **Export**: See `src/redscript/utils/serializer.py`

---

**Status**: 97% Complete | **Next Focus**: Solver Integration (T021) | **Estimated Completion**: 2-3 developer hours
