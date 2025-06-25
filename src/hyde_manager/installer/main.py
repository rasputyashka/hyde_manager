from textual.app import ComposeResult
from textual.widgets import Static

from hyde_manager.app.base import AppContainer
from hyde_manager.app.widgets.base import ConfigurableOptionList
from hyde_manager.app.widgets.options import BooleanOption


class Installer(AppContainer):
    def compose(self) -> ComposeResult:
        print("here")
        self.description_label = Static("", classes="option-info m-1 p-1")
        self.option_list = ConfigurableOptionList(
            BooleanOption("foo", "foo description"),
            description_field=self.description_label,
            classes="options-list m-1 p-1",
        )
        yield self.option_list
        yield self.description_label

    def on_mount(self) -> None:
        self.option_list.border_title = "Options"
        self.description_label.border_subtitle = "Info"
