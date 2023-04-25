# benchmark.py
"""
benchmark.py: A benchmarking script for comparing the runtime performance of different methods
for processing 2D arrays.

This script implements a benchmarking framework for comparing the runtime performance of different
methods for processing 2D arrays of Perlin noise values. The script reads the implementation details
of each method from separate files in the 'src/methods' directory, and uses the timeit module to
run each method on a set of input arrays.

The benchmark results are displayed in a table, sorted by speed, and include the average time and
total elapsed time for each method. The script also includes a profiling option for in-depth
analysis of each method's performance.

To run the benchmark, simply execute script from the command line. The script will automatically
import and execute all methods defined in the 'src/methods' directory.

Example usage:

    $ python benchmark.py

ROADMAP:
- More detailed documentation to the module and function docstrings, including information about
  the input and output parameters, any limitations, assumptions, or prerequisites, and examples of
  usage.
- Handle log information by using a logging library. Log information about the benchmarking process,
  such as the elapsed time, method name, and any errors or exceptions.
- Add some sort of validation system  to verify that the output of the processing function is
  correct and matches the expected results.
- Add command-line interface which would allow to specify input parameters, such as size of the
  input arrays, the number of trials, and the benchmark method to use.
"""

# Modules
from typing import Callable, Dict, Tuple
from numpy import ndarray
from timeit import Timer
import cProfile
import src.utils as utils

profiler = cProfile.Profile()

# Settings
DEBUG = False

# constants
SIZE = (2560, 1440)

NUM_TRIALS = 1000
NUM_WARMUP = 1

# Test-Case [x=20, y=70] => end_array[x,y][0]  = start_array[x, y] * 255
#   = 0.2807 * 255 = 71
TEST_VALUE = (20, 70)

# -> dict of methods in folder
methods = utils.create_methods_list()

# -> tuple[ndarray, NDArray[uint8]] of base-arrays
start_array, end_array = utils.create_base_arrays(SIZE[0], SIZE[1])


def benchmark(setup: Callable[[], str],
              process: Callable[[ndarray, ndarray], ndarray],
              start_array: ndarray,
              end_array: ndarray) -> Tuple[float, float]:
    """
    Run a benchmark on the given process function in a isolated timeit enviroment.

    Args:
        setup (Callable[[], str]): A function that returns the setup code as a string.
        process (Callable[[ndarray, ndarray], ndarray]): The process function to benchmark.
        start_array (ndarray): The 2D array of Perlin noise values.
        end_array (ndarray): The 3D array to store the processed values.

    Returns:
        Tuple[float, float]: A tuple containing the total elapsed time and average time per trial.
    """

    # Retrieve the setup_code defined in the method-file.
    setup_code = setup()

    # Declare a Namespace for the timeit-environment with basic information
    _NS = {
        "start_array": start_array.copy(),
        "end_array": end_array.copy(),
        "GRID_ROW": SIZE[0],
        "GRID_COL": SIZE[1]
    }

    # Set benchmark on the method
    timer = Timer(lambda: process(start_array, end_array), setup=setup_code, globals={**_NS})

    # Run a few empty calls - if configured - so that cache is ready
    if NUM_WARMUP > 0:
        [timer.timeit(number=NUM_WARMUP) for _ in range(NUM_WARMUP)]

    if DEBUG:
        profiler = cProfile.Profile()
        profiler.enable()

    # Run the code to be profiled
    elapsed_time = timer.timeit(number=NUM_TRIALS)

    if DEBUG:
        profiler.disable()
        profiler.print_stats(sort="cumulative")

    return elapsed_time, elapsed_time / NUM_TRIALS * 1000


def display_results(methods: Dict[str, Dict[str, str]]) -> None:
    """
    Display a table with method names and their runtime performance, sorted by speed.

    Args:
        methods (Dict[str, Dict[str, str]]): A dictionary containing method names and their setup
        and process code.
    """
    separator = "-" * 100
    header = f'{SIZE[0]}x{SIZE[1]} | Runs: {NUM_TRIALS}'

    print(f"{separator}")
    print(f"{'-> Benchmark started':<40}{header:>60}")
    print(f"{separator}")

    results = []
    overall = 0
    for method_name, module in methods.items():
        total_time, avg_time = benchmark(module.setup, module.process, start_array, end_array)
        results.append((method_name, avg_time, total_time))
        overall += total_time

    # Sort the results by average time
    sorted_results = sorted(results, key=lambda x: x[1])

    # Print the sorted results
    for method_name, avg_time, total_time in sorted_results:
        print(f'{method_name:<50}{avg_time:>35.4f} ms{total_time:>10.2f} s')

    print(f"{separator}")
    print(f"{'Total Runtime: ':<50}{overall:>48.2f} s")
    print(f"{separator}")


def main() -> None:
    """
    Main function that displays benchmark results for various methods.
    """
    display_results(methods)


if __name__ == "__main__":
    main()
