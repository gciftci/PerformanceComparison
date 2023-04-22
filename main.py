from timeit import timeit
import pyfastnoisesimd as fns
from numpy import array, zeros, where, vectorize,  sort, uint8
import numba
from joblib import Parallel, delayed
from datetime import datetime
import cProfile
pr = cProfile.Profile()
pr.enable()

# General Settings
GRID_ROW = 2560
GRID_COL = 1440
WARMUP_RUNS = 10
COUNTING_RUNS = 10

# Perlin Config
oct = 50
seed = 1337

# pyfastnoisesimd
fastnoise = fns.Noise(seed=seed)
fastnoise.fractal.octaves = oct
fastnoise.noiseType = fns.NoiseType.Perlin

# Generate data
result = fastnoise.genAsGrid([GRID_ROW, GRID_COL])
grid_array = zeros((GRID_ROW, GRID_COL, 3), dtype=uint8)
grid_array_trash = zeros((GRID_ROW, GRID_COL, 3), dtype=uint8)


def original_method(result):
    """1. Original Method
    Iterate through the result array using nested loops and apply filter and operation.

    Args:
        result (ndarray): The 2D array of Perlin noise values.
        grid_array (ndarray): The 2D array to store the processed values.

    Returns:
        ndarray: The updated grid_array with processed values.

    Time complexity: O(n*m) where n and m are the dimensions of the array.
    Benefits: Easy to understand and implement; no additional library required.

    """
    for x in range(GRID_ROW):
        for y in range(GRID_COL):
            res = 255 if result[x][y] > 0 else 0
            grid_array_trash[x, y] = (res, 0, 0)
    return grid_array_trash


def where_method(result):
    """2. where Method
    Iterate through the result array using where and apply filter and operation.

    Args:
        result (ndarray): The 2D array of Perlin noise values.
        grid_array (ndarray): The 2D array to store the processed values.

    Returns:
        ndarray: The updated grid_array with processed values.

    Time complexity: O(n*m) where n and m are the dimensions of the array.
    Benefits: More efficient than nested loops due to the use of NumPy's optimized functions.
    """
    res_array = where(result > 0, 255, 0)
    grid_array_trash[:, :, 0] = res_array
    return grid_array_trash


def vectorize_method(result):
    """3. vectorize Method
    Iterate through the result array using vectorize and apply filter and operation.

    Args:
        result (ndarray): The 2D array of Perlin noise values.
        grid_array (ndarray): The 2D array to store the processed values.

    Returns:
        ndarray: The updated grid_array with processed values.

    Time complexity: O(n*m) where n and m are the dimensions of the array.
    Benefits: Can be more concise and easier to read than nested loops.
    """
    def custom_function(value):
        return 255 if value > 0 else 0

    vectorized_function = vectorize(custom_function)
    res_array = vectorized_function(result)
    grid_array_trash[:, :, 0] = res_array
    return grid_array_trash


def broadcasting_method(result):
    """4. Broadcasting Method
    Iterate through the result array using broadcasting and apply filter and operation.

    Args:
        result (ndarray): The 2D array of Perlin noise values.
        grid_array (ndarray): The 2D array to store the processed values.

    Returns:
        ndarray: The updated grid_array with processed values.

    Time complexity: O(n*m) where n and m are the dimensions of the array.
    Benefits: Can be more efficient due to the use of NumPy's array broadcasting; no explicit loops
    required.

    """
    grid_array_trash[:, :, 0] = (result > 0) * 255
    return grid_array_trash


def list_comprehension_method(result):
    """5. List Comprehension Method
    Iterate through the result array using list comprehension and apply filter and operation.

    Args:
        result (ndarray): The 2D array of Perlin noise values.
        grid_array (ndarray): The 2D array to store the processed values.

    Returns:
        ndarray: The updated grid_array with processed values.

    Time complexity: O(n*m) where n and m are the dimensions of the array.
    Benefits: Can be more concise and faster than nested loops, while still using pure Python.
    """
    grid_array_list = [
        [(255 if value > 0 else 0, 0, 0) for value in row] for row in result
    ]
    grid_array_trash = array(grid_array_list)
    return grid_array_trash


@numba.jit(nopython=True, parallel=True)
def numba_jit_method(result):
    """6. Numba JIT Method
    Iterate through the result array using Numba's Just-In-Time (JIT) compiler and apply filter and
    operation.

    Args:
        result (ndarray): The 2D array of Perlin noise values.
        grid_array (ndarray): The 2D array to store the processed values.

    Returns:
        ndarray: The updated grid_array with processed values.

    Time complexity: O(n*m) where n and m are the dimensions of the array.
    Benefits: Can significantly speed up the computation by compiling the code to machine
    instructions.
    """
    grid_array_trash = zeros((GRID_ROW, GRID_COL, 3), dtype=uint8)
    for x in range(result.shape[0]):
        for y in range(result.shape[1]):
            res = 255 if result[x][y] < 0 else 0
            grid_array_trash[x, y] = (res, 0, 0)
    return grid_array_trash


def parallel_method(result):
    """7. Parallel Method
    Iterate through the result array using parallel processing and apply filter and operation.

    Args:
        result (ndarray): The 2D array of Perlin noise values.
        grid_array (ndarray): The 2D array to store the processed values.

    Returns:
        ndarray: The updated grid_array with processed values.

    Time complexity: O(n*m) where n and m are the dimensions of the array.
    Benefits: Can potentially speed up the computation by leveraging multiple CPU cores for
    parallel processing.
    """

    def process_cell(value):
        return (255 if value > 0 else 0, 0, 0)

    grid_array_trash = Parallel(n_jobs=-1)(
        delayed(process_cell)(value) for row in result for value in row
    )
    return array(grid_array_trash).reshape(GRID_ROW, GRID_COL, 3)


# All our methods to check
methods = [
    (1, "Original Method", original_method),
    (2, "where Method", where_method),
    (3, "vectorize Method", vectorize_method),
    (4, "Broadcasting Method", broadcasting_method),
    (5, "List Comprehension Method", list_comprehension_method),
    (6, "Numba JIT Method", numba_jit_method),
    (7, "Parallel Method", parallel_method),
]
dtype_list = [('duration', float), ('name', '<U18')]

# Timer code

print(f"Configuration: Running [{len(methods)}] Methods [{COUNTING_RUNS}] times.\
      (Arraysize: [{GRID_ROW}x{GRID_COL}])")
print("Benchmark started...")

[(numba_jit_method(result), print(f' Warming "numba_jit_method" up ([{WARMUP_RUNS}] cycles)'))
 for _ in range(WARMUP_RUNS) if WARMUP_RUNS > 0]

ordered_methods = []
# Method-Start
for number, name, method in methods:
    duration = timeit(
        # stmt='''pr.run('method(result)')''',
        stmt='''method(result)''',
        setup="from __main__ import method, name, result, pr, datetime",
        number=COUNTING_RUNS)
    ordered_methods.append([(duration / COUNTING_RUNS), name])

pr.dump_stats(f'logs/profiler-{datetime.now().strftime("%H_%M_%S")}.pstats')
# pr.print_stats()
new_order = array([tuple(x) for x in ordered_methods], dtype=dtype_list)
sorted_data = sort(new_order, order=['duration'])
[print('{:5}> {:3d}{:40s} {:10} {:.4f}s'.format("-"*5, i+1, val[1], " ", val[0])) for i, val in
    enumerate(sorted_data)]
