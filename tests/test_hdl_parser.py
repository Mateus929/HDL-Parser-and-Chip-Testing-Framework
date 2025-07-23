from src.hdl_parser import HDLParser


def test_parse_simple_chip() -> None:
    hdl_content = """
    CHIP SimpleChip {
        IN a, b;
        OUT out;

        PARTS:
        And(a=a, b=b, out=out);
    }
    """

    parser = HDLParser()
    chip_def = parser.parse_hdl_content(hdl_content)

    assert chip_def.name == "SimpleChip"
    assert len(chip_def.inputs) == 2
    assert chip_def.inputs[0].name == "a"
    assert chip_def.inputs[1].name == "b"
    assert len(chip_def.outputs) == 1
    assert chip_def.outputs[0].name == "out"
    assert len(chip_def.parts) == 1
    assert chip_def.parts[0].chip_type == "And"


def test_parse_chip_with_comments() -> None:
    hdl_content = """
    // This is a simple chip
    CHIP CommentedChip {
        IN a, b; // Input pins
        OUT out; /* Output pin */

        PARTS:
        /* This is an AND gate */
        And(a=a, b=b, out=out); // Connect inputs to AND gate
    }
    """

    parser = HDLParser()
    chip_def = parser.parse_hdl_content(hdl_content)

    assert chip_def.name == "CommentedChip"
    assert len(chip_def.inputs) == 2
    assert len(chip_def.outputs) == 1
    assert len(chip_def.parts) == 1


def test_parse_chip_no_parts() -> None:
    hdl_content = """
    CHIP EmptyChip {
        IN a, b;
        OUT out;

        PARTS:
    }
    """

    parser = HDLParser()
    chip_def = parser.parse_hdl_content(hdl_content)

    assert chip_def.name == "EmptyChip"
    assert len(chip_def.parts) == 0


def test_parse_complex_connections() -> None:
    hdl_content = """
    CHIP ComplexChip {
        IN a, b, c;
        OUT out1, out2;

        PARTS:
        And(a=a, b=b, out=internal1);
        Or(a=internal1, b=c, out=out1);
        Not(in=out1, out=out2);
    }
    """

    parser = HDLParser()
    chip_def = parser.parse_hdl_content(hdl_content)

    assert chip_def.name == "ComplexChip"
    assert len(chip_def.inputs) == 3
    assert len(chip_def.outputs) == 2
    assert len(chip_def.parts) == 3

    and_part = chip_def.parts[0]
    assert and_part.chip_type == "And"
    assert and_part.connections["a"] == "a"
    assert and_part.connections["b"] == "b"
    assert and_part.connections["out"] == "internal1"
