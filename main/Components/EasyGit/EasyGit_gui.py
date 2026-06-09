from textual.widgets import Static, Input
from textual.containers import Vertical
from textwrap import dedent

from tokens import *
from git_actions import *

class EasyGit_gui(Static):
    def __init__(self):
        super().__init__()
        
        self.id = "content_EasyGit"
        self.border_title = "Menu principal de opciones - EasyGit"

    def compose(self):
        menu_EasyGit = Static(dedent("""
            1- Iniciar sesion
            2- Registrar un token usuario nuevo
            3- Borrar usuario
            4- Actualizar ventana
        """), id="menu_EasyGit")

        menu_EasyGit.border_title = "Opciones del menu"

        yield menu_EasyGit
