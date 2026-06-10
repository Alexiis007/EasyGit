from textual.app import App
from textual.widgets import Label, Static

from tools import *

from Components.Sessions.Sessions_gui import Sessions_gui
from Components.ConfigRepo.ConfigRepo_gui import ConfigRepo_gui
from Components.EasyGit.EasyGit_gui import EasyGit_gui
from textwrap import dedent

class main_app(App):
    CSS_PATH = "Components\\style.tcss"

    # Arranque de la primera seccion (Widget Sessions)
    def compose(self):
        # Se imprime el arte a nivel global
        self.arte = Static(dedent("""
      ███████╗ █████╗ ███████╗██╗   ██╗ ██████╗ ██╗████████╗
      ██╔════╝██╔══██╗██╔════╝╚██╗ ██╔╝██╔════╝ ██║╚══██╔══╝
    █████╗  ███████║███████╗ ╚████╔╝ ██║  ███╗██║   ██║
    ██╔══╝  ██╔══██║╚════██║  ╚██╔╝  ██║   ██║██║   ██║
    ███████╗██║  ██║███████║   ██║   ╚██████╔╝██║   ██║
    ╚══════╝╚═╝  ╚═╝╚══════╝   ╚═╝    ╚═════╝ ╚═╝   ╚═╝
        """), id="logo")
        self.arte.border_title = "Alexsis007"
        yield self.arte

        # Se inicia widget de Sessions y se liga on_succes para dar comienzo
        # a la siguiente pantalla
        yield Sessions_gui(on_success=self.on_Sessions_gui_success)

    # Finalizando el objetivo de vida de Sessions_gui obtenemos la respuesta requerida
    def on_Sessions_gui_success(self, token):
        # Guardamos el retorno del on_Sessions_gui_success
        self.token = token                
        
        # Desmontamos Sessions_gui
        self.query_one(Sessions_gui).remove()
        # Corremos la siguiente logica - ConfigRepo_gui Widget y le ligamos igualmente
        # un on_succes para obtener su finalidad. Y en este caso le enviamos el token tambien
        self.mount(ConfigRepo_gui(token, on_success=self.on_ConfigRepo_gui_success))

    # Finalizando el objetivo de vida de Sessions_gui obtenemos la respuesta requerida
    def on_ConfigRepo_gui_success(self, root, remote):
        # Guardamos las variables obtenidas por la anterior pantalla (ConfigRepo_gui Widget)
        self.remote = remote        
        self.root = root        

        # Desmontamos ConfigRepo_gui
        self.query_one(ConfigRepo_gui).remove()
        # Corremos la siguiente logica - EasyGit_gui Widget y le enviamos los 
        # parametros requeridos
        self.mount(EasyGit_gui(self.root, self.remote, self.token))
        
if __name__ == "__main__":
    app = main_app()
    app.run()
