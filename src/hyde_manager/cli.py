import sys

from hyde_manager.main import get_app, OPTION_TO_CONTAINER_CLASS


USAGE_MESSAGE = f"""USAGE: hyde OPTION

OPTIONS:
    {"\n\t".join(OPTION_TO_CONTAINER_CLASS.keys())}
"""


def main():
    if (
        len(sys.argv) != 2
        or sys.argv[1] not in OPTION_TO_CONTAINER_CLASS.keys()
    ):
        print(USAGE_MESSAGE)
        exit(1)

    option = sys.argv[1]
    app = get_app(option)

    app.run()
