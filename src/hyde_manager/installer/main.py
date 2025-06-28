from hyde_manager.app.base import (
    AppContainer,
)
from hyde_manager.app.options import (
    BooleanOption,
    ButtonAsOption,
    OneOfOption,
    SeveralOfOption,
)
from hyde_manager.app.widgets.sidebar_step_menu import SidebarStepMenu
from hyde_manager.app.screens.config_modal import ConfigModal

CONFIG = """
[project]
version = "12"
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
                action=lambda x: x,
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
