# src\methods\clip_method.py
"""
clip_method.py: A module that implements the clipping method for processing 2D arrays.

This module contains three functions: `setup`, `process`, and `run`. The `setup` function is used
to provide any required setup code as a string, while the `process` function contains the actual
implementation of the method. The `run` function is a helper that can be called with the provided
`setup_code` to set up the test environment and execute the `process` function.

The structure of this module allows it to be easily integrated into a larger project as a standalone
module, with the added benefit of being able to benchmark the `process` function without the need
for any additional modifications. This is achieved by separating the setup, processing, and
validation steps into different functions, making it easier to manage and maintain the code.

To use this module in your project, simply import it and call the `process` function with the
appropriate input arguments. If you want to benchmark the performance of the function, you can
do so by invoking setup and process call on timeit.

Example usage:

    from src.methods import clip_method

    start_array = ...  # Your 2D input array
    end_array = ...    # Your 3D output array

    # Process the input array using the clipping method
    processed_array = clip_method.process(start_array, end_array)

    # Benchmark the performance of the clipping method (timeit)
    timer = Timer(lambda: process(start_array, end_array), setup=setup_code, globals={**_NS})

Note: The `process` function in this module benefits from the efficiency of NumPy's array
broadcasting, as it does not require any explicit loops to perform the required operations on
the input array.
"""

from numpy import clip, ndarray


def setup() -> str:
    """
    Set up code for clipping method.

    Returns:
        str: Setup code as a string.
    """
    return '''from numpy import clip
    '''


def process(start_array: ndarray, end_array: ndarray) -> ndarray:
    """
    Iterate through the start_array using broadcasting and apply filter and operation.

    Args:
        start_array (ndarray): The 2D array of Perlin noise values.
        end_array (ndarray): The 3D array to store the processed values.

    Returns:
        ndarray: The updated end_array with processed values.

    Benefits: Can be more efficient due to the use of NumPy's array broadcasting; no explicit loops
    required.
    """
    end_array[:, :, 0] = clip(start_array, 0, None) * 255
    return end_array


def run(setup_code: str) -> None:
    """
    Run the process function with the provided setup code.

    Args:
        setup_code (str): The code to set up the test environment.
    """
    exec(setup_code)

    start_array = ...
    end_array = ...
    return process(start_array, end_array)


if __name__ == "__main__":
    run(setup())
