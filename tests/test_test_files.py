import os

import pytest

from src.chip_models import ChipDefinition
from src.chip_simulator import ChipSimulator
from src.hdl_parser import HDLParser
from src.test_runner import TestRunner

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
TEST_DIR = os.path.join(ROOT_DIR, "test_files")


def prepare_chips(test_dir: str) -> tuple[dict[str, ChipDefinition], HDLParser]:
    parser = HDLParser()
    chip_map = {}

    for filename in os.listdir(test_dir):
        if filename.endswith(".hdl"):
            chip_name = os.path.splitext(filename)[0]
            hdl_path = os.path.join(test_dir, filename)
            chip = parser.parse_hdl_file(hdl_path)
            chip_map[chip_name] = chip

    return chip_map, parser


def collect_test_cases(
    test_dir: str, chip_map: dict[str, ChipDefinition]
) -> list[tuple[str, ChipDefinition, str]]:
    cases = []
    for chip_name, chip in chip_map.items():
        tv_path = os.path.join(test_dir, chip_name + ".tv")
        if os.path.exists(tv_path):
            cases.append((chip_name, chip, tv_path))
    return cases


CHIP_MAP, PARSER = prepare_chips(TEST_DIR)
TEST_CASES = collect_test_cases(TEST_DIR, CHIP_MAP)


@pytest.mark.parametrize("chip_name, chip, tv_path", TEST_CASES)
def test_chip(chip_name: str, chip: ChipDefinition, tv_path: str) -> None:
    simulator = ChipSimulator(PARSER)
    test_runner = TestRunner(simulator)

    passed, total = test_runner.run_tests(chip, tv_path)
    assert passed == total, f"{chip_name}: {passed}/{total} tests passed"
