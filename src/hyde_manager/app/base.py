from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar
from textual.app import ComposeResult
from textual.containers import Container
from textual.app import App
from textual.widgets import Header, Footer, Static

from hyde_manager.app.widgets.options import (
    BaseOptionWidget,
    OptionWidgetWithSetMark,
)


ValueT = TypeVar("ValueT")


class Sentinel:
    def __repr__(self) -> str:
        return "Sentinel object"


NOT_SET = Sentinel()  # sentinel object


class AppContainer(Container):
    """Base class for all containers.

    Container is a widget that holds widgets with options and options info.
    """


class Application(App):
    CSS = """
    .p-1 { padding: 1 }
    .p-2 { padding: 2 }
    .m-1 { margin: 1 }
    .m-2 { margin: 2 }

    .welcome-text {
        text-align: center;
    }
    
    .app-container {
        layout: horizontal;
    }

    """

    TITLE = "HyDE Manager"

    def __init__(
        self, app_container_class: type[AppContainer], *args, **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.app_container_class = app_container_class
        self.capture_mouse(None)

    def compose(self) -> ComposeResult:
        yield Header(classes="header")
        yield Static("Welcome to HyDE manager", classes="welcome-text m-1")
        yield self.app_container_class(classes="app-container")
        yield Footer()


class Option:
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description


class OptionWithValue(Option):
    def __init__(self, name: str, description: str, value: Any):
        super().__init__(name, description)
        self.value = value


class Selectable(ABC):
    @abstractmethod
    def on_select(self): ...

    @abstractmethod
    def get_widget(self) -> BaseOptionWidget:
        pass


class SelectableOption(Option, Selectable):
    pass


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
            if self.value:
                return "[+]"
            else:
                return "[-]"
        else:
            return ""

    def update_set_mark(self):
        self._widget.set_is_set_mark(self.get_set_mark())

    def get_widget(self) -> BaseOptionWidget:
        return self._widget

    def unset_value(self):
        self.value = self._default
        self.update_set_mark()

    def set_value(self, value: ValueT | Sentinel):
        self.value = value
        self.update_set_mark()


class ChoosableOption(ConfigurableOption[bool]):
    def __init__(
        self,
        name: str,
        description: str,
        app,
        value: bool = False,
    ):
        # value may be changed, but the _default -- not
        super().__init__(name, description, app, value)

    """Used for options in 'one of several' or 'one of' option lists

    This is like a boolean option, but it does not show modal window on select
    """

    def on_select(self):
        self.value = not self.value
        self.update_set_mark()
