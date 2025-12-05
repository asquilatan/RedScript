# 2x2 Piston Door
# A flush 2x2 piston door with 4 sticky pistons

# Define the four pistons in a 2x2 grid
piston1 = StickyPiston(position: (10, 5, 10), facing: up)
piston2 = StickyPiston(position: (11, 5, 10), facing: up)
piston3 = StickyPiston(position: (10, 5, 11), facing: up)
piston4 = StickyPiston(position: (11, 5, 11), facing: up)

# Define a lever to control the door
lever = Lever(position: (8, 5, 10))

# Connect lever to all pistons (parallel activation)
lever.signal -> piston1.power
lever.signal -> piston2.power
lever.signal -> piston3.power
lever.signal -> piston4.power
