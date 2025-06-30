from typing import Callable
from hyde_manager.app.base import SelectableOption
from hyde_manager.app.widgets.options import BaseOptionWidget


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
