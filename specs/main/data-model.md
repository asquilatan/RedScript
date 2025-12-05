# Data Model: Extended Redstone Features

## 1. Component Types
New additions to `ComponentType` enum:

| Type | Properties | Description |
|------|------------|-------------|
| `REPEATER` | `delay` (1-4), `locked` (bool) | Signal repeater/delayer |
| `COMPARATOR` | `mode` ("compare", "subtract") | Logic comparator |
| `OBSERVER` | `facing` (direction) | Detects block updates |
| `DROPPER` | `facing` (direction) | Drops items |
| `HOPPER` | `facing` (direction), `enabled` (bool) | Moves items |
| `TARGET` | None | Redirects redstone |
| `SLIME_BLOCK` | None | Sticky block |
| `HONEY_BLOCK` | None | Sticky block (doesn't stick to slime) |
| `REDSTONE_TORCH` | `facing` (direction) | Inverts signal |
| `PRESSURE_PLATE` | `type` ("stone", "wood", "heavy", "light") | Input source |
| `BUTTON` | `type` ("stone", "wood"), `face` (wall/floor/ceiling) | Input pulse |

## 2. Block Properties
Standardized properties for compilation:

- **Facing**: `north`, `south`, `east`, `west`, `up`, `down`.
- **Delay**: Integer `1`, `2`, `3`, `4`.
- **Mode**: `compare`, `subtract`.
- **Face**: `floor`, `wall`, `ceiling`.

## 3. Kinematic Graph
Updated `LogicalGraph` to support:
- **Cluster Nodes**: Groups of blocks moved together by pistons (via Slime/Honey).
- **Strong/Weak Power**: Distinction for Target Blocks and Repeaters.

## 4. Viewer Entities
- **Models**: Need simple geometric approximations (cubes, torches, plates).
- **Colors**:
  - Slime: Green transparent
  - Honey: Orange transparent
  - Target: White/Red rings
  - Repeater/Comparator: Stone slab-like
