from textual.widgets import Static, Input
from textual.containers import Vertical
from textwrap import dedent

from tokens import *
from git_actions import *

class Sessions_gui(Static):    
    # Configuracion del Widget
    # ------------------------------
    def __init__(self, on_success=None):
        super().__init__()
        
        self.id = "content_sessions"
        self.border_title = "Menu Inicial - Inicio / Registro de sesion"

        self.on_success = on_success        
        self.mode = "menu"

        self.user = ""
        self.password = ""
        self.token = ""        

    def compose(self):

        menu_sessions = Static(dedent("""
                1- Iniciar sesion
                2- Registrar un token usuario nuevo
                3- Borrar usuario
                4- Actualizar ventana
        """), id="menu_sessions")

        menu_sessions.border_title = "Opciones del menu"

        yield menu_sessions

        list_users_sessions = Static(dedent(self.render_list_users()), id="list_users_sessions")   

        list_users_sessions.border_title = "Lista de usuarios existentes"

        yield list_users_sessions
 
        yield Input(
            placeholder="Seleccione una opción...",
            id="input_sessions"
        )
        yield Static("", id="message")
    
    def on_input_submitted(self, event: Input.Submitted):

        # Extraemos el valor de el evento submit
        value = event.value.strip()
        
        # Creamos el objeto input_widget a base de la 
        # identificacion por ID (input_sessions) del elemento Input
        input_widget = self.query_one("#input_sessions", Input)

        if self.mode == "menu":

            # Modos iniciales estando en el menu (modo menu)
            match value:

                case "1":
                    self.mode = "get_user_login"
                    input_widget.value = ""
                    input_widget.placeholder = "Ingrese el usuario git"

                case "2":
                    self.mode = "get_user_register"
                    input_widget.value = ""
                    input_widget.placeholder = "Ingrese un nombre de usuario para registrar !"       

                case "3":
                    self.mode = "get_user_delete"
                    input_widget.value = ""
                    input_widget.placeholder = "Ingrese el usuario git !"

        # Funcionalidades por modo
        elif self.mode == "get_user_login":
            self.login(value, input_widget)

        elif self.mode == "get_password_login":    
            self.login(value, input_widget)  

        elif self.mode == "get_user_register":
            self.register(value, input_widget)

        elif self.mode == "get_password_register":
            self.register(value, input_widget)

        elif self.mode == "get_token_register":
            self.register(value, input_widget)

        elif self.mode == "get_user_delete":
            self.delete(value, input_widget)            

    def render_list_users(self):
        list_users_local = list_users()        

        for user_index in range(0, len(list_users_local)):
            list_users_local[user_index] = f"{user_index+1}- {list_users_local[user_index]}"
            
        return "\n".join(list_users_local)

    def delete(self, value, input_widget):
        user = value

        if self.mode == "get_user_delete":
            del_user(user=user)
            self.notify(f"Usuario {user} borrado !")
                
        # Limpieza de alertas
        message = self.query_one("#message", Static)
        message.update(f"")
            
        self.mode = "menu"        
        input_widget.value = ""
        input_widget.placeholder = "Ingrese el usuario git"
        return
    
    def register(self, value, input_widget):    
        if self.mode == "get_user_register":
            user = value

            users = list_users()

            # Validacion de existencia del usuario
            if user in users:                
                message = self.query_one("#message", Static)
                message.update(f"El usuario {user} ya se encuentra registrado !")

                self.mode = "get_user_register"
                input_widget.value = ""
                input_widget.placeholder = "Ingrese un nombre de usuario nuevo para registrar !"       
                return  
            
            # Antes de Seguir con el proceso guardamos el usuario globalmente
            self.user = ""
            self.user = value
            
            # Limpieza de alertas
            message = self.query_one("#message", Static)
            message.update(f"")
            
            # Continuamos con el proceso de obtencion del token
            self.mode = "get_token_register"
            input_widget.value = ""
            input_widget.placeholder = "Ingrese el token del usuario que quiere registrar"
            return
        
        elif self.mode == "get_token_register":
            token = value

            # Validamos que el token ingresado no este vencido            
            if not vigenci_token(token=token):  
                message = self.query_one("#message", Static)
                message.update(f"El token ingresado ya se encuentra vencido o no existe!")

                self.mode = "get_token_register"
                input_widget.value = ""
                input_widget.placeholder = "Ingrese otro token que no este vencido !"
                return
            
            # Antes de seguir con el proceso guardamos el token globalmente
            self.token = ""
            self.token = token

            # Limpieza de alertas
            message = self.query_one("#message", Static)
            message.update(f"")

            # Continuamos con el proceso de obtencion del password
            self.mode = "get_password_register"
            input_widget.value = ""
            input_widget.placeholder = "Ingrese la contraseña maestra !"
            return
        
        elif self.mode == "get_password_register":
            password = value
            user = self.user
            token = self.token

            if set_token(user=user, token=token, password=password):
                self.notify(f"El usuario {user} a sido registrado con exito !")     
            else:
                self.notify(f"El usuario {user} no a podido ser registrado !")     

            self.user = ""
            self.token = ""
            self.password = ""

            # Limpieza de alertas
            message = self.query_one("#message", Static)
            message.update(f"")

            # Continuamos reenviando al usuario registrado al 
            # menu para que inicie sesion
            self.mode = "menu"
            input_widget.value = ""
            input_widget.placeholder = "Seleccione una opción..."
            return
                        
    def login(self, value, input_widget):            
        if self.mode == "get_user_login":            
            user = value
            users = list_users()

            # Validacion de existencia del usuario
            if user not in users:                
                message = self.query_one("#message", Static)
                message.update(f"El usuario {user} no esta registrado aun !")

                self.mode = "get_user_login"
                input_widget.value = ""
                input_widget.placeholder = "Ingrese el usuario git"       
                return  

            self.user = user

            # Limpieza de alertas
            message = self.query_one("#message", Static)
            message.update(f"")
            
            # Continuamos con el proceso de obtencion del password
            self.mode = "get_password_login"
            input_widget.value = ""            
            input_widget.placeholder = "Ingrese contraseña !"              

            return
        elif self.mode == "get_password_login":
            user = self.user            
            password = value

            # Logica Login
            token = get_token(user=user, password=password)    
                
            # Validacion de la obtencion token (Respuesta Login)
            if token is None:                                
                message = self.query_one("#message", Static)
                message.update(f"Clave incorrecta !!")

                self.mode = "get_user_login"
                input_widget.value = ""
                input_widget.placeholder = "Ingrese el usuario git !"
                return

            # Validacion de la vigencia del token una vez obtenido
            if not vigenci_token(token=token):                
                message = self.query_one("#message", Static)
                message.update(f"El token esta vencido !. Registrese de nuevo.")
                del_user(user=user) 

                self.mode = "get_user_login"
                input_widget.value = ""
                input_widget.placeholder = "Ingrese el usuario git !"
                return        

            self.notify(f"Sesion iniciada {user} !")               
                      
            # Limpieza de alertas
            message = self.query_one("#message", Static)
            message.update(f"")
            
            if self.on_success:
                self.on_success(token)