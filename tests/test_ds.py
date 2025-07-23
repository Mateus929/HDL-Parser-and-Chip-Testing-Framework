from src.test_vector_parser import TestVector
from src.chip_models import Pin, ChipInstance, ChipDefinition


def test_pin_creation() -> None:
    pin = Pin("test_pin", 8)
    assert pin.name == "test_pin"
    assert pin.width == 8

    pin_default = Pin("default_pin")
    assert pin_default.width == 1


def test_chip_instance_creation() -> None:
    connections = {"a": "input1", "b": "input2", "out": "output1"}
    instance = ChipInstance("test_instance", "And", connections)

    assert instance.name == "test_instance"
    assert instance.chip_type == "And"
    assert instance.connections == connections


def test_chip_definition_creation() -> None:
    inputs = [Pin("a"), Pin("b")]
    outputs = [Pin("out")]
    parts = [ChipInstance("and1", "And", {"a": "a", "b": "b", "out": "out"})]

    chip_def = ChipDefinition("TestChip", inputs, outputs, parts)

    assert chip_def.name == "TestChip"
    assert len(chip_def.inputs) == 2
    assert len(chip_def.outputs) == 1
    assert len(chip_def.parts) == 1


def test_test_vector_creation() -> None:
    inputs = {"a": 1, "b": 0}
    outputs = {"out": 0}
    vector = TestVector(inputs, outputs)

    assert vector.inputs == inputs
    assert vector.expected_outputs == outputs
