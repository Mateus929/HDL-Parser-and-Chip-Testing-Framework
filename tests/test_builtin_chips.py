from src.builtin_chips import BuiltinChips


def test_nand_gate() -> None:
    assert BuiltinChips.nand(0, 0) == 1
    assert BuiltinChips.nand(0, 1) == 1
    assert BuiltinChips.nand(1, 0) == 1
    assert BuiltinChips.nand(1, 1) == 0


def test_not_gate() -> None:
    assert BuiltinChips.not_gate(0) == 1
    assert BuiltinChips.not_gate(1) == 0


def test_and_gate() -> None:
    assert BuiltinChips.and_gate(0, 0) == 0
    assert BuiltinChips.and_gate(0, 1) == 0
    assert BuiltinChips.and_gate(1, 0) == 0
    assert BuiltinChips.and_gate(1, 1) == 1


def test_or_gate() -> None:
    assert BuiltinChips.or_gate(0, 0) == 0
    assert BuiltinChips.or_gate(0, 1) == 1
    assert BuiltinChips.or_gate(1, 0) == 1
    assert BuiltinChips.or_gate(1, 1) == 1
