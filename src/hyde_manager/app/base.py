from abc import ABC, abstractmethod
from typing import TypeVar
from textual.app import ComposeResult
from textual.containers import Container
from textual.app import App
from textual.widgets import Header, Footer, Static

from hyde_manager.app.widgets.options import BaseOptionWidget


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
    def __init__(self, name: str, description):
        self.name = name
        self.description = description


class Selectable(ABC):
    @abstractmethod
    def on_select(self): ...

    @abstractmethod
    def get_widget(self) -> BaseOptionWidget:
        pass


class SelectableOption(Option, Selectable):
    pass
