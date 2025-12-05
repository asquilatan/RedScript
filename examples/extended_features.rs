# Extended Features Demo
# Demonstrates Repeaters, Comparators, Slime Blocks, and Target Blocks

# 1. Repeater Delay Chain
# A button triggers a sequence of lamps with increasing delay
button1 = Button(position: (0, 5, 0), facing: up)

rep1 = Repeater(position: (2, 5, 0), facing: east, delay: 1)
rep2 = Repeater(position: (4, 5, 0), facing: east, delay: 2)
rep3 = Repeater(position: (6, 5, 0), facing: east, delay: 4)

lamp1 = Lamp(position: (3, 5, 0))
lamp2 = Lamp(position: (5, 5, 0))
lamp3 = Lamp(position: (7, 5, 0))

button1.signal -> rep1.input
rep1.output -> lamp1.power
rep1.output -> rep2.input
rep2.output -> lamp2.power
rep2.output -> rep3.input
rep3.output -> lamp3.power

# 2. Comparator Subtraction
# A signal strength test
lever_main = Lever(position: (0, 5, 5))
lever_side = Lever(position: (2, 5, 6))

comp = Comparator(position: (2, 5, 5), facing: east, mode: subtract)
lamp_out = Lamp(position: (4, 5, 5))

lever_main.signal -> comp.rear
lever_side.signal -> comp.side
comp.output -> lamp_out.power

# 3. Slime Block Launcher
# A sticky piston pushes a slime block which pushes a block
piston_slime = StickyPiston(position: (10, 5, 0), facing: up)
slime = SlimeBlock(position: (10, 6, 0))
# Using Lamp as a generic block to be pushed
block_on_slime = Lamp(position: (10, 7, 0))

button_launch = Button(position: (8, 5, 0), facing: up)
button_launch.signal -> piston_slime.power

# 4. Target Block Redirection
# A target block pulls wire to activate a piston that would otherwise be missed
lever_target = Lever(position: (10, 5, 5))
target = Target(position: (12, 5, 5))
piston_target = Piston(position: (12, 6, 5), facing: up)

lever_target.signal -> target.power
target.power -> piston_target.power
