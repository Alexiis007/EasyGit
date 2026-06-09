from textual.app import App
from textual.widgets import Label

from Components.Sessions.Sessions_gui import Sessions_gui
from Components.ConfigRepo.ConfigRepo_gui import ConfigRepo_gui
from Components.EasyGit.EasyGit_gui import EasyGit_gui

class main_app(App):
    CSS_PATH = "Components\\style.tcss"

    def compose(self):
        yield Sessions_gui(on_success=self.on_login_success)

    def on_login_success(self, token):
        self.token = token                
        self.query_one(Sessions_gui).remove()
        self.mount(ConfigRepo_gui())
        
if __name__ == "__main__":
    app = main_app()
    app.run()
