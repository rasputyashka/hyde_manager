from typing import Callable, Generic

from textual.widget import Widget
from hyde_manager.app.base import (
    SelectableOption,
    ValueT,
    Sentinel,
    NOT_SET,
)
from hyde_manager.app.screens.boolean_modal import BooleanModal
from hyde_manager.app.widgets.options import (
    BaseOptionWidget,
    OptionWidgetWithSetMark,
)


class ConfigurableOption(SelectableOption, Generic[ValueT]):
    def __init__(
        self,
        name: str,
        description: str,
        app,
        value: ValueT | Sentinel = NOT_SET,
    ):
        # value may be changed, but the _default -- not
        super().__init__(name, description)
        self.value = value
        self._default = value
        self.app = app
        self._widget: OptionWidgetWithSetMark = OptionWidgetWithSetMark(
            name, self.get_set_mark(), option_parent=self
        )

    def get_set_mark(self) -> str:
        if self.value is not NOT_SET:
            return "[+]"
        else:
            return ""

    def update_set_mark(self):
        self._widget.set_is_set_mark(self.get_set_mark())

    def _on_config_window_closed(self, returned_value):
        self.value = returned_value
        print(self.value, "option returned")
        self.update_set_mark()

    def get_widget(self) -> BaseOptionWidget:
        return self._widget


class BooleanOption(ConfigurableOption[bool]):
    def on_select(self):
        modal_window = BooleanModal(
            question=f"Do you want to enable {self.name}?"
        )
        self.app.push_screen(modal_window, self._on_config_window_closed)

    def get_set_mark(self) -> str:
        if self.value is NOT_SET:
            if self._default is NOT_SET:
                new_set_mark = ""
            else:
                if self._default:
                    new_set_mark = "[d+]"
                else:
                    new_set_mark = "[d-]"
        else:
            if self.value:
                new_set_mark = "[+]"
            else:
                new_set_mark = "[-]"

        return new_set_mark


class OneOfOption(ConfigurableOption[str]):
    def on_select(self):
        pass

    def on_config_window_closed(self, returned_value):
        self.value = returned_value


class SeveralOfOption(ConfigurableOption[list[str]]):
    def on_select(self):
        pass


class ButtonAsOption(SelectableOption):
    def __init__(self, name: str, description: str, app, action: Callable):
        super().__init__(name, description)
        self.app = app
        self._widget: BaseOptionWidget = BaseOptionWidget(
            name, option_parent=self
        )
        self.action = action

    def on_select(self):
        self.action()

    def get_widget(self) -> BaseOptionWidget:
        return self._widget
