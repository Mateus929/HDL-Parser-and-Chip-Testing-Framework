from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class Pin:
    name: str
    width: int = 1


@dataclass
class Connection:
    source_chip: str
    source_pin: str
    target_chip: str
    target_pin: str


@dataclass
class ChipInstance:
    name: str
    chip_type: str
    connections: Dict[str, str] = field(default_factory=dict)


@dataclass
class ChipDefinition:
    name: str
    inputs: List[Pin]
    outputs: List[Pin]
    parts: List[ChipInstance]
