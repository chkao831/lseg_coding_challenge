# LSEG Coding Challenge
Feb 6, 2023 by Carolyn Kao (chkao831@stanford.edu)

## Problem Description
This program runs lightshows, demonstrated on a squared grid with default size of 1000x1000. Customers provide instructions on how they want the lights to be turned on during the event.

The program contains two parts. 
- The first part (the '**System 1**') involves operations that switch on/off the lights and invert the lights, and would calculate how many lights are on at the end. 
- The second part (the '**System 2**') is an upgraded version of **System 1**. The lights in **System 2** have individual brightness levels, with a brightness level of 0 or higher. It would then calculates the sum of lights state (i.e. the brightness) at the end. 

All lights start turned off for both systems. 

## Input format
The sequence of instructions are written line-by-line in a text file. Each line of instruction identifies inclusive ranges of coordinates, forming the opposite corners of a rectangle. 

As an example, for a 1000x1000 grid, the corners are at `(0,0)`, `(999,0)`, `(0,999)` and `(999,999)`. An instruction `(0,0) through (2,2)` refers to the 9 lights in a 3x3 grid in the bottom left corner. 

Sample commands from a text file:
```
turn on 0,0 through 999,999
turn off 499,499 through 500,500
toggle 0,499 through 999,500
```

Please ensure that the value of each coordinate pair should fall between `0` and `grid_size-1` (by default, 999), inclusive. Otherwise, by the error handling mechanism, values out of such range would be detected as invalid. 

## Setup
```bat
$ cd lseg_coding_challenge
$ pip install -r requirements.txt
```

- Requirements
  * numpy>=1.24.1
  * pytest>=7.2.1 
  * python>=3.10.9

## Usage
Please be noted that all input files should be **in the format of .txt**, and **should be put under the folder** `lseg_coding_challenge/data/` for the program to function properly. 

```py
usage: python3 -m src.main [-h] [--system {1,2}] [--grid GRID] input
```
```bat
positional arguments:
  input           The input data file name (.txt) under /data folder.

options:
  -h, --help      show this help message and exit
  --system {1,2}  Optional. Selection from system 1 or 2 (upgraded). 
                  Default: 1.
  --grid GRID     Optional. The side length of the grid. 
                  Default: 1000.
```

For example, to run the program with an input file called `sample_input.txt` (for **System 1** by default), 
```bat
$ cd lseg_coding_challenge
$ python3 -m src.main sample_input.txt
```
The output would then be printed to the console such as the following, \
`INFO: 2023-02-06 03:42:24:  [System 1] The final brightness is 998004.`

To run the same file for **System 2**,
```bat
$ python3 -m src.main sample_input.txt  --system 2
```
which yields an output of `INFO: 2023-02-06 03:44:18:  [System 2] The final brightness is 1003996.`


As illustrated in the usage, I designed an additional, optional argument `--grid` for better flexibility given a squared grid with size length other than 1000. However, when specifying this argument, please be noted that the coordinates' value in the input data file could not exceed `[0,grid_size)` to avoid ValueError.

## Test
```bat
$ cd lseg_coding_challenge
$ python3 -m pytest -v
```
The `-v` flag is optional. It controls the verbosity of pytest output in various aspects: test session progress, assertion details when tests fail, fixtures details, etc. For shorter console output, simply ignore the flag.

Upon the end of the test, the result is ideally shown as follows,
```py
=========================== test session starts ===========================

collected 10 items

src/test/test_main.py::TestMain::test_io_parsing PASSED                   [ 10%]
src/test/test_main.py::TestMain::test_assign_value PASSED                 [ 20%]
src/test/test_main.py::TestMain::test_matrix_binary_conversion PASSED     [ 30%]
src/test/test_main.py::TestMain::test_matrix_addition PASSED              [ 40%]
src/test/test_main.py::TestMain::test_upgraded_turn_off PASSED            [ 50%]
src/test/test_main.py::TestMain::test_sample_sys1_end_to_end PASSED       [ 60%]
src/test/test_main.py::TestMain::test_sample_sys2_end_to_end PASSED       [ 70%]
src/test/test_main.py::TestMain::test_turn_input_exception PASSED         [ 80%]
src/test/test_main.py::TestMain::test_toggle_input_exception PASSED       [ 90%]
src/test/test_main.py::TestMain::test_out_of_range_input_exception PASSED [100%]

=========================== 10 passed in 0.15s ===========================
```

## Technical Notes
### Structure Design
```python3
lseg_coding_challenge/
    data/
    src/
        py_lib/
            __init__.py
            io.py
            lightshow.py
            lightshow_upgraded.py
        test/
            __init__.py
            test_main.py
            test_data/
        __init__.py
        main.py
    README.md
    requirements.txt
```
`main` runs the main pipeline, which calls `io` and then `lightshow` or `lightshow_upgraded` in order. 

I utilize `__init__.py` to mark directories as Python package directories. This is for a relatively robust import between modules under the `src` folder. 

For example, under `main.py`, I do 
```python3
from .py_lib.io import IOProcessor
```
With an (usually) empty file `__init__.py`, Python would look for submodules inside the directory in its attempt of module import. 

### Object-oriented Design
The `LightShowUpgraded` class inherits the `LightShow` class. 

This is because when I designed the `LightShow` class, I spotted some interchangeable properties between the two. Since the `LightShowUpgraded` refers to an upgraded version of the `LightShow` class, naturally I would think of the possibilities of having the third, fourth shows which may also be extended/upgraded from the **System 1**. 

With inheritance, the mutual properties may be reused whenever possible and the redundancy is reduced. For different operations between different shows, I simply overrode them in the child class with customization.

In addition, another noteworthy advantage of such design is that OOP allows me to write a more organized interface, as illustrated in `main`. Since those two lightshow classes share mutual properties upon their initializations and function calls, the switcher and pipeline under the interface become very neat.   

### Error Handling

- `IOError` is thrown
    - **upon errorneous file opening** (e.g. wrong file path, wrong file format, etc.)
        - empty line(s) would be skipped without throwing an error
- `ValueError` is thrown
    - **upon invalid entry (line) is processed**
        - the only three valid entry formats are the following: (`<int>` denotes a nonnegative integer within `[0,grid_size)`)
         1. `turn on <int>,<int> through <int>,<int>`
         2. `turn off <int>,<int> through <int>,<int>`
         3. `toggle <int>,<int> through <int>,<int>`
        - Please note that there shall not be space between the coordinate values.
        - Any command other than these three would result in ValueError.
    - **upon invalid coordinate values/formats**
        - may result from the failure of splitting exactly two integer values with the comma delimiter.
        - may result from the assertion error for coordinate value out of the `[0,grid_size)` range.

### Algorithm
All operations are performed with the help of numpy. The relevant operations include value assignment, addition, counting the occurrence of a specific value, computing the value of NOT-x against x element-wise, extracting the maximum possible value element-wise, summing up all values. 
