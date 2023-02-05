import logging
from typing import List, Tuple

class IOProcessor:
    """
    An input processor that reads in a sequence of raw instructions from the parsed input file (.txt).
    Each line of instruction identifies inclusive ranges of coordinates, forming the opposite corners of a rectangle. 
    The objective of this class is to process the data in the form of a list of tuples for subsequent operations.
    """

    def __init__(self, input_path: str, grid_size: int):
        self.input_path = input_path
        self.input_list = []
        self.grid_size = grid_size

    def get_input(self):
        """Opens the input txt file."""
        try:
            with open(self.input_path, 'r') as f:
                for line in f:
                    l = line.split()
                    if l: # to skip empty line
                        self.input_list.append(l)
        except Exception as e:
            logging.error(e)
            raise IOError(f"Input data is invalid."
                          f"Please check the file path is correct and the content is written line-by-line in text format.")
    
    def parse_input(self) -> List[Tuple]:
        """Parses the sequences of operations into the desired format of inputs.
        
        Returns
        -------
        processed_entries
            a list of tuples, each tuple contains a string of command, a tuple of starting and ending indices (inclusive) in i direction, 
            and a tuple of starting and ending indices (inclusive) in j direction.

        Raises
        ------
        ValueError
            if the command string does not match 'turn on', 'turn off' or 'toggle',
            or if the format of a line does not strictly align with the designed format:
                'turn <off/on> <int>,<int> through <int>,<int>' or 'toggle <int>,<int> through <int>,<int>'.
        """

        def parse_range(str_start: List, str_end: List) -> Tuple:
            """Parses the coordinate pairs, checks their formats and ranges, and returns the pairs as tuples."""
            try:
                list_start, list_end = str_start.split(','), str_end.split(',')
                assert len(list_start) == 2 and len(list_end) == 2
                x_start, x_end = int(list_start[0]), int(list_end[0])
                y_start, y_end = int(list_start[1]), int(list_end[1])
                assert all(0 <= val < self.grid_size for val in [x_start, x_end, y_start, y_end]), f"coordinate out of range of a {self.grid_size}x{self.grid_size} grid."

            except Exception as e:
                raise ValueError(f"Parsing coordinates failed."
                                 f" Please check the coordinate design (comma delimiter and valid literal pairs for int conversion).")

            i_tuple = (x_start, x_end) if x_start <= x_end else (x_end, x_start)
            j_tuple = (y_start, y_end) if y_start <= y_end else (y_end, y_start)
            return i_tuple, j_tuple

        processed_entries = []
        for entry in self.input_list:
            # previously guaranteed non-empty entry in file opening
            if entry[0] == 'turn':
                if len(entry) != 5 or not entry[1] in ['on', 'off'] or entry[3] != 'through' or not ',' in (entry[2] and entry[4]):
                    raise ValueError(f"turn on/off command invalid for command {entry}."
                                     f" Please check if the command strictly follows 'turn <off/on> <int>,<int> through <int>,<int>' format,"
                                     f" with no space between each <int>,<int> coordinate pair.")
                i_tup, j_tup = parse_range(str_start=entry[2], str_end=entry[4])
                processed_entries.append((entry[1], i_tup, j_tup))

            elif entry[0] == 'toggle':
                if len(entry) != 4 or entry[2] != 'through' or not ',' in (entry[1] and entry[3]):
                    raise ValueError(f"toggle command invalid for command {entry}."
                                     f" Please check if the command strictly follows 'toggle <int>,<int> through <int>,<int>' format,"
                                     f" with no space between each <int>,<int> coordinate pair.")
                i_tup, j_tup = parse_range(str_start=entry[1], str_end=entry[3])
                processed_entries.append((entry[0], i_tup, j_tup))

            else:
                raise ValueError('The input line is invalid.')

        return processed_entries