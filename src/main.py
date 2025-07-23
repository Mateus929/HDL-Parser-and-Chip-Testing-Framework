import os
from typing import Optional

import click

from src.chip_simulator import ChipSimulator
from src.hdl_parser import HDLParser
from src.test_runner import TestRunner


def run_single_test(hdl_file: str, tv_file: str) -> tuple[int, int]:
    parser = HDLParser()
    simulator = ChipSimulator(parser)
    test_runner = TestRunner(simulator)

    if not os.path.exists(hdl_file):
        click.echo(f"HDL file not found: {hdl_file}")
        return 0, 0
    if not os.path.exists(tv_file):
        click.echo(f"Test vector file not found: {tv_file}")
        return 0, 0

    chip = parser.parse_hdl_file(hdl_file)
    passed, total = test_runner.run_tests(chip, tv_file)
    return passed, total


def run_directory_tests(dir_path: str) -> None:
    parser = HDLParser()
    simulator = ChipSimulator(parser)
    test_runner = TestRunner(simulator)

    chip_map = {}

    for filename in os.listdir(dir_path):
        if filename.endswith(".hdl"):
            chip_path = os.path.join(dir_path, filename)
            chip_name = os.path.splitext(filename)[0]
            chip = parser.parse_hdl_file(chip_path)
            chip_map[chip_name] = chip

    total_passed = 0
    total_tests = 0

    for chip_name, chip in chip_map.items():
        test_filename = chip_name + ".tv"
        test_path = os.path.join(dir_path, test_filename)
        if os.path.exists(test_path):
            passed, total = test_runner.run_tests(chip, str(test_path))
            total_passed += passed
            total_tests += total
        else:
            click.echo(
                f"No test file found for {chip_name} ({test_filename} missing)\n"
            )

    click.echo("=" * 50)
    click.echo(
        f"Total Summary: {total_passed}/{total_tests} tests passed across all chips"
    )
    click.echo("=" * 50)


@click.command()
@click.option(
    "-f",
    "--files",
    nargs=2,
    type=click.Path(exists=True, dir_okay=False),
    help="Run test on given HDL and TV files",
)
@click.option(
    "-d",
    "--directory",
    type=click.Path(exists=True, file_okay=False),
    help="Run tests on all HDL and matching TV files in the directory",
)
def main(files: Optional[tuple[str, str]], directory: Optional[str]) -> None:
    if files:
        hdl_file, tv_file = files
        run_single_test(hdl_file, tv_file)
    elif directory:
        run_directory_tests(directory)
    else:
        click.echo("You must specify either --files or --directory option")
        raise click.Abort()


if __name__ == "__main__":
    main()
