import pytest
from redscript.compiler.voxel_grid import VoxelGrid, Block
from redscript.compiler.safety import KinematicSafety
from redscript.compiler.logical_graph import LogicalGraph

class TestMechanics:
    def setup_method(self):
        self.grid = VoxelGrid()
        self.graph = LogicalGraph()

    def test_piston_push_limit_ok(self):
        # Piston at (0,0,0) facing East
        self.grid.set_block(0, 0, 0, Block("minecraft:piston", {"facing": "east"}))
        
        # 12 Stone blocks in front (1,0,0) to (12,0,0)
        for x in range(1, 13):
            self.grid.set_block(x, 0, 0, Block("minecraft:stone"))
            
        is_valid, errors = KinematicSafety.validate_physical(self.grid, self.graph)
        assert is_valid
        assert len(errors) == 0

    def test_piston_push_limit_exceeded(self):
        # Piston at (0,0,0) facing East
        self.grid.set_block(0, 0, 0, Block("minecraft:piston", {"facing": "east"}))
        
        # 13 Stone blocks in front (1,0,0) to (13,0,0)
        for x in range(1, 14):
            self.grid.set_block(x, 0, 0, Block("minecraft:stone"))
            
        is_valid, errors = KinematicSafety.validate_physical(self.grid, self.graph)
        assert not is_valid
        assert "exceeds push limit" in errors[0]

    def test_immovable_block(self):
        # Piston at (0,0,0) facing East
        self.grid.set_block(0, 0, 0, Block("minecraft:piston", {"facing": "east"}))
        
        # Obsidian at (1,0,0)
        self.grid.set_block(1, 0, 0, Block("minecraft:obsidian"))
        
        is_valid, errors = KinematicSafety.validate_physical(self.grid, self.graph)
        assert not is_valid
        assert "immovable block" in errors[0]

    def test_slime_block_stickiness(self):
        # Piston at (0,10,0) facing East
        self.grid.set_block(0, 10, 0, Block("minecraft:sticky_piston", {"facing": "east"}))
        
        # Slime block at (1,10,0)
        self.grid.set_block(1, 10, 0, Block("minecraft:slime_block"))
        
        # Blocks attached to slime on sides
        # (1,11,0) - Up
        self.grid.set_block(1, 11, 0, Block("minecraft:stone"))
        # (1,9,0) - Down
        self.grid.set_block(1, 9, 0, Block("minecraft:stone"))
        
        # Total pushed: Slime(1) + Up(1) + Down(1) = 3. OK.
        is_valid, errors = KinematicSafety.validate_physical(self.grid, self.graph)
        assert is_valid

        # Add 10 more blocks to the "Up" chain to exceed limit
        # Current count 3. Limit 12. Need 10 more -> 13.
        for y in range(12, 22):
            self.grid.set_block(1, y, 0, Block("minecraft:stone"))
            
        # Now we have Slime(1) + Down(1) + Up_Chain(11) = 13 blocks
        
        # Reset grid
        self.grid = VoxelGrid()
        self.grid.set_block(0, 10, 0, Block("minecraft:sticky_piston", {"facing": "east"}))
        self.grid.set_block(1, 10, 0, Block("minecraft:slime_block"))
        
        # 11 Stones in front
        for x in range(2, 13):
            self.grid.set_block(x, 10, 0, Block("minecraft:stone"))
            
        # 1 Stone on top of Slime
        self.grid.set_block(1, 11, 0, Block("minecraft:stone"))
        
        is_valid, errors = KinematicSafety.validate_physical(self.grid, self.graph)
        assert not is_valid
        assert "exceeds push limit" in errors[0]

    def test_slime_honey_interaction(self):
        # Slime and Honey do not stick to each other
        # Piston (0,0,0) East
        self.grid.set_block(0, 0, 0, Block("minecraft:piston", {"facing": "east"}))
        
        # Slime (1,0,0)
        self.grid.set_block(1, 0, 0, Block("minecraft:slime_block"))
        
        # Honey (1,1,0) - On top of Slime
        self.grid.set_block(1, 1, 0, Block("minecraft:honey_block"))
        
        # If they stuck, Honey would be moved.
        # But they don't stick. So Honey stays.
        # Pushed count should be 1 (Slime only).
        
        # Wait, my BFS logic counts "pushed blocks".
        # If Honey is not stuck, it is not in the set.
        # So count = 1.
        
        is_valid, errors = KinematicSafety.validate_physical(self.grid, self.graph)
        assert is_valid
        
        # To verify it didn't count Honey, let's make Honey have a huge chain attached to it that would fail if counted.
        # Honey at (1,1,0).
        # 12 blocks attached to Honey? No, Honey is sticky too.
        # If Honey was counted, it would check its neighbors.
        # Let's put 12 blocks in front of Honey (1,1,0) -> (2,1,0)...
        # If Honey moves, it pushes them.
        
        for x in range(2, 15):
            self.grid.set_block(x, 1, 0, Block("minecraft:stone"))
            
        # If Honey was picked up, total > 12.
        # Since not picked up, total = 1 (Slime).
        is_valid, errors = KinematicSafety.validate_physical(self.grid, self.graph)
        assert is_valid

    def test_glazed_terracotta(self):
        # Glazed Terracotta doesn't stick to Slime
        self.grid.set_block(0, 0, 0, Block("minecraft:piston", {"facing": "east"}))
        self.grid.set_block(1, 0, 0, Block("minecraft:slime_block"))
        
        # Glazed Terracotta on top (1,1,0)
        self.grid.set_block(1, 1, 0, Block("minecraft:magenta_glazed_terracotta"))
        
        # Add 12 blocks in front of the Terracotta to ensure if it moved it would fail
        for x in range(2, 15):
            self.grid.set_block(x, 1, 0, Block("minecraft:stone"))
            
        is_valid, errors = KinematicSafety.validate_physical(self.grid, self.graph)
        assert is_valid
