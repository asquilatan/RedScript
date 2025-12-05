#!/usr/bin/env python3
"""
RedScript Compiler CLI
"""
import argparse
import sys
from pathlib import Path

def main():
    parser = argparse.ArgumentParser(
        description="RedScript Compiler - Translate kinematic intent to Minecraft schematics"
    )
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # Compile command
    compile_parser = subparsers.add_parser('compile', help='Compile RedScript to schematic')
    compile_parser.add_argument('input', type=str, help='Input .rs file')
    compile_parser.add_argument('--output', '-o', type=str, help='Output .litematic file')
    compile_parser.add_argument('--optimize', action='store_true', help='Enable optimization')
    
    # View command
    view_parser = subparsers.add_parser('view', help='Launch 3D viewer')
    view_parser.add_argument('schematic', type=str, help='Schematic file to view')
    
    args = parser.parse_args()
    
    if args.command == 'compile':
        from redscript.compiler import compile_file
        try:
            compile_file(args.input, args.output, optimize=args.optimize)
            print(f"✓ Compiled to {args.output}")
        except Exception as e:
            print(f"✗ Compilation failed: {e}", file=sys.stderr)
            sys.exit(1)
    
    elif args.command == 'view':
        from redscript.viewer import launch_viewer
        try:
            launch_viewer(args.schematic)
        except Exception as e:
            print(f"✗ Viewer failed: {e}", file=sys.stderr)
            sys.exit(1)
    
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
