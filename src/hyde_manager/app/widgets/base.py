from abc import ABC, abstractmethod
from typing import Any

from textual.binding import Binding
from textual.screen import ModalScreen

from textual.widgets import (
    OptionList,
    Static,
)
from textual.widgets.option_list import Option

from hyde_manager.app.base import NOT_SET


class CustomOption(Option):
    name: str
    description: str
    value: Any

    def __init__(
        self,
        name: str,
        description: str,
        value: Any = NOT_SET,
        *args,
        **kwargs,
    ):
        super().__init__(name, *args, **kwargs)
        self.name = name
        self.description = description
        self._update_value(value)

    def _update_value(self, value):
        self.value = value
        if value is NOT_SET:
            self._set_prompt(self.name)
        else:
            self._set_prompt(self.name + "[+]")


class ConfigurableOption(CustomOption, ABC):
    @abstractmethod
    def get_configuration_window(self, *args, **kwarg) -> ModalScreen:
        pass


class ConfigurableOptionList(OptionList):
    BINDINGS = [
        Binding("enter", "select", "Select option"),
    ]

    def __init__(
        self,
        *options: ConfigurableOption,
        description_field: Static,
        **kwargs,
    ):
        super().__init__(*options, **kwargs)
        self.__options = list(options)
        self.description_label = description_field

    def on_mount(self) -> None:
        super().on_mount()
        self.description_label.update(self.__options[0].description)  # type: ignore

    def action_cursor_up(self) -> None:
        super().action_cursor_up()
        self.description_label.update(
            self.__options[self.highlighted].description  # type: ignore
        )

    def action_cursor_down(self) -> None:
        super().action_cursor_down()
        self.description_label.update(
            self.__options[self.highlighted].description  # type: ignore
        )

    def _set_option_value_callback(self, value: Any) -> None:
        option = self.get_option_at_index(self.highlighted)  # type: ignore
        option.value = value  # type: ignore

    def action_select(self) -> None:
        if self.highlighted is not None:
            self.app.push_screen(
                # for some reason it is mandatory create new window each time
                # probably because the internal logic is bound to id of an object
                self.__options[self.highlighted].get_configuration_window(),
                self._set_option_value_callback,
            )
