import os
from typing import Dict, List


class TestVector:
    def __init__(self, inputs: Dict[str, int], expected_outputs: Dict[str, int]):
        self.inputs = inputs
        self.expected_outputs = expected_outputs


class TestVectorParser:
    def parse_test_file(self, filename: str) -> List[TestVector]:
        if not os.path.exists(filename):
            raise FileNotFoundError(f"Test file not found: {filename}")

        with open(filename, "r") as f:
            lines = [line.strip() for line in f.readlines() if line.strip()]

        if not lines:
            return []

        header = lines[0]
        input_part, output_part = header.split(";")
        input_names = [name.strip() for name in input_part.split(",")]
        output_names = [name.strip() for name in output_part.split(",")]

        test_vectors = []

        for line in lines[1:]:
            input_part, output_part = line.split(";")
            input_values = [int(val.strip()) for val in input_part.split(",")]
            output_values = [int(val.strip()) for val in output_part.split(",")]

            inputs = dict(zip(input_names, input_values))
            expected_outputs = dict(zip(output_names, output_values))

            test_vectors.append(TestVector(inputs, expected_outputs))

        return test_vectors
