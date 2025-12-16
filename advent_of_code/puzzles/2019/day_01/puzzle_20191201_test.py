# test_aoc201901.py

import pathlib
import pytest
import puzzle_20191201 as aoc

PUZZLE_DIR = pathlib.Path(__file__).parent


@pytest.fixture
def example1():
    puzzle_input = (PUZZLE_DIR / "20191201_TEST_INPUT_01.txt").read_text().strip()
    return aoc.parse(puzzle_input)


def test_parse_example1(example1):
    """Test that input is parsed properly."""
    assert example1 == [12, 14, 1969, 100756]


def test_part1_example1(example1):
    """Test part 1 on example input."""
    assert aoc.part1(example1) == 2 + 2 + 654 + 33583


def test_part2_calculate_total_fuel1():
    assert aoc.calculate_total_fuel(14) == 2


def test_part2_calculate_total_fuel2():
    assert aoc.calculate_total_fuel(1969) == 966


def test_part2_calculate_total_fuel3():
    assert aoc.calculate_total_fuel(100756) == 50346