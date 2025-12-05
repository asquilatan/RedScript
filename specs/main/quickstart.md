# Quickstart: Extended Features

## Using New Components

```redscript
definition Main {
    # Timing with Repeaters
    rep1 = Repeater(delay: 4)
    rep2 = Repeater(delay: 2)
    
    # Logic with Comparators
    comp = Comparator(mode: "subtract")
    
    # Sticky Mechanics
    piston = StickyPiston(facing: up)
    slime = SlimeBlock(position: (0, 1, 0))
    block = Block("minecraft:stone", position: (0, 2, 0))
    
    # Inputs
    btn = Button(type: "stone", face: "wall")
    plate = PressurePlate(type: "heavy")
    
    # Connections
    btn.signal -> rep1.input
    rep1.output -> comp.side
    plate.signal -> comp.rear
    comp.output -> piston.power
}
```

## Using the Viewer

Launch the viewer with:
```bash
python src/redscript/cli/main.py view my_circuit.rs
```

**Controls**:
- **W/A/S/D**: Move horizontally
- **Space**: Move Up
- **Shift**: Move Down
- **Mouse**: Look around
- **Scroll**: Adjust movement speed
- **Right Click**: Toggle mouse capture (if needed)
