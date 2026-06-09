from textual.app import App
from textual.widgets import Label

from Components.Sessions.Sessions_gui import Sessions_gui
from Components.ConfigRepo.ConfigRepo_gui import ConfigRepo_gui
from Components.EasyGit.EasyGit_gui import EasyGit_gui

class main_app(App):
    CSS_PATH = "Components\\style.tcss"

    def compose(self):
        yield Sessions_gui(on_success=self.on_Sessions_gui_success)

    # Finalizando el objetivo de vida de Sessions_gui obtenemos la respuesta requerida
    def on_Sessions_gui_success(self, token):
        self.token = token                
        self.query_one(Sessions_gui).remove()
        self.mount(ConfigRepo_gui(token, on_success=self.on_ConfigRepo_gui_success))

    # Finalizando el objetivo de vida de Sessions_gui obtenemos la respuesta requerida
    def on_ConfigRepo_gui_success(self, root, remote):
        self.remote = remote        

        self.query_one(ConfigRepo_gui).remove()
        self.mount(EasyGit_gui())
        
if __name__ == "__main__":
    app = main_app()
    app.run()
