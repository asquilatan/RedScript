# Data Model: RedScript Compiler

## Abstract Syntax Tree (AST)

The AST represents the parsed RedScript code.

### Nodes

- **Program**: Root node. Contains a list of `Statement`s.
- **Statement**: Base class for executable instructions.
    - **Action**: A kinematic command (e.g., `piston.extend()`).
        - `target`: ComponentID
        - `operation`: Enum (EXTEND, RETRACT, MOVE)
        - `parameters`: Dict (e.g., `delay=4`)
    - **Definition**: Defining a component (e.g., `door = Door(3,3)`).
    - **ControlFlow**: `Parallel`, `Sequence` blocks.

## Logical Graph

The intermediate representation (IR) before physical placement.

### Entities

- **Component**: A logical unit.
    - `id`: UUID
    - `type`: String (PISTON, LEVER, REPEATER)
    - `inputs`: List[Port]
    - `outputs`: List[Port]
    - `dimensions`: Vector3
- **Port**: A connection point on a component.
    - `offset`: Vector3 (relative to component origin)
    - `signal_type`: Enum (REDSTONE, MECHANICAL)
- **Connection**: A logical link between ports.
    - `source`: PortID
    - `target`: PortID
    - `min_delay`: Int (ticks)
    - `max_delay`: Int (ticks)

## Voxel Grid (Physical Model)

The 3D representation of the world.

### Entities

- **Grid**: A sparse 3D array (Hash Map `(x,y,z) -> Block`).
    - `bounds`: AABB (Axis Aligned Bounding Box)
- **Block**:
    - `material`: String (e.g., "minecraft:stone")
    - `properties`: Dict (e.g., `{"facing": "north", "powered": "true"}`)
- **Schematic**: Wrapper for Grid + Metadata.
    - `author`: String
    - `regions`: List[Region]

## Routing

### Entities

- **PathRequest**:
    - `start`: Vector3
    - `end`: Vector3
    - `signal_strength`: Int
- **PathResult**:
    - `nodes`: List[Vector3]
    - `blocks_placed`: List[Block] (Dust, Repeaters, Glass)

## C++ Data Structures (Solver)

Structures used in the C++ extension for performance.

### Structs

- **Vec3**: Simple 3D integer vector.
    - `x`, `y`, `z`: int
- **BlockInfo**: Minimal block data for solver.
    - `is_solid`: bool
    - `is_redstone_component`: bool
- **PathRequest**:
    - `start`: Vec3
    - `end`: Vec3
    - `signal_strength`: int
    - `min_delay`: int
- **SolverGrid**: Flattened or sparse representation of the VoxelGrid for fast access.

