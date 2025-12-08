# Component Reference

This document lists all supported RedScript components and their available properties.

## Common Properties

All components support the following properties:

- `pos` or `position`: Tuple `(x, y, z)` specifying the relative coordinate.

## Component List

### Mechanics

- **Piston**
  - Properties: `facing` (up, down, north, south, east, west), `extended` (true, false)
- **StickyPiston**
  - Properties: `facing`, `extended`
- **Dispenser**
  - Properties: `facing`, `triggered`
- **Dropper**
  - Properties: `facing`, `triggered`
- **Hopper**
  - Properties: `facing`, `enabled`

### Logic & Wiring

- **RedstoneWire**
  - Properties: `power` (0-15), `north`, `south`, `east`, `west` (connection types)
- **Repeater**
  - Properties: `facing`, `delay` (1-4), `locked`
- **Comparator**
  - Properties: `facing`, `mode` (compare, subtract), `powered`
- **RedstoneTorch**
  - Properties: `facing` (for wall torches), `lit`
- **Observer**
  - Properties: `facing`, `powered`

### Input/Output

- **Lever**
  - Properties: `facing`, `face` (floor, wall, ceiling), `powered`
- **Button** (Stone/Oak/etc mapped to generic `Button`)
  - Properties: `facing`, `face`, `powered`
- **PressurePlate**
  - Properties: `powered`
- **Lamp**
  - Properties: `lit`
- **NoteBlock**
  - Properties: `note`, `instrument`, `powered`
- **Target**
  - Properties: `power`
- **Lectern**
  - Properties: `facing`, `has_book`, `powered`
- **DaylightDetector**
  - Properties: `inverted`, `power`
- **TripwireHook**
  - Properties: `facing`, `powered`, `attached`
- **TrappedChest**
  - Properties: `facing`, `type`
- **TNT**
  - Properties: `unstable`
- **Bell**
  - Properties: `facing`, `attachment`, `powered`
- **LightningRod**
  - Properties: `facing`, `powered`
- **SculkSensor**
  - Properties: `sculk_sensor_phase`, `power`, `waterlogged`
- **CalibratedSculkSensor**
  - Properties: `sculk_sensor_phase`, `power`, `waterlogged`, `facing`

### Rails

- **DetectorRail**
  - Properties: `shape`, `powered`
- **PoweredRail**
  - Properties: `shape`, `powered`
- **ActivatorRail**
  - Properties: `shape`, `powered`

### Doors & Gates

- **IronDoor** / **OakDoor**
  - Properties: `facing`, `half`, `hinge`, `open`, `powered`
- **IronTrapdoor** / **OakTrapdoor**
  - Properties: `facing`, `half`, `open`, `powered`, `waterlogged`
- **OakFenceGate**
  - Properties: `facing`, `in_wall`, `open`, `powered`

### Blocks

- **Stone**
- **Glass**
- **SlimeBlock**
- **HoneyBlock**
- **GlazedTerracotta**
  - Properties: `facing`

---

*Note: Property values should generally be strings (e.g., `facing="north"`), but numbers can be used for integer properties like `delay`.*
