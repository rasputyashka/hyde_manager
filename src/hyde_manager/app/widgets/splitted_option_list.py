from __future__ import annotations

from typing import Any
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Container
from textual.message import Message
from textual.reactive import reactive
from textual.widget import Widget


class SplittedOptionList(Container, can_focus=True):
    BINDINGS = [
        Binding("up", "cursor_up"),
        Binding("down", "cursor_down"),
        Binding("enter", "select_option"),
    ]

    DEFAULT_CSS = """
    SplittedOptionList {
    }

    .top-option-list {
        dock: top;
        height: auto;
        padding: 1 0 1 1;
    }

    .bottom-option-list {
        dock: bottom;
        height: auto;
        padding: 1 0 1 1;
    }
    
    .active {
        background: $primary;
    }
    """

    highlighted: reactive[int] = reactive(0)

    class OptionMessage(Message):
        def __init__(
            self,
            option_list: SplittedOptionList,
            option: Any,
            option_index: int,
        ):
            super().__init__()
            self.option_list = option_list
            self.option = option
            self.option_index = option_index

    class OptionHiglighted(OptionMessage):
        pass

    class OptionSelected(OptionMessage):
        pass

    def __init__(
        self,
        top_options: list[Widget],
        bottom_options: list[Widget],
        **kwargs,
    ):
        self.top_options = top_options
        self.bottom_options = bottom_options
        super().__init__(**kwargs)
        self.top_options[0].add_class("active")  # TODO: test this
        self._options = top_options + bottom_options

    def compose(self) -> ComposeResult:
        with Container(classes="top-option-list"):
            for c in self.top_options:
                yield c
        with Container(classes="bottom-option-list"):
            for c in self.bottom_options:
                yield c

    def watch_highlighted(self, old_value: int, new_value: int):
        self.post_message(
            self.OptionHiglighted(self, self._options[new_value], new_value)
        )
        self._options[old_value].remove_class("active")
        self._options[new_value].add_class("active")

    def action_cursor_up(self):
        # support for wrapping around
        self.highlighted = (self.highlighted - 1) % len(self._options)

    def action_cursor_down(self):
        # support for wrapping around
        self.highlighted = (self.highlighted + 1) % len(self._options)

    def action_select_option(self):
        self.post_message(
            (
                self.OptionSelected(
                    self, self._options[self.highlighted], self.highlighted
                )
            )
        )
