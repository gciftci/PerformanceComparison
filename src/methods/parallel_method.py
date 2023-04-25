# src/methods/parallel_method.py
"""
parallel_method.py: A module that implements the parallel method for processing 2D arrays.

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

    from src.methods import parallel_method

    start_array = ...  # Your 2D input array
    end_array = ...    # Your 3D output array

    # Process the input array using the parallel method
    processed_array = parallel_method.process(start_array, end_array)

    # Benchmark the performance of the parallel method (timeit)
    timer = Timer(lambda: process(start_array, end_array), setup=setup_code, globals={**_NS})

Note: The `process` function in this module benefits from parallel processing using the Joblib
library, which can leverage multiple CPU cores to speed up the computation.
"""
from numpy import array
from joblib import Parallel, delayed
from multiprocessing import cpu_count
n_jobs = cpu_count()


def process_cell(value):
    return (int(255 * value) if value > 0 else 0, 0, 0)


def process_row(row):
    return array([process_cell(value) for value in row], dtype='int32')


def setup() -> str:
    """
    Set up code for parallel method.

    Returns:
        str: Setup code as a string.
    """
    return '''
from numpy import array
from joblib import Parallel, delayed
from multiprocessing import cpu_count
n_jobs = cpu_count()
def process_cell(value):
    return (int(255 * value) if value > 0 else 0, 0, 0)

def process_row(row):
    return array([process_cell(value) for value in row], dtype='int32')
'''


def process(start_array: array, end_array: array) -> array:
    """
    Iterate through the start_array using parallel processing and apply filter and operation.

    Args:
        start_array (ndarray): The 2D array of Perlin noise values (from -1.00 to 1.00).
        end_array (ndarray): The 2D array to store the processed values.

    Returns:
        ndarray: The updated end_array with processed values.

    Time complexity: O(n*m) where n and m are the dimensions of the array.
    Benefits: Can potentially speed up the computation by leveraging multiple CPU cores for
    parallel processing.
    """
    new_end_array = Parallel(n_jobs=n_jobs)(
        delayed(process_row)(row) for row in start_array
    )
    end_array_res = array(new_end_array, dtype='int32')
    return end_array_res


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
