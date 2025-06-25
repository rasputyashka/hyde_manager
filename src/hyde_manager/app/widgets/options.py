from hyde_manager.app.widgets.base import ConfigurableOption
from hyde_manager.app.screens.boolean_modal import BooleanModal


class BooleanOption(ConfigurableOption):
    def get_configuration_window(self):
        return BooleanModal(self.name, self.description)


class ChoicesOption(ConfigurableOption):
    pass


class OneOfOption(ConfigurableOption):
    pass
