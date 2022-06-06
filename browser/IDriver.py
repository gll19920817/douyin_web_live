class IDriver():
    def new_tab(self) -> str:
        ...

    def change_tab(self, tab_handler: str):
        ...

    def open_url(self, url: str, tab_handler: str = ""):
        ...

    def screenshot(self, tab_handler: str = "") -> str:
        ...