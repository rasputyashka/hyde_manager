from textual import on
from textual.app import ComposeResult
from textual.binding import Binding
from textual.screen import ModalScreen

from hyde_manager.app.base import NOT_SET, OptionWithValue
from hyde_manager.app.base import ChoosableOption
from hyde_manager.app.button_as_option import ButtonAsOption
from hyde_manager.app.widgets.sidebar_step_menu import SidebarStepMenu
from hyde_manager.app.widgets.splitted_option_list import SplittedOptionList


class OneOfModal(ModalScreen[bool | object]):
    BINDINGS = [
        Binding("escape", "close", "Close"),
    ]

    def __init__(
        self, name: str, options: list[OptionWithValue], *args, **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.option_name = name
        self.raw_options = options
        self.options = [
            ChoosableOption(
                option.name,
                description=option.description,
                app=self.app,
                value=option.value,
            )
            for option in options
        ]

    def compose(self) -> ComposeResult:
        yield SidebarStepMenu(
            options=self.options,
            control_buttons=[
                ButtonAsOption(
                    "confirm",
                    f"confirm choosing {self.option_name}",
                    action=self.action_close,
                    app=self.app,
                )
            ],
        )

    def action_close(self) -> None:
        chosen_option = self.options[0]
        for option in self.options:
            if option.value:
                chosen_option = option
                break

        self.dismiss(chosen_option.name)

    @on(SplittedOptionList.OptionSelected)
    def on_option_selected(self, message):
        selected_option = message.option.option_parent
        if hasattr(selected_option, "value"):  # TODO: fix this shit
            if selected_option.value:
                for option in self.options:
                    if option != selected_option:
                        option.set_value(False)
