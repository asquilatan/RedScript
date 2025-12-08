# RedScript User Guide

Welcome to the RedScript User Guide! RedScript is a hardware description language for Minecraft Redstone that allows you to define circuits using high-level code and compile them into `.litematic` schematics.

## Table of Contents

1. [Getting Started](#getting-started)
2. [Basic Concepts](#basic-concepts)
3. [Defining Components](#defining-components)
4. [Connecting Components](#connecting-components)
5. [Modules](#modules)
6. [Control Flow](#control-flow)
7. [Assertions](#assertions)

---

## Getting Started

To compile a RedScript file, use the CLI tool:

```bash
redscript compile my_circuit.rs --output my_circuit.litematic
```

You can then load the `.litematic` file in Minecraft using the Litematica mod.

## Basic Concepts

RedScript files (`.rs`) consist of a series of statements. Statements can define components, modules, connections, or control flow logic.

### Coordinates
RedScript uses relative coordinates. When you define a component at `(0, 0, 0)`, it will be placed at the origin of your schematic.

## Defining Components

Components are the physical blocks in your circuit (e.g., Pistons, Repeaters, Redstone Dust). You define them using the assignment syntax:

```rust
name = Type(property=value, ...)
```

Example:

```rust
// A piston at (0, 0, 0) facing up
p1 = Piston(pos=(0, 0, 0), facing="up")

// A repeater with 2 ticks delay
r1 = Repeater(pos=(0, 0, 1), delay=2, facing="north")
```

See the [Component Reference](COMPONENT_REFERENCE.md) for a full list of available components and their properties.

## Connecting Components

You can define logical connections between components using the arrow syntax `->`. This instructs the compiler's auto-router to find a path for the redstone signal.

```rust
// Connect button signal to lamp power
btn = Button(pos=(0, 0, 0))
lamp = Lamp(pos=(5, 0, 0))

btn.signal -> lamp.power
```

*Note: The auto-router will automatically place redstone dust, repeaters, and glass blocks to connect the two points.*

## Modules

Modules allow you to encapsulate logic and reuse sub-circuits.

### Defining a Module

```rust
module PistonDoor() {
    p1 = Piston(pos=(0, 0, 0), facing="east")
    p2 = Piston(pos=(0, 1, 0), facing="east")

    // Internal logic...
}
```

### Using a Module

```rust
// Instantiate the door
door = PistonDoor()
```

## Control Flow

RedScript supports procedural generation using loops and conditionals. This happens at *compile time*, meaning the loop runs to generate multiple blocks in the schematic.

### For Loops

```rust
// Create a wall of lamps
for x in range(0, 5) {
    for y in range(0, 5) {
        lamp = Lamp(pos=(x, y, 0))
    }
}
```

### If Statements

```rust
enable_lights = 1

for x in range(0, 5) {
    block = Stone(pos=(x, 0, 0))

    if (enable_lights == 1) {
        lamp = Lamp(pos=(x, 1, 0))
    }
}
```

## Assertions

You can use assertions to verify properties of your circuit during compilation.

```rust
p = Piston(facing="up")

// Verify the facing direction
assert(p.facing == "up")
```
