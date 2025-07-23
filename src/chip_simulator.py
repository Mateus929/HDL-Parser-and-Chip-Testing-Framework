from typing import Dict

from src.builtin_chips import BuiltinChips
from src.chip_models import ChipDefinition
from src.hdl_parser import HDLParser


class ChipSimulator:
    def __init__(self, parser: HDLParser):
        self.parser = parser
        self.builtin = BuiltinChips()

    def simulate_chip(
        self, chip_def: ChipDefinition, inputs: Dict[str, int]
    ) -> Dict[str, int]:
        if not chip_def:
            raise ValueError("Cannot simulate None chip definition")

        signals = inputs.copy()

        for part in chip_def.parts:
            part_inputs = {}

            for pin_name, signal_name in part.connections.items():
                if signal_name in signals:
                    part_inputs[pin_name] = signals[signal_name]
                else:
                    try:
                        part_inputs[pin_name] = int(signal_name)
                    except ValueError:
                        part_inputs[pin_name] = 0

            part_outputs = self._simulate_part(part.chip_type, part_inputs)

            for pin_name, value in part_outputs.items():
                for conn_pin, signal_name in part.connections.items():
                    if conn_pin == pin_name:
                        signals[signal_name] = value
                        break

        outputs = {}
        for output_pin in chip_def.outputs:
            if output_pin.name in signals:
                outputs[output_pin.name] = signals[output_pin.name]
            else:
                outputs[output_pin.name] = 0

        return outputs

    def _simulate_part(self, chip_type: str, inputs: Dict[str, int]) -> Dict[str, int]:
        if chip_type == "Nand":
            a = inputs.get("a", 0)
            b = inputs.get("b", 0)
            return {"out": self.builtin.nand(a, b)}

        elif chip_type == "Not":
            a = inputs.get("in", 0)
            return {"out": self.builtin.not_gate(a)}

        elif chip_type == "And":
            a = inputs.get("a", 0)
            b = inputs.get("b", 0)
            return {"out": self.builtin.and_gate(a, b)}

        elif chip_type == "Or":
            a = inputs.get("a", 0)
            b = inputs.get("b", 0)
            return {"out": self.builtin.or_gate(a, b)}

        else:
            chip_def = self.parser.get_chip_definition(chip_type)
            if chip_def:
                return self.simulate_chip(chip_def, inputs)
            else:
                raise ValueError(f"Unknown chip type: {chip_type}")
