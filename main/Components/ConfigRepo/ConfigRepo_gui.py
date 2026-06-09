from textual.widgets import Static, Input
from textual.containers import Vertical
from textwrap import dedent

from tokens import *
from git_actions import *

class ConfigRepo_gui(Static):
    def __init__(self, token, on_success=None):
        super().__init__()
        
        self.id = "content_ConfigRepo"
        self.border_title = "Menu de configuracion de inicio - Repositorio"

        self.on_success = on_success

        self.token = token
        self.mode = "Inicio"
        self.root = ""        
        self.https = ""
        self.user = ""

    def compose(self):
        menu_ConfigRepo = Static(dedent("""
            1- Trabajar sobre un repo local existente
            2- Crear un espacio nuevo (Clonacion de repo)
            3- Crear un repositorio nuevo
        """), id="menu_ConfigRepo")

        menu_ConfigRepo.border_title = "Iniciar en repo existente o crear un espacio nuevo"

        yield menu_ConfigRepo

        yield Input(
            placeholder="Seleccione una opción...",
            id="input_ConfigRepo"
        )
        
        yield Static("", id="message")

    def on_input_submitted(self, event: Input.Submitted):
        value = event.value.strip()

        input_widget = self.query_one("#input_ConfigRepo", Input)
        
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

        elif self.mode == "get_root_local_repo":
            self.local_repository(value, input_widget)
        elif self.mode == "get_https_clon_repo":
            self.clone_repository(value, input_widget)
        elif self.mode == "get_user_clon_repo":
            self.clone_repository(value, input_widget)
        elif self.mode == "get_root_clon_repo":
            self.clone_repository(value, input_widget)

    def new_repository(self, value, input_widget):
        if self.mode == "get_https_new_repo":
            self.https = ""
            self.https = value.strip()

            if self.https == "":
                message = self.query_one("#message", Static)
                message.update(f"Por favor ingrese un HTTPS de repositorio correcto !")                

                self.mode = "get_https_new_repo"
                input_widget.value = ""
                input_widget.placeholder = "Ingrese el HTTPS de su nuevo repo (Antes crealo en git):"
                return            

            message = self.query_one("#message", Static)
            message.update(f"")                

            self.mode = "get_user_new_repo"
            input_widget.value = ""
            input_widget.placeholder = "Ingrese el nombre de su usuario en git:"
            return    
        
        elif self.mode == "get_user_new_repo":
            self.user = ""
            self.user = value

            if self.user == "":
                message = self.query_one("#message", Static)
                message.update(f"Por favor ingrese un usuario de git correcto !")                

                self.mode = "get_user_new_repo"
                input_widget.value = ""
                input_widget.placeholder = "Ingrese el nombre de su usuario en git:"
                return       

            message = self.query_one("#message", Static)
            message.update(f"")                

            self.mode = "get_root_new_repo"
            input_widget.value = ""
            input_widget.placeholder = "Ingresa la ruta local donde desea comenzar su nuevo repo:"
            return    

        elif self.mode == "get_root_new_repo":
            self.root = ""
            self.root = value

            repo_name = self.https.split("/")[-1].replace(".git", "")

            if self.root == "":
                message = self.query_one("#message", Static)
                message.update(f"Por favor revisa bien donde crearas tu repo !")                

                self.mode = "get_root_new_repo"
                input_widget.value = ""
                input_widget.placeholder = "Ingresa la ruta local donde desea comenzar su nuevo repo:"
                return   
            
            if os.path.exists(os.path.join(self.root, repo_name)):
                message = self.query_one("#message", Static)
                message.update(f"Ya existe un directorio (repo) con el nombre {repo_name} en la ruta {self.root}")                

                self.mode = "get_root_new_repo"
                input_widget.value = ""
                input_widget.placeholder = "Ingresa la ruta local donde desea comenzar su nuevo repo:"
                return   
            
            root, remote = new_repo(https=self.https, user=self.user, root=self.root, repo_name=repo_name)

            self.notify("Creacion de repositorio completa")

            # Limpieza de alertas
            message = self.query_one("#message", Static)
            message.update(f"")

            if self.on_success:
                self.on_success(root, remote)

    def clone_repository(self, value, input_widget):
        if self.mode == "get_https_clon_repo":
            self.https = ""
            self.https = value.strip()

            if self.https == "":
                message = self.query_one("#message", Static)
                message.update(f"Por favor ingrese un HTTPS de repositorio correcto !")                

                self.mode = "get_https_clon_repo"
                input_widget.value = ""
                input_widget.placeholder = "Ingrese el HTTPS de su repo:"
                return            

            message = self.query_one("#message", Static)
            message.update(f"")                

            self.mode = "get_user_clon_repo"
            input_widget.value = ""
            input_widget.placeholder = "Ingrese el nombre de su usuario en git:"
            return    
        
        elif self.mode == "get_user_clon_repo":
            self.user = ""
            self.user = value

            if self.user == "":
                message = self.query_one("#message", Static)
                message.update(f"Por favor ingrese un usuario de git correcto !")                

                self.mode = "get_user_clon_repo"
                input_widget.value = ""
                input_widget.placeholder = "Ingrese el nombre de su usuario en git:"
                return       

            message = self.query_one("#message", Static)
            message.update(f"")                

            self.mode = "get_root_clon_repo"
            input_widget.value = ""
            input_widget.placeholder = "Ingresa la ruta local donde deseas crear el repo:"
            return    

        elif self.mode == "get_root_clon_repo":
            self.root = ""
            self.root = value

            repo_name = self.https.split("/")[-1].replace(".git", "")  

            if self.root == "":
                message = self.query_one("#message", Static)
                message.update(f"Por favor revisa bien donde crearas tu repo !")                

                self.mode = "get_root_clon_repo"
                input_widget.value = ""
                input_widget.placeholder = "Ingresa la ruta local donde deseas crear el repo:"
                return   
            
            if os.path.exists(os.path.join(self.root, repo_name)):
                message = self.query_one("#message", Static)
                message.update(f"Ya existe un directorio (repo) con el nombre {repo_name} en la ruta {self.root}")                

                self.mode = "get_root_clon_repo"
                input_widget.value = ""
                input_widget.placeholder = "Ingresa la ruta local donde deseas crear el repo:"
                return   
            
            root, remote = clone(token=self.token, user=self.user, root=self.root, repo_name=repo_name)

            self.notify("Clonacion de repositorio completa")

            # Limpieza de alertas
            message = self.query_one("#message", Static)
            message.update(f"")

            if self.on_success:
                self.on_success(root, remote)

    def local_repository(self, value, input_widget):
        if self.mode == "get_root_local_repo":
            root = value.strip()

            root = get_workspace(root=root)

            if root == False:             
                message = self.query_one("#message", Static)
                message.update(f"Ruta erronea !")
                    
                self.mode = "get_root_local_repo"        
                input_widget.value = ""
                input_widget.placeholder = "Digite la ruta de trabajo (Donde este el archivo .git):"
                return
            elif len(root) <= 0:
                message = self.query_one("#message", Static)
                message.update(f"Ruta erronea !")
                    
                self.mode = "get_root_local_repo"        
                input_widget.value = ""
                input_widget.placeholder = "Digite la ruta de trabajo (Donde este el archivo .git):"
                return

            remote = set_remote_token(root=root, token=self.token)

            self.notify("Repositorio local iniciado")

            # Limpieza de alertas
            message = self.query_one("#message", Static)
            message.update(f"")
                
            if self.on_success:
                self.on_success(root, remote)