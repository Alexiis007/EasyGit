from textual.widgets import Static, Input
from textual.containers import Vertical
from textwrap import dedent

from tokens import *
from git_actions import *

class EasyGit_gui(Static):
    def __init__(self, root, remote, token):
        super().__init__()
        
        self.id = "content_EasyGit"
        self.border_title = "Menu principal de opciones - EasyGit"

        self.root = root
        self.remote = remote
        self.token = token

        self.mode = "Inicio"

    def compose(self):
        update_local(root=self.root)  
        
        data_branches = get_branches(root=self.root)        
        branches_status = data_branches["branches_status"]
        branches_status = "\n".join(branches_status)
        active_branch = data_branches["active_branch"] 

        ramas_EasyGit = Static(dedent(branches_status), id="ramas_EasyGit")
        ramas_EasyGit.border_title = "Ramas existentes en el repositorio"
        yield ramas_EasyGit

        commits_not_stage, commits_not_stage_count = self.modified_files_list(active_branch=active_branch)
        modified_files_EasyGit = Static(commits_not_stage, id="modified_files_EasyGit")
        modified_files_EasyGit.border_title = f"-> Archivos modificados({commits_not_stage_count}) - {active_branch}:"
        yield modified_files_EasyGit

        untracked_files, untracked_files_count = self.new_files_list(active_branch=active_branch)
        new_files_EasyGit = Static(untracked_files, id="new_files_EasyGit")
        new_files_EasyGit.border_title = f"-> Archivos nuevos creados({untracked_files_count}) - {active_branch}:"
        yield new_files_EasyGit

        status_EasyGit = Static("", id="status_EasyGit")
        status_EasyGit.border_title = f"Estatus de rama actual - {active_branch}:"
        yield status_EasyGit

        menu_EasyGit = Static(dedent("""
            1- Iniciar sesion
            2- Registrar un token usuario nuevo
            3- Borrar usuario
            4- Actualizar ventana
        """), id="menu_EasyGit")
        menu_EasyGit.border_title = "Opciones del menu"
        yield menu_EasyGit

        yield Input(placeholder="Selecciona una opcion:", id="input_EasyGit")

    def on_input_submitted(self, event:Input.Submitted):
        value = event.value.strip()

        input_widget = self.query_one("#input_EasyGit", Input)

        if self.mode == "Inicio":
            match value:
                case "1":
                    self.mode = "get_root_local_repo"
                    input_widget.value = ""
                    input_widget.placeholder = "Digite la ruta de trabajo (Donde este el archivo .git):"
                case "2":
                    self.mode = "get_https_clon_repo"
                    input_widget.value = ""
                    input_widget.placeholder = "Ingrese el HTTPS de su repo:"
                case "3":
                    self.mode = "get_https_new_repo"
                    input_widget.value = ""
                    input_widget.placeholder = "Ingrese el HTTPS de su nuevo repo (Antes crealo en git):"
        

    def modified_files_list(self, active_branch:str):
        # Listado de archivos modificados                        
        commits_not_stage = status(self.root, active_branch=active_branch)["commits_not_stage"]        
        commits_not_stage_str = ""
        
        count = 0
        for i in commits_not_stage:
            count+=1
            commits_not_stage_str += f"\n{count}- Archivo modificado: {i.replace("\tmodified:   ", "")}"

        if count == 0:
            return "No hay archivos modificados.", count
        else:
            return commits_not_stage_str, count
    
    def new_files_list(self, active_branch:str):
        # Listado de archivos nuevos
        untracked_files = status(self.root, active_branch=active_branch)["untracked_files"]        
        untracked_files_str = ""

        count = 0
        for i in untracked_files:
            count+=1
            untracked_files_str += f"\n{count}- Nuevo archivo detectado: {i.replace("\t", "")}"

        if count == 0:
            return "No hay archivos nuevos detectados.", count
        else:
            return untracked_files_str, count
