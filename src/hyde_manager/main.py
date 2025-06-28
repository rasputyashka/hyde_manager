from hyde_manager.installer.main import Installer
from hyde_manager.app.base import Application

OPTION_TO_CONTAINER_CLASS = {"install": Installer}


def get_app(option) -> Application:
    container = OPTION_TO_CONTAINER_CLASS[option]
    app = Application(container)
    return app


def main(option):
    app = get_app(option)
    app.run(mouse=False)


if __name__ == "__main__":
    # used more for developing purpuses (so it's possible to run )
    # textual run main.py --dev
    main("install")
