"""
Block State Mapping: Material and property normalization
"""

class BlockStateMapper:
    """Maps RedScript block types to Minecraft block states"""
    
    # Material -> (block_name, required_properties)
    MATERIAL_MAP = {
        'minecraft:stone': ('stone', {}),
        'minecraft:piston': ('piston', {'facing': 'up'}),
        'minecraft:sticky_piston': ('sticky_piston', {'facing': 'up'}),
        'minecraft:redstone_wire': ('redstone_wire', {'power': '15'}),
        'minecraft:repeater': ('repeater', {'facing': 'north', 'delay': '1'}),
        'minecraft:redstone_block': ('redstone_block', {}),
        'minecraft:air': ('air', {}),
    }
    
    @staticmethod
    def normalize_material(material: str) -> str:
        """Normalize material name to Minecraft namespace"""
        if ':' not in material:
            return f'minecraft:{material}'
        return material
    
    @staticmethod
    def get_required_properties(material: str) -> dict:
        """Get required NBT properties for a material"""
        material = BlockStateMapper.normalize_material(material)
        _, props = BlockStateMapper.MATERIAL_MAP.get(
            material,
            ('stone', {})
        )
        return props.copy()
