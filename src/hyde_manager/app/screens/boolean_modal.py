from typing import Any
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Container, Horizontal, Vertical
from textual.screen import ModalScreen, ScreenResultType
from textual.widgets import Static
from hyde_manager.app.base import NOT_SET


class BooleanModal(ModalScreen[bool | object]):
    """Styled modal that matches the screenshot"""

    BINDINGS = [
        Binding("escape", "dismiss", "Close"),
        Binding("left", "navigate_left", "Navigate left"),
        Binding("right", "navigate_right", "Navigate right"),
        Binding("enter", "select", "Select"),
        Binding("y", "select_yes", "Yes"),
        Binding("n", "select_no", "No"),
        Binding("u", "unset", "Unset"),
    ]
    CSS = """
    
    #modal-container {
        border: solid $primary;
        align: center middle;
        padding: 3;
    }
    
    #modal-content {
        width: 100%;
        height: 100%;
        align: center middle;
    }
    
    .question {
        width: 100%;
        text-align: center;
        text-style: bold;
        margin-bottom: 3;
        content-align: center middle;
    }
    
    #button-container {
        width: 100%;
        height: 5;
        align: center middle;
    }
    
    .modal-button {
        width: 12;
        height: 3;
        margin: 0 2;
        text-style: bold;
        text-align: center;
        content-align: center middle;
        border: solid transparent;
    }
    
    .yes-button.selected {
        background: $primary;
        color: black;
        border: solid $primary;
    }
    
    .yes-button.unselected {
        background: transparent;
        border: solid transparent;
    }
    
    .no-button.selected {
        background: $primary;
        color: black;
        border: solid $primary;
    }
    
    .no-button.unselected {
        background: transparent;
        border: solid transparent;
    }
    
    """

    def __init__(self, option_name: str, description: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.option_name = option_name
        self.description = description
        self.selected_option = True  # YES is on the left
        self.question = "Enable this option?"

    def compose(self) -> ComposeResult:
        with Container(id="modal-container"):
            with Vertical(id="modal-content"):
                yield Static(
                    self.question, id="question-text", classes="question"
                )
                with Horizontal(id="button-container"):
                    yield Static(
                        "Yes",
                        id="yes-btn",
                        classes="modal-button yes-button",
                    )
                    yield Static(
                        "No", id="no-btn", classes="modal-button no-button"
                    )

    def on_mount(self) -> None:
        self.update_selection()

    def update_selection(self) -> None:
        yes_btn = self.query_one("#yes-btn")
        no_btn = self.query_one("#no-btn")

        yes_btn.remove_class("selected")
        yes_btn.remove_class("unselected")
        no_btn.remove_class("selected")
        no_btn.remove_class("unselected")

        if self.selected_option:  # Yes selected
            yes_btn.add_class("selected")
            no_btn.add_class("unselected")
        else:
            no_btn.add_class("selected")
            yes_btn.add_class("unselected")

    def action_navigate_left(self) -> None:
        if not self.selected_option:
            self.selected_option = True
            self.update_selection()

    def action_navigate_right(self) -> None:
        if self.selected_option:
            self.selected_option = False
            self.update_selection()

    def action_select(self) -> None:
        if self.selected_option:
            self.dismiss(True)
        else:
            self.dismiss(False)

    def action_select_yes(self) -> None:
        self.dismiss(True)

    def action_select_no(self) -> None:
        self.dismiss(False)

    def action_unset(self) -> None:
        self.dismiss(NOT_SET)

    def action_dismiss(self) -> None:  # type: ignore
        self.dismiss(NOT_SET)
