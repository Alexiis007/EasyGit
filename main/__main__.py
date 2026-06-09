# Para la ejecucion de comandos
import subprocess

# Importacion de herramientas de trabajo
from tools import *

# Importacion de funciones git
from git_actions import *

# Funcionalidad para el uso de sesiones - tokens
from tokens import *

from main.app import *

art_number = 3

def main():
    logger(msg="-"*60, level="info")
    logger(msg="main() - Iniciando CLI", level="info")        
    logger(msg="-"*60, level="info")
    
    # subprocess.run("color 0A", shell=True)                        

    # Inicio de sesion / Registro de sesion (Menu)
    # token = sessions()    

    flag = True
    while flag:
        subprocess.run("cls", shell=True)                        
        art(art_number)        
        print("-"*60)  

        pretty_printer("Iniciar en repo existente o crear un espacio nuevo:")
        pretty_printer("\t1- Trabajar sobre un repo local existente")
        pretty_printer("\t2- Crear un espacio nuevo (Clonacion de repo)")
        pretty_printer("\t3- Crear un repositorio nuevo")    
        try:
            working_option = int(pretty_printer("R=", inputF=True))
        except:
            working_option = ""
                
        print("-"*60)    

        if working_option == 1:
            root = get_workspace()                         
            remote = set_remote_token(root=root, token=token)
            flag = False            
        elif working_option == 2:
            root, remote = clone(token=token)                    
            pretty_printer("Pulse enter para continuar:", inputF=True)                
            subprocess.run("cls", shell=True)
            flag = False
        elif working_option == 3:       
            root, remote = new_repo(token=token)             
            pretty_printer("Pulse enter para continuar:", inputF=True)                
            subprocess.run("cls", shell=True)
            flag = False        

    update_local(root=root)            
    subprocess.run("cls", shell=True)                    

    # Menu de acciones - EasyGit
    while True:         
        art(art_number)                      
        print("-"*60)  

        data_branches = get_branches(root=root)
        active_branch = data_branches["active_branch"]                   
        branches_status = data_branches["branches_status"]

        pretty_printer("Ramas existentes en el repositorio:") 
        print("-"*60) 

        for branch in branches_status:
            pretty_printer(f"{branch}")                          
  
        print("-"*60)  
        status(root=root, active_branch=active_branch)                
        print("-"*60)  
        pretty_printer("Que deseas realizar:")    
        print("-"*60)  

        # Nombre de la opcion, funcionalidad y condicion para limpiar pantalla con mensaje bonito
        options = [
            ["Cambiar rama de trabajo", lambda:change_branch(root=root, remote=remote, active_branch=active_branch), True],      #1
            ["Realizar un commit", lambda:commit(root=root, remote=remote, push=False, active_branch=active_branch), True],           #2
            ["Realizar un commit + push", lambda:commit(root=root, remote=remote, push=True, active_branch=active_branch), True],    #3
            ["Crear una rama", lambda:new_branch(root=root, remote=remote), True],              #4
            ["Borrar rama", lambda:del_branch(root=root, remote=remote, active_branch=active_branch), True],                  #5            
            ["Realizar merge", lambda:merge(root=root, active_branch=active_branch), True],               #6
            ["Insertar Comando", "", True], #7
            ["Historial de commits", lambda:hist_commits(root=root, active_branch=active_branch), True],         #8
            ["Abrir explorador de Windows", lambda:command_exec("explorer .", cwd=root), False],  #9
            ["Actualizar Ventana", lambda:subprocess.run("cls", shell=True), False],           #10
            ["Abrir repo - Web", lambda:command_exec(f"start {remote}", cwd=root), False],      #11
            ["Empujar rama", lambda:push_branch_to_remote(root=root, remote=remote), True],        #12
            ["Cerrar sesion", lambda:main(), False]                 #13            
        ]

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
                    pretty_printer(f"{index}- {line}")                    

            # Lado derecho 1
            elif side == 1:     
                
                # Agregado de espaciado lateral derecho.
                # A partir de 10 se aumenta en 1 
                # el espacio por lo que se corrige restando 1.
                if index > 10:           
                    line += f" "*(32-len(line))
                else:
                    line += f" "*(33-len(line))

                pretty_printer(f"{index-1}- {line}{index}- {i}")
                side = 0                            

        print("-"*60)  
        option = only_int_options(max_number_option=len(options), zero_start=False)
        print("-"*60)  
        
        options[option-1][1]()  

        # Estructura de limpieza de pantalla post funcion - detalle estetico
        if options[option-1][2]:
            print()
            print("-"*60)  
            pretty_printer(f"Tarea finalizada con exito !")
            print("-"*60)  
            pretty_printer("Pulse enter para continuar:", inputF=True)                
            subprocess.run("cls", shell=True)
        else:
            subprocess.run("cls", shell=True) 
        
if __name__ == "__main__":
    # main()

    app = main_app()
    app.run()
