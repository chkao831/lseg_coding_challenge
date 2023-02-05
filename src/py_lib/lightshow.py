import numpy as np
from typing import List, Tuple

class LightShow:
    """
    The LightShow class represents the lightshow that demonstrates a sequence of instructions from part 1.
    It reads in processed_list, a sequence of processed instructions and performs the operations.
    Specifically speaking, the processed list is a list of tuples. Each tuple contains three elements:
    (command: str, i_range: Tuple[int, int], j_range: Tuple[int, int]). The ranges are inclusive.

    Each light is identified by a pair of coordinates, ranging from 0 to <grid_size-1(default=999)>.
    All lights start turned off. All lights are either on (denoted as 1) or off (denoted as 0).
    """
    
    def __init__(self, processed_list: List[Tuple], grid_size: int=1000):
        self.input = processed_list
        self.grid_size = grid_size
        self.matrix = np.zeros((grid_size, grid_size))

    def command_switcher(self):
        """A switcher in support of selecting one of the three supported operations."""
        action = {
            'on': self.turn_on, 
            'off': self.turn_off, 
            'toggle': self.toggle
        }
        for com, i, j in self.input:
            action.get(com)(i, j)

    def turn_on(self, i: Tuple[int], j: Tuple[int]):
        """Turns on light(s) given the inclusive ranges in i and j directions. Lights that were already on are unaffected."""
        self.matrix[i[0]:i[1]+1, j[0]:j[1]+1] = 1

    def turn_off(self, i: Tuple[int], j: Tuple[int]):
        """Turns off light(s) given the inclusive ranges in i and j directions. Lights that were already off are unaffected."""
        self.matrix[i[0]:i[1]+1, j[0]:j[1]+1] = 0

    def toggle(self, i: Tuple[int], j: Tuple[int]):
        """Inverts the light(s) given the inclusive ranges in i and j directions."""
        self.matrix[i[0]:i[1]+1, j[0]:j[1]+1] = np.logical_not(self.matrix[i[0]:i[1]+1, j[0]:j[1]+1])

    def counter(self) -> int:
        """Returns the result (number of lights on) by the end of all operations."""
        return np.count_nonzero(self.matrix==1)