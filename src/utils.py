# src/utils.py
"""
utils.py: A module containing utility functions for processing 2D arrays.

This module contains two functions: `create_base_arrays` and `create_methods_list`.
`create_base_arrays` is used to create the initial 2D and 3D arrays for processing, while
`create_methods_list` is used to import and return a dictionary of available methods from the
`src/methods` directory.

To use this module in your project, simply import it and call the appropriate function(s) as
needed.

Example usage:

    from src.utils import create_base_arrays, create_methods_list

    # Create the initial 2D and 3D arrays for processing
    start_array, end_array = create_base_arrays(GRID_ROW, GRID_COL)

    # Import available methods from the src/methods directory
    methods = create_methods_list()
"""
import pyfastnoisesimd as fastns
from numpy import zeros, uint8
from os import listdir
from importlib import import_module

# pyfastnoisesimd
OCTAVES = 25
SEED = 1337
fn = fastns.Noise(seed=SEED)
fn.fractal.octaves = OCTAVES
fn.noiseType = fastns.NoiseType.Perlin


def create_base_arrays(GRID_ROW: int, GRID_COL: int) -> tuple:
    """
    Create the initial 2D and 3D arrays for processing.

    Args:
        GRID_ROW (int): The number of rows in the 2D array.
        GRID_COL (int): The number of columns in the 2D array.

    Returns:
        tuple: A tuple containing the start and end arrays for processing.
    """
    start_array = fn.genAsGrid([GRID_ROW, GRID_COL])
    end_array = zeros((GRID_ROW, GRID_COL, 3), dtype=uint8)
    return start_array, end_array


def create_methods_list() -> dict:
    """
    Import available methods from the src/methods directory.

    Returns:
        dict: A dictionary of available methods.
    """
    methods = {}
    method_files = [f[:-3] for f in listdir('src/methods')
                    if f.endswith('.py') and f != '__init__.py']
    for method_file in method_files:
        module = import_module(f'src.methods.{method_file}')
        methods[method_file] = module
    return methods
