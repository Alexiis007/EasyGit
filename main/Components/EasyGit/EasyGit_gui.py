from textual.widgets import Static, Input
from textual.containers import Vertical
from textwrap import dedent

from tokens import *
from git_actions import *

class EasyGit_gui(Static):
    def __init__(self, root, remote, token):
        super().__init__()
        
        # Configuracion inicial del apartado EasyGit_gui
        self.id = "content_EasyGit"
        self.border_title = "Menu principal de opciones - EasyGit"

        # Variables usadas
        self.root = root
        self.remote = remote
        self.token = token

        # Variable de Modo inicial
        self.mode = "Inicio"

    def compose(self):
        update_local(root=self.root)  
        
        # Obtencion de data relacionada a ramas
        data_branches = get_branches(root=self.root)        

        #Obtencion de la rama activa
        active_branch = data_branches["active_branch"] 

        # Obtencion de lista de ramas
        branches_status = data_branches["branches_status"]
        # Conversion de lista a string
        branches_status = "\n".join(branches_status)
        # Creacion de widget para la muestra de estatus de las ramas
        ramas_EasyGit = Static(dedent(branches_status), id="ramas_EasyGit")
        ramas_EasyGit.border_title = "Ramas existentes en el repositorio"
        yield ramas_EasyGit

        # Obtencion de los cambios nuevos realizados y el conteo de los mismos
        commits_not_stage, commits_not_stage_count = self.modified_files_list(active_branch=active_branch)
        # Creacion de widget para la muestra de estatus de los cambios realizados
        modified_files_EasyGit = Static(commits_not_stage, id="modified_files_EasyGit")
        modified_files_EasyGit.border_title = f"-> Archivos modificados({commits_not_stage_count}) - {active_branch}:"
        yield modified_files_EasyGit

        # Obtencion de los archivos nuevos creados y el conteo de los mismos
        untracked_files, untracked_files_count = self.new_files_list(active_branch=active_branch)
        # Creacion de widget para la muestra de estatus de los archivos nuevos creados
        new_files_EasyGit = Static(untracked_files, id="new_files_EasyGit")
        new_files_EasyGit.border_title = f"-> Archivos nuevos creados({untracked_files_count}) - {active_branch}:"
        yield new_files_EasyGit

        # Obtencion de las opciones actuales de EasyGit (Las opciones se definen dentro de la funcion)
        options_menu = self.options_menu_lists(active_branch=active_branch)
        # Creacion de menu principal de EasyGit
        menu_EasyGit = Static(dedent(options_menu), id="menu_EasyGit")
        menu_EasyGit.border_title = "Opciones del menu"
        yield menu_EasyGit

        # Creacion y muestreo de widget Input para la obtencion de datos
        yield Input(placeholder="Selecciona una opcion:", id="input_EasyGit")

    def on_input_submitted(self, event:Input.Submitted):
        # Obtencion del valor captado por el evento Submitted
        value = event.value.strip()
        # Creacion de objeto de control por ID del Widget #input_EasyGit
        input_widget = self.query_one("#input_EasyGit", Input)

        # Modos iniciales
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
            commits_not_stage_str += f"{count}- Archivo modificado: {i.replace("\tmodified:   ", "")}\n"

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
            untracked_files_str += f"{count}- Nuevo archivo detectado: {i.replace("\t", "")}\n"

        if count == 0:
            return "No hay archivos nuevos detectados.", count
        else:
            return untracked_files_str, count

    def options_menu_lists(self, active_branch):
        # Nombre de la opcion, funcionalidad y condicion para limpiar pantalla con mensaje bonito
        options = [
            ["Cambiar rama de trabajo", lambda:change_branch(root=self.root, remote=self.remote, active_branch=active_branch), True],      #1
            ["Realizar un commit", lambda:commit(root=self.root, remote=self.remote, push=False, active_branch=active_branch), True],           #2
            ["Realizar un commit + push", lambda:commit(root=self.root, remote=self.remote, push=True, active_branch=active_branch), True],    #3
            ["Crear una rama", lambda:new_branch(root=self.root, remote=self.remote), True],              #4
            ["Borrar rama", lambda:del_branch(root=self.root, remote=self.remote, active_branch=active_branch), True],                  #5            
            ["Realizar merge", lambda:merge(root=self.root, active_branch=active_branch), True],               #6
            ["Insertar Comando", "", True], #7
            ["Historial de commits", lambda:hist_commits(root=self.root, active_branch=active_branch), True],         #8
            ["Abrir explorador de Windows", lambda:command_exec("explorer .", cwd=self.root), False],  #9
            ["Actualizar Ventana", lambda:subprocess.run("cls", shell=True), False],           #10
            ["Abrir repo - Web", lambda:command_exec(f"start {self.remote}", cwd=self.root), False],      #11
            ["Empujar rama", lambda:push_branch_to_remote(root=self.root, remote=self.remote), True],        #12
            ["Cerrar sesion", "", False]                 #13            
        ]

        options_lists_str = ""

        # Pintado de las opciones
        side = 0 # Side inicia en 0 (0=izquierdo, 1=derecho)
        index = 0
        for i in options:        
            i = i[0]
            index+=1

            # Lado izquierdo 0
            if side == 0:
                line = i    
                side += 1                
                if side == 1 and i == options[-1][0]:                                
                    options_lists_str += f"{index}- {line}\n"

            # Lado derecho 1
            elif side == 1:     
                
                # Agregado de espaciado lateral derecho.
                # A partir de 10 se aumenta en 1 
                # el espacio por lo que se corrige restando 1.
                if index > 10:           
                    line += f" "*(32-len(line))
                else:
                    line += f" "*(33-len(line))

                options_lists_str += f"{index-1}- {line}{index}- {i}\n"
                side = 0     

        return options_lists_str     