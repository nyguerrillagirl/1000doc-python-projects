# test_aoc_template.py

import pathlib
import pytest
import puzzle_20201205 as aoc

PUZZLE_DIR = pathlib.Path(__file__).parent

@pytest.fixture
def example1():
    puzzle_input = (PUZZLE_DIR / "20201205_TEST_INPUT_01.txt").read_text().strip()
    return aoc.parse(puzzle_input)

@pytest.fixture
def example2():
    puzzle_input = (PUZZLE_DIR / "20201205_TEST_INPUT_01.txt").read_text().strip()
    return aoc.parse(puzzle_input)

def test_parse_example1(example1):
    """Test that input is parsed properly."""
    assert example1 == ['FBFBBFFRLR', 'BFFFBBFRRR', 'FFFBBBFRRR', 'BBFFBBFRLL']


def test_processFB1():
    """Test part 1 on example input."""
    assert aoc.processFB("FBFBBFF", {}) == 44

def test_processLR1():
    """Test part 2 on example input."""
    assert aoc.processLR("RLR",{}) == 5

def test_process_string():
    boarding_pass = "FBFBBFFRLR"
    assert aoc.
@pytest.mark.skip(reason="Not implemented")
def test_part2_example2(example2):
    """Test part 2 on example input."""
    assert aoc.part2(example2) == ...