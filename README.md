# RedScript HDL

RedScript is a Hardware Description Language (HDL) for Minecraft Redstone. It allows you to define circuits using high-level code and compile them into Litematica schematics.

## Features

- **High-Level Syntax**: Define components and connections easily.
- **Compilation**: Generates `.litematic` files for use with Litematica mod.
- **Simulation**: (Experimental) Simulate circuit logic.
- **3D Viewer**: Preview your circuit before building.

## Supported Components

- **Basic**: Redstone Wire, Torch, Block, Lever
- **Logic**: Repeater, Comparator
- **Mechanics**: Piston, Sticky Piston, Slime Block, Honey Block
- **Input/Output**: Button, Pressure Plate, Lamp, Target Block, Note Block, Dropper, Hopper, Observer

## Installation

```bash
pip install redscript
```

## Usage

1. Write your script (e.g., `circuit.rs`):
   ```rust
   button = Button(position: (0, 5, 0))
   lamp = Lamp(position: (2, 5, 0))
   button.signal -> lamp.power
   ```

2. Compile and View:
   ```bash
   redscript compile circuit.rs --view
   ```

## Extended Features

RedScript now supports:
- **Repeaters**: Configurable delay (1-4 ticks).
- **Comparators**: Compare and Subtract modes.
- **Slime/Honey Blocks**: Sticky mechanics with push limit checks (12 blocks).
- **Target Blocks**: Redirection of redstone wire.
- **Spectator Mode**: Fly through your circuit in the 3D viewer (WASD + Mouse).

ps: Hail Specify, Gemini 3.0 Pro, and Opus 4.5.