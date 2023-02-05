import argparse
import logging
import os

from typing import Callable, List, Tuple
from .py_lib.io import IOProcessor
from .py_lib.lightshow import LightShow
from .py_lib.lightshow_upgraded import LightShowUpgraded

logging.basicConfig(level=logging.DEBUG, filemode='a', format='%(levelname)s:%(asctime)s:  %(message)s'
                    , datefmt=' %Y-%m-%d %H:%M:%S')

def light_switcher(system_selection: int, input_data: List[Tuple], grid_size: int) -> Callable:
    """A switcher in support of selecting one of the two light systems."""
    system = {
        1: LightShow(input_data, grid_size), 
        2: LightShowUpgraded(input_data, grid_size), 
    }
    return system.get(system_selection)

def run_lightshow(args):
    """The main function that runs the main pipeline by the parser input.
       It firstly processes the data, and then passes the processed data to the lightshow algorithm.
       Upon running the lightshow, the result would be printed to the console.
    """
    proc = IOProcessor(os.path.join('data', args.input), args.grid)
    proc.get_input()
    data = proc.parse_input()
    light = light_switcher(args.system, data, args.grid)
    light.command_switcher()
    ans = light.counter()
    logging.info(f'[System {args.system}] The final brightness is {ans}.')

parser = argparse.ArgumentParser(description='Perform Lightshow')

parser.add_argument('input', help='The input data file name under /data folder.')
parser.add_argument('--system', type=int, choices=[1,2], help='Optional. Selection from system 1 or 2 (upgraded). Default is system 1.', default=1)
parser.add_argument('--grid', type=int, help='Optional. The side length of the grid. Default is 1000.', default=1000)

run_lightshow(parser.parse_args())
