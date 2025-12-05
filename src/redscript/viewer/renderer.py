"""
Voxel Renderer: Converts voxel grid to 3D entities
"""
from ursina import Entity, color, Vec3
from redscript.compiler.voxel_grid import VoxelGrid

class VoxelRenderer:
    """Renders voxel blocks as 3D entities in Ursina"""
    
    # Rainbow-style colors for easy debugging
    BLOCK_COLORS = {
        'minecraft:stone': color.light_gray,
        'minecraft:piston': color.yellow,
        'minecraft:sticky_piston': color.orange,
        'minecraft:redstone_wire': color.red,
        'minecraft:repeater': color.lime,
        'minecraft:comparator': color.green,
        'minecraft:glass': color.azure,
        'minecraft:air': None,
        'minecraft:redstone_block': color.red,
        'minecraft:observer': color.violet,
        'minecraft:lever': color.brown,
        'minecraft:dropper': color.gray,
        'minecraft:hopper': color.dark_gray,
        'minecraft:target': color.pink,
        'minecraft:slime_block': color.lime,
        'minecraft:honey_block': color.gold,
        'minecraft:redstone_torch': color.orange,
        'minecraft:stone_pressure_plate': color.light_gray,
        'minecraft:stone_button': color.white,
        'minecraft:redstone_lamp': color.brown,
        'minecraft:lit_redstone_lamp': color.gold,
    }

    @staticmethod
    def render_grid(voxel_grid: VoxelGrid, parent_entity: Entity = None) -> list[Entity]:
        """Render the entire voxel grid"""
        entities = []
        
        for (x, y, z), block in voxel_grid.blocks.items():
            if block.material == 'minecraft:air':
                continue
                
            col = VoxelRenderer.BLOCK_COLORS.get(block.material, color.magenta)  # Magenta = missing
            if col is None:
                continue
            
            scale = Vec3(1, 1, 1)
            
            # Custom scaling for flat blocks
            if block.material == 'minecraft:redstone_wire':
                scale = Vec3(0.9, 0.1, 0.9)
            elif block.material in ['minecraft:repeater', 'minecraft:comparator']:
                scale = Vec3(0.9, 0.2, 0.9)
            elif block.material == 'minecraft:stone_pressure_plate':
                scale = Vec3(0.75, 0.1, 0.75)
            elif block.material == 'minecraft:stone_button':
                scale = Vec3(0.3, 0.2, 0.3)
            elif block.material == 'minecraft:redstone_torch':
                scale = Vec3(0.2, 0.5, 0.2)
            
            # Main block entity
            e = Entity(
                model='cube',
                color=col,
                position=(x, y, z),
                scale=scale,
                parent=parent_entity,
                collider='box'
            )
            
            # Add wireframe border (slightly larger)
            Entity(
                parent=e,
                model='wireframe_cube',
                color=color.black33,
                scale=1.02
            )
            
            entities.append(e)
            
        return entities
