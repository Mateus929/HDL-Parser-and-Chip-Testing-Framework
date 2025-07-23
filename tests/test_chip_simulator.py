from src.chip_simulator import ChipSimulator
from src.hdl_parser import HDLParser


def test_simulate_nand_gate() -> None:
    parser = HDLParser()
    simulator = ChipSimulator(parser)
    result = simulator._simulate_part("Nand", {"a": 1, "b": 1})
    assert result == {"out": 0}


def test_simulate_not_gate() -> None:
    parser = HDLParser()
    simulator = ChipSimulator(parser)
    result = simulator._simulate_part("Not", {"in": 1})
    assert result == {"out": 0}


def test_simulate_and_gate() -> None:
    parser = HDLParser()
    simulator = ChipSimulator(parser)
    result = simulator._simulate_part("And", {"a": 1, "b": 1})
    assert result == {"out": 1}


def test_simulate_or_gate() -> None:
    parser = HDLParser()
    simulator = ChipSimulator(parser)
    result = simulator._simulate_part("Or", {"a": 0, "b": 1})
    assert result == {"out": 1}


def test_simulate_composed_chip() -> None:
    hdl_content = """
    CHIP TestAnd {
        IN a, b;
        OUT out;

        PARTS:
        Nand(a=a, b=b, out=nandOut);
        Not(in=nandOut, out=out);
    }
    """

    parser = HDLParser()
    simulator = ChipSimulator(parser)

    chip_def = parser.parse_hdl_content(hdl_content)

    assert simulator.simulate_chip(chip_def, {"a": 0, "b": 0}) == {"out": 0}
    assert simulator.simulate_chip(chip_def, {"a": 0, "b": 1}) == {"out": 0}
    assert simulator.simulate_chip(chip_def, {"a": 1, "b": 0}) == {"out": 0}
    assert simulator.simulate_chip(chip_def, {"a": 1, "b": 1}) == {"out": 1}
