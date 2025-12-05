"""
Error Reporting: Comprehensive error handling and diagnostics
"""
from enum import Enum
from typing import List, Optional
from dataclasses import dataclass


class ErrorType(Enum):
    """Classification of compilation errors"""
    SYNTAX_ERROR = "syntax_error"           # Invalid RedScript syntax
    ROUTING_FAILED = "routing_failed"        # Cannot route signal between components
    TIMING_VIOLATION = "timing_violation"    # Timing requirements cannot be met
    PHYSICS_VIOLATION = "physics_violation"  # Violates Minecraft physics (QC, BUD, etc.)
    SAFETY_VIOLATION = "safety_violation"    # Violates kinematic safety constraints
    IO_ERROR = "io_error"                    # File read/write problems


@dataclass
class CompileError:
    """Single compilation error with context"""
    error_type: ErrorType
    message: str
    file_path: Optional[str] = None
    line_number: Optional[int] = None
    column_number: Optional[int] = None
    context: Optional[str] = None
    suggestion: Optional[str] = None
    
    def format(self) -> str:
        """Format error for console display"""
        result = f"[{self.error_type.value.upper()}] {self.message}"
        
        if self.file_path:
            result += f"\n  File: {self.file_path}"
        
        if self.line_number is not None:
            result += f":{self.line_number}"
            if self.column_number is not None:
                result += f":{self.column_number}"
        
        if self.context:
            result += f"\n  > {self.context}"
        
        if self.suggestion:
            result += f"\n  💡 Suggestion: {self.suggestion}"
        
        return result


class ErrorReporter:
    """Collects and reports compilation errors"""
    
    def __init__(self, strict_mode: bool = False):
        self.errors: List[CompileError] = []
        self.warnings: List[CompileError] = []
        self.strict_mode = strict_mode
    
    def add_error(self, error: CompileError) -> None:
        """Add error to report"""
        self.errors.append(error)
    
    def add_warning(self, error: CompileError) -> None:
        """Add warning to report"""
        self.warnings.append(error)
    
    def has_errors(self) -> bool:
        """Check if any errors occurred"""
        return len(self.errors) > 0 or (self.strict_mode and len(self.warnings) > 0)
    
    def format_report(self) -> str:
        """Format all errors and warnings for display"""
        lines = []
        
        if self.errors:
            lines.append(f"\n❌ ERRORS ({len(self.errors)}):")
            for error in self.errors:
                lines.append(error.format())
        
        if self.warnings:
            lines.append(f"\n⚠️  WARNINGS ({len(self.warnings)}):")
            for warning in self.warnings:
                lines.append(warning.format())
        
        if not self.errors and not self.warnings:
            lines.append("\n✅ Compilation successful!")
        
        return "\n".join(lines)
