from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Container, Horizontal
from textual.screen import ModalScreen
from textual.widgets import (
    Button,
    Input,
    Label,
    ListItem,
    ListView,
)
from textual.app import App
from textual.app import ComposeResult
from textual.containers import Container
from textual.widgets import Header, Footer, Static


NOT_SET = object()  # sentinel object


class AppContainer(Container):
    """Base class for all containers/

    Container is a widget that holds widgets with options and options info.
    """


class Application(App):
    CSS = """
    .p-1 { padding: 1 }
    .p-2 { padding: 2 }
    .m-1 { margin: 1 }
    .m-2 { margin: 2 }

    .options-container {
        height: 100%;
        width: 1fr;
    }
    .option-info {
        height: 100%;
        width: 3fr;
    }

    .welcome-text {
        text-align: center;
    }
    
    .app-container {
        layout: horizontal;
    }

    .options-list {
        height: 100%;
        width: 1fr;
        border: solid $primary;
        background: rgba(0,0,0,0);
    }
    .option-info {
        height: 100%;
        width: 3fr;
        border: solid $primary;
    }
    """

    def __init__(
        self, app_container_class: type[AppContainer], *args, **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.app_container_class = app_container_class

    def compose(self) -> ComposeResult:
        yield Header(classes="header")
        yield Static("Welcome to HyDE manager", classes="welcome-text m-1")
        yield self.app_container_class(classes="app-container")
        yield Footer()
