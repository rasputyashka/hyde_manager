from hyde_manager.app.base import (
    AppContainer,
)
from hyde_manager.app.options import (
    BooleanOption,
    ButtonAsOption,
    OneOfOption,
    SeveralOfOption,
)
from hyde_manager.app.screens.boolean_modal import BooleanModal
from hyde_manager.app.widgets.sidebar_step_menu import SidebarStepMenu
from hyde_manager.app.screens.config_modal import ConfigModal

CONFIG = """
[hyde]
"""


class Installer(AppContainer):
    # def __init__(self, options, control_buttons, *args, **kwargs):
    #    super().__init__(*args, **kwargs)
    #    self.options = options
    #    self.control_buttons = control_buttons

    def compose(self):
        self.options = [
            BooleanOption(
                "Nvidia detection",
                "Detect nvidia GPU cards and install open-source drivers",
                app=self.app,
                value=True,
            ),
            OneOfOption("bar", "bar description", app=self.app),
            SeveralOfOption("baz", "baz description", app=self.app),
        ]

        self.control_buttons = [
            ButtonAsOption(
                "Install App",
                "Start installation",
                app=self.app,
                action=self.show_confirmation_window,
            ),
            ButtonAsOption(
                "Show config",
                "Show current configuration",
                app=self.app,
                action=self.show_config,
            ),
        ]
        yield SidebarStepMenu(
            options=self.options, control_buttons=self.control_buttons
        )

    def show_config(self):
        config_modal = ConfigModal(CONFIG)
        self.app.push_screen(config_modal)  # pass config screen

    def show_confirmation_window(self):
        confirmation_window = BooleanModal("Start installation?")

        def handle_confirmation_window_close(value):
            if value:
                self.run_installation()

        self.app.push_screen(
            confirmation_window, handle_confirmation_window_close
        )

    def run_installation(self):
        pass
