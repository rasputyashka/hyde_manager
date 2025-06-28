from textual import on
from textual.app import ComposeResult
from textual.containers import Horizontal
from textual.widgets import Markdown, Rule

from hyde_manager.app.base import SelectableOption
from hyde_manager.app.options import ConfigurableOption
from hyde_manager.app.widgets.options import (
    BaseOptionWidget,
    OptionWidgetWithSetMark,
)
from hyde_manager.app.widgets.splitted_option_list import SplittedOptionList


class SidebarStepMenu(Horizontal):
    DEFAULT_CSS = """
        SidebarStepMenu {
            margin: 0 1 1 2;
            border: solid $primary;
        }

        .option-description-field {
            padding: 1 2;
            width: 10fr;
            height: 100%;
            background: transparent;
        }

        .option-list {
            width: 3fr;
            height: 100%;
        }
    """

    def __init__(
        self,
        options: list[ConfigurableOption],
        control_buttons: list[SelectableOption],
        *args,
        **kwargs,
    ):
        self.options = options
        self.control_buttons = control_buttons

        self._configure_control_buttons_widgets()
        self._configure_options_widgets()
        self._configure_widget_mappings()

        super().__init__(*args, **kwargs)

    def _configure_options_widgets(self) -> None:
        widgets = []
        for option in self.options:
            widget = option.get_widget()
            widgets.append(widget)

        self.options_widgets = widgets

    def _configure_control_buttons_widgets(self) -> None:
        widgets = []
        for option in self.control_buttons:
            widget = option.get_widget()
            widgets.append(widget)

        self.control_buttons_widgets = widgets

    def _configure_widget_mappings(self):
        self._option_to_widget = {
            option: widget
            for option, widget in zip(self.options, self.options_widgets)
        }

        self._widget_to_option = {
            widget: option
            for option, widget in zip(self.options, self.options_widgets)
        }

        self._widget_to_control_button = {
            widget: option
            for option, widget in zip(
                self.control_buttons, self.control_buttons_widgets
            )
        }

    def convert_widget_to_option(
        self, widget: BaseOptionWidget
    ) -> SelectableOption:
        return self._widget_to_option[widget]

    def convert_option_to_widget(
        self, option: ConfigurableOption
    ) -> BaseOptionWidget:
        return self._option_to_widget[option]

    def conver_widget_to_control_button(
        self, widget: BaseOptionWidget
    ) -> SelectableOption:
        return self._widget_to_control_button[widget]

    def get_option_from_widget(
        self, widget: BaseOptionWidget
    ) -> SelectableOption:
        if widget in self._widget_to_option:
            return self._widget_to_option[widget]
        elif widget in self._widget_to_control_button:
            return self._widget_to_control_button[widget]
        else:
            raise ValueError(f"Provided widget is not know attribute of {self}")

    def compose(self) -> ComposeResult:
        yield SplittedOptionList(
            self.options_widgets,
            self.control_buttons_widgets,
            classes="option-list",
        )
        yield Rule(orientation="vertical")
        yield Markdown("This is an example", classes="option-description-field")

    @on(SplittedOptionList.OptionHiglighted)
    def on_option_highlighted(
        self, message: SplittedOptionList.OptionHiglighted
    ):
        descripion_field = self.query_one(Markdown)
        option = self.get_option_from_widget(message.option)
        descripion_field.update(option.description)
        message.stop()

    @on(SplittedOptionList.OptionSelected)
    def on_option_selected(self, message: SplittedOptionList.OptionSelected):
        option = self.get_option_from_widget(message.option)
        option.on_select()
