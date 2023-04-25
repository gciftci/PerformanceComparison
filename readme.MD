# Performance Comparison of 2D Array Iteration Techniques in Python
<div align="center">

![Python](https://img.shields.io/badge/-Python-black?style=flat-square&=Python)![C++](https://img.shields.io/badge/-C++-00599C?style=flat-square&logo=c)![Docker](https://img.shields.io/badge/-Docker-black?style=flat-square&logo=docker)![GitHub](https://img.shields.io/badge/-GitHub-181717?style=flat-square&logo=github)![GitLab](https://img.shields.io/badge/-GitLab-FCA121?style=flat-square&logo=gitlab)
</div>
This repository contains my analysis and comparison of various techniques to iterate through a 2D NumPy array in Python. My goal is to determine the most performant method for my specific use case (AntSim), which involves filtering and modifying the original array based on certain conditions.


## Content
- [Performance Comparison of 2D Array Iteration Techniques in Python](#performance-comparison-of-2d-array-iteration-techniques-in-python)
  - [Content](#content)
  - [Problem](#problem)
  - [Testing Methodology](#testing-methodology)
    - [Project Tree](#project-tree)
    - [Hardware](#hardware)
    - [Testing Enviroment](#testing-enviroment)
      - [TimeIt](#timeit)
    - [Methods](#methods)
      - [1. Broadcasting](#1-broadcasting)
      - [2. todo...](#2-todo)
  - [Results](#results)
  - [Conclusions](#conclusions)
  - [Contact](#contact)

## Problem

The initial problem involves iterating through a 2D array of Perlin noise values with dimensions `2560x1440` (ROW x COL), and assigning the result to another 3D array, `grid_array`, based on the following filter and operation:

- Filter: The Perlin noise value at `start_array[x][y]` has to be > 0.
- Operation: Multiply the value by 255.
- insert that value into `end_array[x][y][0]`

The original code using nested loops:

```python
for x in range(0, GRID_ROW):
    for y in range(0, GRID_COL):
        res = 255 if result[x][y] < 0 else 0
        grid_array[x, y] = (res, 0, 0)
```

## Testing Methodology
### Project Tree
```
│   benchmark.py
├───methods
│   │   broadcasting_method.py
│   │   clip_method.py
│   │   dask_array_method.py
│   │   greater_multiply_method.py
│   │   heaviside_method.py
│   │   list_comprehension_method.py
│   │   maximum_method.py
│   │   nested_loop_method.py
│   │   numba_jit_method.py
│   │   pandas_applymap_method.py
│   │   parallel_method.py
│   │   piecewise_method.py
│   │   vectorize_method.py
│   │   where_method.py
├───src
│   │   utils.py
```
### Hardware
- CPU: AMD Ryzen 5 5600X 6-Core Processor
- GPU: AMD Radeon RX 6600
- SSD: Samsung SSD 980 PRO 500GB (465GB, SCSI)
- Memory: 32681MB (3600)
- Motherboard: ROG STRIX B550-I GAMING
- Windows Version: Microsoft Windows 10 Pro

### Testing Enviroment
The testing environment for benchmarking different methods is set up using the benchmark.py script. This script is designed to compare the runtime performance of various methods by running them on a set of input arrays and measuring their execution time using the timeit module.

#### TimeIt
The timeit module in Python is a powerful tool for measuring the execution time of code snippets. It provides a simple and accurate way to time small bits of Python code and can be used to compare the performance of different implementations. The timeit module internally takes care of various factors that can affect timing accuracy, such as garbage collection, and runs the code multiple times to obtain a reliable measurement.
```python
timeit.timeit(stmt='pass', setup='pass', timer=<default timer>, number=1000000, globals=None)
```

In my testing environment, the timeit module has been implemented in a modular fashion. This is achieved by organizing each method's implementation in separate files within the src/methods directory. 

**setup()**
The `setup()` function in the modules provides any required setup code as a string, which can be executed when setting up the test environment for benchmarking purposes. In this particular case, the setup function returns an empty string because there is no additional setup required.

```python
# src/methods/XXX_method.py
(function) def setup() -> str
Set up code for broadcasting method.

Returns:
    str: Setup code as a string.
``` 
The `process()` function in the module contains the actual implementation of the method. It accepts a 2D array `start_array` of Perlin noise values and a 3D array `end_array` to store the processed values. The function multiplies the `start_array` by 255, and then assigns the resulting array to the first channel (channel 0) of the `end_array`. The updated `end_array` is returned as the output.

**process()**
```python
Iterate through the start_array using broadcasting and apply filter and operation.
(function) def process(
    start_array: ndarray,
    end_array: ndarray
) -> ndarray

Args:
    start_array (ndarray): The 2D array of Perlin noise values.
    end_array (ndarray): The 3D array to store the processed values.

Returns:
    ndarray: The updated end_array with processed values.
```
**Using the Broadcasting Method in my Project**
To use the `broadcasting` method, import the `broadcasting_method` module and call the `process` function with the appropriate input arguments. If you want to benchmark the performance of the function, you can use the *timeit* library by invoking the *setup* function and passing its output to the Timer object, along with the `process` function call.

 This modular structure allows the benchmark.py script to import and execute each method independently.

```python
Import available methods from the src/methods directory.
(function) def create_methods_list() -> dict

Returns:
    dict: A dictionary of available methods.
```

To utilize timeit for benchmarking, the benchmark function in the benchmark.py script takes the setup and process functions as arguments, along with the input arrays start_array and end_array. The setup function is called to get the setup code, and a new timeit.Timer object is created using the process function as the target code, the setup code, and a namespace dictionary containing the necessary variables for the benchmarking environment.

```python
Run a benchmark on the given process function in a isolated timeit enviroment.

(function) def benchmark(
    setup: () -> str,
    process: (ndarray, ndarray) -> ndarray,
    start_array: ndarray,
    end_array: ndarray
) -> Tuple[float, float]

Args:
    setup (Callable[[], str]): A function that returns the setup code as a string.
    process (Callable[[ndarray, ndarray], ndarray]): The process function to benchmark.
    start_array (ndarray): The 2D array of Perlin noise values.
    end_array (ndarray): The 3D array to store the processed values.

Returns:
    Tuple[float, float]: A tuple containing the total elapsed time and average time per trial.
```

The benchmark.py script reads the implementation details of each method from separate files located in the src/methods directory. These files should contain a setup function that returns the setup code as a string, and a process function containing the actual method implementation. By organizing the methods in this manner, the script can easily import and execute them in a modular fashion.

When the script is executed, it automatically imports and benchmarks all methods defined in the src/methods directory. The benchmark results are then displayed in a table, sorted by speed, and include the average time and total elapsed time for each method. Additionally, the script includes a profiling option for in-depth analysis of each method's performance.

Before running the actual benchmark, the script allows for an optional warmup phase, where the code is executed a few times to populate caches and other system resources. Then, the timeit function is called with the specified number of trials, and the elapsed time is recorded. If the DEBUG flag is set, additional profiling information is collected using the cProfile module.

By structuring the benchmarking process in this manner, the testing environment enables easy comparison of different methods' performance. Everything in `setup()` will be excluded from the benchmark timing. To add or remove a method for benchmarking, you can simply modify the contents of the src/methods directory without needing to change the main `benchmark.py` script. This modular approach allows for better maintainability and scalability of the testing environment.

In summary, the testing environment is designed to provide a structured and modular approach to benchmarking different methods for processing 2D arrays. It utilizes the timeit module for accurate timing measurements and allows for easy comparison of different methods by simply adding or removing method files in the src/methods directory.
### Methods
Used methods:
* Broadcasting
* Maximum
* Clip
* Where
* GreaterMultiply
* Piecewise
* Heaviside
* NumbaJit
* DaskArray
* Vectorize
* PandasApplymap
* Parallel
* ListComprehension
* NestedLoop          
#### 1. Broadcasting
The broadcasting method is a technique for processing 2D arrays. It leverages NumPy's array broadcasting capabilities to efficiently perform operations on the input array without requiring any explicit loops. The module broadcasting_method.py contains the implementation for this method and can be easily integrated into your project.

10 function calls in 0.004 seconds
|ncalls     | tottime | percall | cumtime | percall |  filename:lineno(function)    |
|-----------|---------|---------|---------|---------|-------------------------------|
| 1         | 0.000   | 0.000   | 0.004   | 0.004   | timeit.py:164(timeit) |
| 1         | 0.000   | 0.000   | 0.004   | 0.004   | <timeit-src>:2(inner) |
| 1         | 0.000   | 0.000   | 0.004   | 0.004   | benchmark.py:92(<lambda>) |
| 1         | 0.003   | 0.003   | 0.003   | 0.003   | broadcasting_method.py:50(process) |
| 1         | 0.000   | 0.000   | 0.000   | 0.000   | {method 'disable' of '_lsprof.Profiler' objects} |
| 2         | 0.000   | 0.000   | 0.000   | 0.000   | {built-in method time.perf_counter} |
| 1         | 0.000   | 0.000   | 0.000   | 0.000   | {built-in method gc.isenabled} |
| 1         | 0.000   | 0.000   | 0.000   | 0.000   | {built-in method gc.enable} |
| 1         | 0.000   | 0.000   | 0.000   | 0.000   | {built-in method gc.disable} |

```python
Iterate through the start_array using broadcasting and apply filter and operation.

Args:
    start_array (ndarray): The 2D array of Perlin noise values.
    end_array (ndarray): The 3D array to store the processed values.

Returns:
    ndarray: The updated end_array with processed values.
```
#### 2. todo...
## Results

The results of the benchmark are as follows (1000 runs):

| Method |	Average Time (ms ) |	Total Time (s)      |
| :-------|---------------------:|----------------:|
| Broadcasting Method |	3.6809 |	0.37              |
| Maximum Method |	6.9120 |	0.69                   |
| Clip Method |	6.9197 |	0.69                      |
| Where Method |	7.6250 |	0.76                     |
| Greater Multiply Method |	8.1428 |	0.81          |
| Piecewise Method |	14.4530 |	1.45                |
| Heaviside Method |	16.6420 |	1.66                |
| Numba JIT  Method	| 82.0743| 	8.21                |
| Dask Array  Method| 	83.6481| 	8.36               |
| Vectorize Method |	348.5773 |	34.86              |
| Pandas Applymap  Method| 	701.1184| 	70.11        |
| Parallel Method |	1162.5675 |	116.26             |
| List Comprehension  Method| 	5606.1462| 	560.61   |
| Nested Loop  Method| 	8532.1720| 	853.22          |

## Conclusions

Based on the test results, the most performant method for this specific use case is `broadcast` or basically any `numpy low-level array manipulation`. It's important to note that the performance of these methods may vary depending on the size of the dataset and the complexity of the operations. Make sure to test these methods on your specific use case to determine which one is most suitable for your needs. 

Please refer to the [main script](./main.py) to see the actual code and performance testing setup.

## Contact

Feel free to contact me! <div align="right">

    
[![Linkedin Badge](https://img.shields.io/badge/-gciftci-blue?style=flat-square&logo=Linkedin&logoColor=white&link=https://ch.linkedin.com/in/garbis-ciftci/)](https://https://ch.linkedin.com/in/garbis-ciftci/)[![Instagram Badge](https://img.shields.io/badge/-garbis.ci-purple?style=flat-square&logo=instagram&logoColor=white&link=https://www.instagram.com/garbis.ci/)](https://www.instagram.com/garbis.ci/)[![Gmail Badge](https://img.shields.io/badge/-garbis.ciftci@gmail.com-c14438?style=flat-square&logo=Gmail&logoColor=white&link=mailto:garbis.ciftci@gmail.com)](mailto:garbis.ciftci@gmail.com)
    
</div>


