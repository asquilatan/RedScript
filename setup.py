import os
import sys
from setuptools import setup, Extension

setup(
    name='redscript',
    version='0.1.0a1',
    author='Redstone HDL Contributors',
    description='A Minecraft Redstone HDL compiler',
    packages=['redscript', 'redscript.compiler', 'redscript.solver', 'redscript.viewer', 'redscript.cli', 'redscript.utils'],
    package_dir={'': 'src'},
    install_requires=[
        'lark>=1.1.0',
        'ursina>=5.0.0',
        'litemapy>=0.4.0',
        'numpy>=1.24.0',
    ],
    entry_points={
        'console_scripts': [
            'redscript=redscript.cli.main:main',
        ],
    },
    python_requires='>=3.11',
)
