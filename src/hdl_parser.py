import os
import re
from typing import Dict, List

from src.chip_models import ChipDefinition, Pin, ChipInstance


class CommentRemover:
    @staticmethod
    def clean(content: str) -> str:
        content = re.sub(r"//.*$", "", content, flags=re.MULTILINE)
        content = re.sub(r"/\*.*?\*/", "", content, flags=re.DOTALL)
        return re.sub(r"\s+", " ", content).strip()


class PinParser:
    @staticmethod
    def parse(content: str, section_type: str) -> List[Pin]:
        pattern = rf"{section_type}\s+(.*?);"
        match = re.search(pattern, content, re.IGNORECASE)
        if not match:
            return []
        pins = []
        pin_names = [name.strip() for name in match.group(1).split(",")]
        for pin_name in pin_names:
            bus_match = re.match(r"(\w+)\[(\d+)\]", pin_name)
            if bus_match:
                pins.append(Pin(bus_match.group(1), int(bus_match.group(2))))
            else:
                pins.append(Pin(pin_name, 1))
        return pins


class PartsParser:
    @staticmethod
    def parse(content: str) -> List[ChipInstance]:
        parts_match = re.search(r"PARTS:\s*(.*)", content, re.DOTALL | re.IGNORECASE)
        if not parts_match:
            return []
        parts_content = parts_match.group(1).strip().rstrip("}")
        parts = []
        declarations = [p.strip() for p in parts_content.split(";") if p.strip()]
        for i, declaration in enumerate(declarations):
            part_match = re.match(r"(\w+)\s*\((.*?)\)", declaration)
            if not part_match:
                continue
            chip_type = part_match.group(1)
            connections_str = part_match.group(2)
            connections = {}
            for pair in [c.strip() for c in connections_str.split(",") if "=" in c]:
                pin_name, signal = pair.split("=", 1)
                connections[pin_name.strip()] = signal.strip()
            instance_name = f"{chip_type.lower()}_{i}"
            parts.append(ChipInstance(instance_name, chip_type, connections))
        return parts


class HDLParser:
    def __init__(self) -> None:
        self.builtin_chips = {"Nand", "Not", "And", "Or"}
        self.parsed_chips: Dict[str, ChipDefinition] = {}

    def parse_hdl_file(self, filename: str) -> ChipDefinition:
        if not os.path.exists(filename):
            raise FileNotFoundError(f"HDL file not found: {filename}")
        with open(filename, "r") as f:
            content = f.read()
        return self.parse_hdl_content(content)

    def parse_hdl_content(self, content: str) -> ChipDefinition:
        content = CommentRemover.clean(content)

        chip_match = re.search(r"CHIP\s+(\w+)\s*{", content)
        if not chip_match:
            raise ValueError("No CHIP declaration found")
        chip_name = chip_match.group(1)

        inputs = PinParser.parse(content, "IN")
        outputs = PinParser.parse(content, "OUT")
        parts = PartsParser.parse(content)

        chip_def = ChipDefinition(chip_name, inputs, outputs, parts)
        self.parsed_chips[chip_name] = chip_def
        return chip_def

    def get_chip_definition(
        self, chip_name: str, base_path: str = "."
    ) -> ChipDefinition | None:
        if chip_name in self.parsed_chips:
            return self.parsed_chips[chip_name]
        if chip_name in self.builtin_chips:
            return None
        path = os.path.join(base_path, f"{chip_name}.hdl")
        return self.parse_hdl_file(path)
