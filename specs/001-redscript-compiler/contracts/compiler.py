from typing import List, Optional
from dataclasses import dataclass

@dataclass
class CompileOptions:
    optimize: bool = True
    export_format: str = "litematic"

class Compiler:
    """
    Main entry point for the RedScript compiler.
    """
    
    def compile(self, source_code: str, options: CompileOptions) -> 'Schematic':
        """
        Compiles RedScript source code into a Minecraft Schematic.
        
        Args:
            source_code: The raw string content of the .rs file.
            options: Compilation settings.
            
        Returns:
            A Schematic object containing the voxel data.
            
        Raises:
            SyntaxError: If the source code is invalid.
            RoutingError: If physical paths cannot be resolved.
            TimingError: If synchronization constraints cannot be met.
        """
        pass

class Schematic:
    """
    Represents the compiled 3D structure.
    """
    
    def save(self, path: str) -> None:
        """Writes the schematic to disk."""
        pass
        
    def to_voxel_grid(self) -> 'Grid':
        """Converts to internal grid format for the viewer."""
        pass
