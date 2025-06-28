import rich
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Container, Horizontal, Vertical
from textual.screen import ModalScreen
from textual.widgets import RichLog, TextArea
from rich.syntax import Syntax


class ConfigModal(ModalScreen[bool | object]):
    """Styled modal that matches the screenshot"""

    BINDINGS = [
        Binding("escape", "close", "Close"),
    ]
    CSS = """ ConfigModal {
        background: rgba(0,0,0,0);
        align: center middle;
        padding: 1;
        height: 100%;
    }
    .rich-log {
        background: rgba(0,0,0,0);
    }
    """

    def __init__(self, config: str, lang: str = "toml", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config = config
        self.lang = lang

    def compose(self) -> ComposeResult:
        with Container(id="modal-container"):
            # rich_log = RichLog(highlight=True, markup=True, classes="rich-log")
            # rich_log.write(
            # Syntax(
            # self.config,
            # self.lang,
            # indent_guides=True,
            # background_color="green",
            # )
            # )
            # yield rich_log

            yield TextArea(
                self.config.strip(),
                language=self.lang,
                read_only=True,
            )

    def action_close(self) -> None:
        self.dismiss(None)
