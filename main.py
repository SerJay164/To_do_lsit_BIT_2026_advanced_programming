from nicegui import ui

import gui
from gui import APP_NAME


def main():
    ui.run(
        title=APP_NAME,
        reload=False,
    )


if __name__ == "__main__":
    main()

