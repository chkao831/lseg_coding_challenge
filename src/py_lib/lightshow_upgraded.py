import numpy as np

from typing import List, Tuple
from .lightshow import LightShow

class LightShowUpgraded(LightShow):
    """
    The LightShowUpgraded class inherits LightShow.
    Similarly, it represents the lightshow, upgraded, that demonstrates a sequence of instructions from part 2.
    It also reads a sequence of processed instructions and performs the operations.

    Each light is identified by a pair of coordinates, ranging from 0 to <grid_size-1(default=999)>.
    Each light now has individual brightness levels, with a brightness level of 0 or higher.
    All lights start turned off (i.e. brightness=0).
    """
    
    def __init__(self, processed_list: List[Tuple], grid_size=1000):
        super().__init__(processed_list, grid_size)

    def turn_on(self, i: Tuple[int], j: Tuple[int]):
        """Increases the brightness of lights from the given inclusive ranges in i and j directions by 1."""
        self.matrix[i[0]:i[1]+1, j[0]:j[1]+1] += 1

    def turn_off(self, i: Tuple[int], j: Tuple[int]):
        """Decreases the brightness of lights from the given inclusive ranges in i and j directions, with a minimum of 0."""
        i_0, i_1, j_0, j_1 = i[0], i[1]+1, j[0], j[1]+1
        self.matrix[i_0:i_1, j_0:j_1] = np.maximum(self.matrix[i_0:i_1, j_0:j_1]-1, 0)

    def toggle(self, i: Tuple[int], j: Tuple[int]):
        """Increases the brightness of lights from the given inclusive ranges in i and j directions by 2."""
        self.matrix[i[0]:i[1]+1, j[0]: j[1]+1] += 2

    def counter(self) -> int:
        """Returns the result (sum of brightness) by the end of all operations."""
        return int(self.matrix.sum())