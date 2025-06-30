import yaml

from hyde_manager.app.base import (
    NOT_SET,
    AppContainer,
    Option,
    OptionWithValue,
)
from hyde_manager.app.options import (
    BooleanOption,
    OneOfOption,
    SeveralOfOption,
)
from hyde_manager.app.button_as_option import ButtonAsOption

from hyde_manager.app.screens.boolean_modal import BooleanModal
from hyde_manager.app.widgets.sidebar_step_menu import SidebarStepMenu
from hyde_manager.app.screens.config_modal import ConfigModal
from hyde_manager.installer.config import InstallationConfig

from .config import load_install_cofnig

CONFIG = """
"""


class Installer(AppContainer):
    CONFIG_PATH = "config.yml"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.install_config = load_install_cofnig(
            yaml.safe_load(open(self.CONFIG_PATH))
        )

    def compose(self):
        renderable_options = []
        print(self.install_config)
        for option in self.install_config.options:
            if option.type == "boolean":
                renderable_options.append(
                    BooleanOption(
                        name=option.name,
                        description=option.description,
                        app=self.app,
                        value=option.default or NOT_SET,
                    )
                )
            elif option.type == "oneOf":
                renderable_options.append(
                    OneOfOption(
                        name=option.name,
                        description=option.description,
                        app=self.app,
                        value=option.default,
                        chooses=[
                            OptionWithValue(
                                suboption.name,
                                suboption.description,
                                suboption.name == option.default,
                            )
                            for suboption in option.chooses  # type: ignore
                        ],
                    )
                )
            elif option.type == "severalOf":
                renderable_options.append(
                    SeveralOfOption(
                        name=option.name,
                        description=option.description,
                        app=self.app,
                        value=option.default,
                        chooses=[
                            Option(option.name, option.description)
                            for option in option.chooses  # type: ignore
                        ],
                    )
                )
        self.options = renderable_options

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
