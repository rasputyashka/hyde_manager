from dataclasses import dataclass
from typing import Any, Optional

from hyde_manager.app.base import NOT_SET, Sentinel


@dataclass
class SubOption:
    name: str
    description: str


@dataclass
class Option:
    name: str
    description: str
    type: str
    chooses: Optional[list[SubOption]] = None
    default: Any | Sentinel = NOT_SET


@dataclass
class InstallationConfig:
    options: list[Option]


def load_install_cofnig(mapping) -> InstallationConfig:
    return InstallationConfig(
        [
            Option(
                option["name"],
                option["description"],
                option["type"],
                chooses=[
                    SubOption(**suboption)
                    for suboption in option.get("chooses", [])
                ],
                default=option["default"],
            )
            for option in mapping["options"]
        ]
    )
