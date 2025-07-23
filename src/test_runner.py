from typing import Tuple

import click

from src.chip_models import ChipDefinition
from src.chip_simulator import ChipSimulator
from src.test_vector_parser import TestVectorParser


class TestRunner:
    def __init__(self, simulator: ChipSimulator):
        self.simulator = simulator
        self.test_parser = TestVectorParser()

    def run_tests(self, chip_def: ChipDefinition, test_file: str) -> Tuple[int, int]:
        test_vectors = self.test_parser.parse_test_file(test_file)
        passed = 0
        total = len(test_vectors)

        click.echo("=" * 50)
        click.echo(f"Testing chip: {chip_def.name}")
        click.echo("=" * 50)

        for i, test_vector in enumerate(test_vectors):
            try:
                actual_outputs = self.simulator.simulate_chip(
                    chip_def, test_vector.inputs
                )
                test_passed = True
                for output_name, expected_value in test_vector.expected_outputs.items():
                    actual_value = actual_outputs.get(output_name, 0)
                    if actual_value != expected_value:
                        test_passed = False
                        break

                if test_passed:
                    passed += 1
                    status = "PASS"
                else:
                    status = "FAIL"

                inputs_str = ", ".join(
                    f"{k}={v}" for k, v in test_vector.inputs.items()
                )
                expected_str = ", ".join(
                    f"{k}={v}" for k, v in test_vector.expected_outputs.items()
                )
                actual_str = ", ".join(f"{k}={v}" for k, v in actual_outputs.items())

                click.echo(f"Test {i + 1}: {status}")
                click.echo(f"  Inputs: {inputs_str}")
                click.echo(f"  Expected: {expected_str}")
                click.echo(f"  Actual: {actual_str}")

                if not test_passed:
                    click.echo("Mismatch detected")
                else:
                    click.echo("Test passed")
                click.echo()

            except Exception as e:
                click.echo(f"Test {i + 1}: ERROR - {str(e)}")
                click.echo()

        click.echo("=" * 50)
        click.echo(f"Test Summary: {passed}/{total} tests passed")
        click.echo("=" * 50)
        click.echo()

        return passed, total
