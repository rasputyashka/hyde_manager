from textual.app import ComposeResult
from textual.containers import Container
from textual.reactive import reactive
from textual.widgets import Static


class BaseOptionWidget(Container):
    DEFAULT_CSS = """
    BaseOptionWidget.active {
        background: $primary;
    }

    BaseOptionWidget {
        layout: horizontal;
        height: auto;
    }

    .option-title {
        height: auto;
        width: auto;
    }

    .option-set-mark {
        width: auto;
        dock: right;
    }
    """

    def __init__(self, option_name, option_parent, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.option_name = option_name
        # the widget already has the parent attribute
        self.option_parent = option_parent

    def compose(self) -> ComposeResult:
        yield Static(self.option_name, classes="option-title")


class OptionWidgetWithSetMark(BaseOptionWidget):
    is_set_mark: reactive[str] = reactive("")

    def __init__(
        self, option_name: str, is_set_mark: str, option_parent, *args, **kwargs
    ):
        super().__init__(
            option_name=option_name,
            option_parent=option_parent,
            *args,
            **kwargs,
        )
        self.option_name = option_name
        self.mark = Static("", classes="option-set-mark")
        self.is_set_mark = is_set_mark

    def compose(self) -> ComposeResult:
        yield from super().compose()
        yield self.mark

    def watch_is_set_mark(self, old_value: str, new_value: str):
        print("setting is_set_mark")
        self.mark.update(new_value)

    def set_is_set_mark(self, new_mark: str):
        self.is_set_mark = new_mark
