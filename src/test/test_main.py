import logging
import numpy as np
import pickle
import pytest

from ..py_lib.io import IOProcessor
from ..py_lib.lightshow import LightShow
from ..py_lib.lightshow_upgraded import LightShowUpgraded

logging.basicConfig(level=logging.DEBUG, filemode = 'a', format='%(levelname)s:%(asctime)s:  %(message)s'
                    , datefmt='%Y-%m-%d %H:%M:%S')

class TestMain:

    @pytest.fixture
    def sample_data(self):
        proc = IOProcessor(input_path="data/sample_input.txt", grid_size=1000)
        proc.get_input()
        data = proc.parse_input()
        return data

    def test_io_parsing(self):
        proc = IOProcessor(input_path="data/coding_challenge_input.txt", grid_size=1000)
        proc.get_input()
        processed = proc.parse_input()
        with open("src/test/test_data/coding_challenge_input_processed.pkl", "rb") as file:
            pickled = pickle.load(file)
        assert processed == pickled

    def test_assign_value(self, sample_data):
        light_1 = LightShow(sample_data, 1000)
        assert np.count_nonzero(light_1.matrix==1) == 0
        light_1.turn_on((1, 2), (3, 5))
        assert np.count_nonzero(light_1.matrix==1) == 3*2
        light_1.turn_off((1, 1), (5, 6))
        assert np.count_nonzero(light_1.matrix==1) == 3*2-1

    def test_matrix_binary_conversion(self, sample_data):
        light_1 = LightShow(sample_data, 1000)
        assert np.count_nonzero(light_1.matrix==0) == 1000*1000
        light_1.toggle((1, 6), (2, 4))
        assert np.count_nonzero(light_1.matrix==1) == 6*3
        light_1.toggle((0, 2), (4, 5))
        assert np.count_nonzero(light_1.matrix==1) == 6*3 - 2*1 + 4
        assert np.count_nonzero(light_1.matrix==0) == 1000*1000 - (6*3 - 2*1 + 4) 
    
    def test_matrix_addition(self, sample_data):
        light_2 = LightShowUpgraded(sample_data, 1000)
        assert np.count_nonzero(light_2.matrix==1) == 0
        light_2.turn_on((1, 2), (3, 5))
        assert int(light_2.matrix.sum()) == 3*2
        light_2.turn_on((1, 2), (3, 5))
        assert int(light_2.matrix.sum()) == 3*2*2
        light_2.toggle((0, 5), (2, 7))
        assert int(light_2.matrix.sum()) == 3*2*2 + 6*6*2

    def test_upgraded_turn_off(self, sample_data):
        light_2 = LightShowUpgraded(sample_data, 1000)
        light_2.matrix[3:6, 1:3] = 3
        assert int(light_2.matrix.sum()) == 3*2*3
        light_2.turn_off((3, 4), (1, 1))
        assert int(light_2.matrix.sum()) == 3*2*3 - 2*1
        light_2.turn_off((2, 4), (0, 2))
        assert int(light_2.matrix.sum()) == 3*2*3 - 2*1 - 2*2
        light_2.turn_off((0, 3), (0, 1)) # -1
        light_2.turn_off((0, 3), (0, 2)) # -1
        assert light_2.matrix[3, 1] == 0 
        assert int(light_2.matrix.sum()) == 3*2*3 - 2*1 - 2*2 - 2

    def test_sample_sys1_end_to_end(self, sample_data):
        light = LightShow(sample_data, 1000)
        light.command_switcher()
        ans = light.counter()
        assert ans == 998004

    def test_sample_sys2_end_to_end(self, sample_data):
        light = LightShowUpgraded(sample_data, 1000)
        light.command_switcher()
        ans = light.counter()
        assert ans == 1003996

    def test_turn_input_exception(self):
        with pytest.raises(Exception) as exc_info:   
            proc = IOProcessor(input_path="src/test/test_data/error_turn_input.txt", grid_size=1000)
            proc.get_input()
            proc.parse_input()
        assert str(exc_info.value) == (f"turn on/off command invalid for command ['turn', 'on', '0,0', 'through', '999,', '999']."
                                       f" Please check if the command strictly follows 'turn <off/on> <int>,<int> through <int>,<int>' format,"
                                       f" with no space between each <int>,<int> coordinate pair.")

    def test_toggle_input_exception(self):
        with pytest.raises(Exception) as exc_info:   
            proc = IOProcessor(input_path="src/test/test_data/error_toggle_input.txt", grid_size=1000)
            proc.get_input()
            proc.parse_input()
        assert str(exc_info.value) == (f"Parsing coordinates failed."
                                       f" Please check the coordinate design (comma delimiter and valid literal pairs for int conversion).")

    def test_out_of_range_input_exception(self):
        with pytest.raises(Exception) as exc_info:   
            proc = IOProcessor(input_path="src/test/test_data/error_out_of_range_input.txt", grid_size=1000)
            proc.get_input()
            proc.parse_input()
        assert str(exc_info.value) == (f"Parsing coordinates failed."
                                       f" Please check the coordinate design (comma delimiter and valid literal pairs for int conversion).")