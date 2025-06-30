from typing import Callable, Generic

from textual.widget import Widget
from hyde_manager.app.base import (
    ConfigurableOption,
    Option,
    OptionWithValue,
    SelectableOption,
    ValueT,
    Sentinel,
    NOT_SET,
)
from hyde_manager.app.screens.boolean_modal import BooleanModal
from hyde_manager.app.screens.one_of_modal import OneOfModal
from hyde_manager.app.widgets.options import (
    BaseOptionWidget,
    OptionWidgetWithSetMark,
)


class BooleanOption(ConfigurableOption[bool]):
    def on_select(self):
        modal_window = BooleanModal(
            question=f"Do you want to enable {self.name}?"
        )
        self.app.push_screen(modal_window, self._on_config_window_closed)

    def _on_config_window_closed(self, returned_value):
        self.value = returned_value
        self.update_set_mark()


class OneOfOption(ConfigurableOption[str]):
    def __init__(
        self,
        name: str,
        description: str,
        app,
        chooses: list[OptionWithValue],  # this is actually a SubOption
        value: str | Sentinel = NOT_SET,
    ):
        super().__init__(name, description, app, value)
        self.chooses = chooses

    def on_select(self):
        modal = OneOfModal(self.name, options=self.chooses)
        res = self.app.push_screen(modal, self._on_config_window_closed)

    def _on_config_window_closed(self, returned_value):
        self.value = returned_value
        self.update_set_mark()


class SeveralOfOption(ConfigurableOption[list[str]]):
    def __init__(
        self,
        name: str,
        description: str,
        app,
        chooses: list[Option],  # this is actuall a SubOption
        value: list[str] | Sentinel = NOT_SET,
    ):
        super().__init__(name, description, app, value)
        self.chooses = chooses

    def _on_config_window_closed(self, returned_value):
        self.value = returned_value
        self.update_set_mark()

    def on_select(self):
        pass
