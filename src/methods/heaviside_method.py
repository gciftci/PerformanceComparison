# src/methods/heaviside_method.py
"""
heaviside_method.py: A module that implements the Heaviside-method for processing 2D arrays.

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

    from src.methods import heaviside_method

    start_array = ...  # Your 2D input array
    end_array = ...    # Your 3D output array

    # Process the input array using the Heaviside function method
    processed_array = heaviside_method.process(start_array, end_array)

    # Benchmark the performance of the Heaviside function method (timeit)
    timer = Timer(lambda: process(start_array, end_array), setup=setup_code, globals={**_NS})

Note: The `process` function in this module applies the Heaviside function to the input array and
multiplies the result with the input array, before scaling the result to the appropriate range.
"""

from numpy import heaviside, ndarray


def setup() -> str:
    """
    Set up code for the Heaviside function method.

    Returns:
        str: Setup code as a string.
    """
    return '''
from numpy import heaviside
'''


def process(start_array: ndarray, end_array: ndarray) -> ndarray:
    """
    Apply the Heaviside function to the input array and multiply the result with the input array.

    Args:
        start_array (ndarray): The 2D array of input values.
        end_array (ndarray): The 3D array to store the processed values.

    Returns:
        ndarray: The updated end_array with processed values.

    Benefits: Uses the efficient NumPy `heaviside` function to apply the Heaviside function to the
    input array and avoids the need for explicit loops.
    """
    end_array[:, :, 0] = heaviside(start_array, 0) * start_array * 255
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
