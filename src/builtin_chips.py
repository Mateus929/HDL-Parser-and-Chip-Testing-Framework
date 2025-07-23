class BuiltinChips:
    """Implements the logic for built-in primitive chips"""

    @staticmethod
    def nand(a: int, b: int) -> int:
        """NAND gate: NOT (a AND b)"""
        return int(not (a and b))

    @staticmethod
    def not_gate(a: int) -> int:
        """NOT gate: NOT a"""
        return int(not a)

    @staticmethod
    def and_gate(a: int, b: int) -> int:
        """AND gate: a AND b"""
        return int(a and b)

    @staticmethod
    def or_gate(a: int, b: int) -> int:
        """OR gate: a OR b"""
        return int(a or b)
