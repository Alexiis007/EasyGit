# Recolecolector de basura
import gc

# Para logs
import logging

# Para el metodo de escritura 
import sys
import time

# Para la ejecucion de comandos
import subprocess

import os

# Logger Config
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def pretty_printer(txt: str, inputF:bool = False, fast=False):
    
    if fast:
        sys.stdout.write(txt)
    else:
        for letra in txt:
            sys.stdout.write(letra)
            sys.stdout.flush()

            if letra in ".,:":
                time.sleep(0.3)
            elif letra == " ":
                time.sleep(0.10)
            else:
                time.sleep(0.05)

    if not inputF:        
        print()
        return None
    else:        
        return input()

def command_exec(command:str, cwd:str, response:bool = False):        
    if not response:
        try:            
            subprocess.run(command, shell=True, cwd=cwd)
        except:
            pretty_printer(f"Error al ejecutar el comando '{command}'...")
            return None
        return None
    else:
        try:            
            output = subprocess.run(command, shell=True, capture_output=True, text=True, cwd=cwd)    
        except:
            pretty_printer(f"Error al ejecutar el comando '{command}'...")
            return None
        return output.stdout 

def get_workspace():
    # logger.info("get_workspace - Obtencion de espacio de trabajo.")
    # print("-"*70)

    flag = True
    while flag:
        root = pretty_printer("Digite la ruta de trabajo (Donde este el archivo .git): ", inputF=True)    
        root = root.strip()

        if len(root) != 0 and os.path.exists(root):
            flag = False            
        else:
            pretty_printer("Ruta erronea !!!")
            print("-"*70)
        
    pretty_printer("Verificando la existencia del archivo .git")
    
    list_dir = command_exec("dir /a", cwd=root, response=True)

    if not ".git" in list_dir:
        command_exec("cls", root)
        logger.error("get_workspace - Obtencion de espacio de trabajo. Ruta incorrecta.")
        print("-"*70)
        pretty_printer("La ruta de trabajo establecida no contiene una archivo .git.")
        pretty_printer("Por favor intente de nuevo.")
        print("-"*70)
        get_workspace()
    else:
        pretty_printer("Archivo .git encontrado.")
        pretty_printer("Ruta establecida !")                

    print("-"*70)

    return root

def set_token(root:str):
    # logger.info("setToken - Establecimiento del token.")
    # print("-"*70)

    remote_root = command_exec("git remote -v", response=True, cwd=root)
    remote_root = str(remote_root).split("\n")[0].replace("\t", " ").split(" ")    

    remote_root_token = ""

    for i in remote_root:
        if "http" in i:
            remote_root_token = i

    user = remote_root_token.split("/")[3]

    command_exec(f""" git config user.name "{user}" """, cwd=root)
    command_exec(f""" git config user.email "{user}@github.com" """, cwd=root)

    token = pretty_printer(f"Por favor ingrese un token de trabajo para el usuario {user}: ", inputF=True)        

    # Si el remote_root (origin) fue registrado con un token en algun momento
    # Cambiamos el token clavado por el ingresado en dado caso de que este vencido
    # Sino tenia token registrado avanzamos y lo registramos por primera vez aqui en el else
    if f"{user}:" in remote_root_token:                                
        remote_root_token = f"https://{user}:{token}@github.com/{user}/{remote_root_token.split("/")[-1]}"
    else:
        remote_root_token = remote_root_token.replace("github.com", f"{user}:{token}@github.com")    

    return remote_root_token

def get_branches(root:str):
    # logger.info("get_branches - Obtencion de ramas en el repositorio remoto.")
    # print("-"*70)

    pretty_printer("Ramas existentes en el espacio de trabajo:")    

    res = command_exec("git branch", response=True, cwd=root)
    
    active_branch = ""

    for i in res.split('\n'):
        if len(str(i)) > 0:
            pretty_printer(f"- {i}")
        if "*" in i:
            active_branch = i.split(" ")[-1]
        
    pretty_printer(f"-> Rama activa: {active_branch}")    

    return active_branch

def change_branch(root:str, remote:str, active_branch:str):
    # # logger.info("change_branch - Cambio de rama de trabajo.")
    # # print("-"*70)

    pretty_printer("A que rama desea cambiar:")
    branch = pretty_printer("Opcion: ", inputF=True)

    pretty_printer(f"Esta cambiando de la rama {active_branch} a la rama {branch}.")
    pretty_printer(f"Antes es necesario guardar los cambios de su rama activa actual...")
    pretty_printer(f"\t1- Cancela todo y regresemos")
    pretty_printer(f"\t2- Guardemos todo ahora mismo")
    pretty_printer(f"\t3- Si ya todo esta guardado, solo continuemos")
    option = int(pretty_printer(f"Opcion:", inputF=True))

    if option == 1:
        return
    elif option == 2:
        commit = pretty_printer(f"Denos un mensaje de commit:", inputF=True)
        command_exec(f'''git add .''', cwd=root)
        command_exec(f'''git commit -m "{commit}"''', cwd=root, response=True)
        command_exec(f'''git push -u {remote} {active_branch}''', cwd=root, response=True)
        command_exec(f'''git switch {branch}''', cwd=root, response=True)
    else:
        command_exec(f'''git switch {branch}''', cwd=root, response=True)

    update_local(root=root)        

def commit(root:str, remote:str, push:bool, active_branch:str):
    # # logger.info("change_branch - Cambio de rama de trabajo.")
    # # print("-"*70)

    pretty_printer("Opcion de guardado: ")
    pretty_printer("\t1- Guardar todo")
    pretty_printer("\t2- Especificar archivos:")
    option = int(pretty_printer("R=", inputF=True)) 

    command_exec(f'''git fetch''', cwd=root, response=True)    

    if option == 1:
        commit = pretty_printer(f"Denos un mensaje de commit:", inputF=True)            
        command_exec(f'''git add .''', cwd=root)
        command_exec(f'''git commit -m "{commit}"''', cwd=root, response=True)                
    elif option == 2:
        print("En desarrollo...")
    else:
        print()

    if push:        
        command_exec(f'''git push -u {remote} {active_branch}''', cwd=root, response=True)
        command_exec(f'''git fetch''', cwd=root, response=True)    

def new_branch(root:str, remote:str):
    # # logger.info("change_branch - Cambio de rama de trabajo.")
    # # print("-"*70)

    branch = pretty_printer("A partir de que rama deseas partir: ", inputF=True)    

    command_exec(f'''git switch {branch}''', cwd=root, response=True)
    update_local(root=root)      

    new_branch = pretty_printer("Que nombre deseas ponerle a esta nueva rama: ", inputF=True)    

    command_exec(f"git switch -c {new_branch}", cwd=root, response=True)
    update_local(root=root)      

    option = int(pretty_printer("Deseas reflejar tu nueva rama en el repo remoto? (1 Si) o (2 No): ", inputF=True))

    if option == 1:
        command_exec(f'''git push -u {remote} {new_branch}''', cwd=root, response=True)
        update_local(root=root)      

def update_local(root:str):
    # # logger.info("change_branch - Cambio de rama de trabajo.")
    # # print("-"*70)
    command_exec(f'''git fetch''', cwd=root, response=True)
    command_exec(f'''git pull''', cwd=root, response=True)    

def del_branch(root:str, remote:str, active_branch:str):
    # # logger.info("change_branch - Cambio de rama de trabajo.")
    # # print("-"*70)

    update_local(root=root)

    branch = pretty_printer("Que rama deseas borrar: ", inputF=True)   

    denied = ["main", "master", "origin"]

    if branch.lower() in denied:
        pretty_printer("No puedes eliminar main...")
        return

    pretty_printer(f"Estas seguro de que deseas eliminar la rama {branch}:")
    pretty_printer("\t1- Si, continuar")
    pretty_printer("\t2- No, regresar")
    option = int(pretty_printer("R=", inputF=True))

    if option == 1:
        if active_branch == branch:
            pretty_printer(f"No puedes borrar {branch} porque actualmente estas en ella...") 
        else:
            command_exec(f"git branch -d {branch}", cwd=root, response=True)    

def pending_changes(root:str):
    # # logger.info("change_branch - Cambio de rama de trabajo.")
    # # print("-"*70)
    response = command_exec("git status", cwd=root, response=True)

    if "Changes not staged for commit" in response:
        pretty_printer("Faltan cambios por commitear !")
        return False
    else:
        return True
 
def merge(root:str, active_branch:str):
    # # logger.info("change_branch - Cambio de rama de trabajo.")
    # # print("-"*70)

    if not pending_changes(root=root):
        pretty_printer(f"Tienes cambios pendientes dentro de {active_branch}, primero arreglalos.")
        return

    branch = str(pretty_printer("A que rama deseas aplicarle el merge:", inputF=True))

    if branch != active_branch:        
        command_exec(f"git switch {branch}", cwd=root, response=True)        

    update_local(root=root) 

    merge = str(pretty_printer("Cual es la rama que deseas mergear:", inputF=True))

    if merge == branch:
        pretty_printer(f"No puedes mergear {merge} en {branch}...")
        return

    command_exec(f"git merge {merge}", cwd=root, response=True)

    pretty_printer("Existe la posibilidad de conflictos posteriores,\nlos cuales debes resolver en tu editor VS.")
    pretty_printer(f"La rama {merge} al finalizar el merge seguira existiendo,\nesta la puedes borrar despues")

def clone():
    https = pretty_printer("Ingrese el HTTPS de su repo: ", inputF=True)
    user = pretty_printer("Ingrese el nombre de su usuario en git: ", inputF=True)
    token = pretty_printer("Ingrese el token de su sesion git: ", inputF=True)    

    repo_name = https.split("/")[-1].replace(".git", "")
    
    print("-"*70)  
    flag = True

    while flag:        
        root = pretty_printer("Ingresa la ruta local donde deseas crear el repo: ", inputF=True)
        if not os.path.exists(os.path.join(root, repo_name)):
            flag = False
        else:
            pretty_printer(f"Ya existe un directorio (repo) con el nombre {repo_name} en")
            pretty_printer(f"la ruta {root}")
            pretty_printer(f"Por favor revisa bien donde crearas tu repo...")
            print("-"*70)  

    remote_root_token = https.replace("github.com", f"{user}:{token}@github.com")    

    command_exec(f"git clone {remote_root_token}", cwd=root, response=True)

    print("-"*70)  
    pretty_printer(f"Reposistorio {repo_name} creado con exito en la ruta:")
    pretty_printer(root,"\n")

    root = os.path.join(root, repo_name)

    command_exec(f""" git config user.name "{user}" """, cwd=root)
    command_exec(f""" git config user.email "{user}@github.com" """, cwd=root)

    return root, remote_root_token
    
def new_repo():
    https = pretty_printer("Ingrese el HTTPS de su nuevo repo (Antes creelo en git): ", inputF=True)
    user = pretty_printer("Ingrese el nombre de su usuario en git: ", inputF=True)
    token = pretty_printer("Ingrese el token de su sesion git: ", inputF=True)    

    repo_name = https.split("/")[-1].replace(".git", "")
    remote_root_token = https.replace("github.com", f"{user}:{token}@github.com") 
    
    print("-"*70)  
    flag = True

    while flag:        
        root = pretty_printer("Ingresa la ruta local donde desea comenzar su nuevo repo: ", inputF=True)
        if not os.path.exists(os.path.join(root, repo_name)):
            flag = False
        else:
            pretty_printer(f"Ya existe un directorio (repo) con el nombre {repo_name} en")
            pretty_printer(f"la ruta {root}")
            pretty_printer(f"Por favor revisa bien donde crearas tu repo...")
            print("-"*70)  

    root = os.path.join(root, repo_name)
    os.mkdir(root)            

    command_exec("git init", cwd=root, response=True)
    command_exec(f""" git config user.name "{user}" """, cwd=root)
    command_exec(f""" git config user.email "{user}@github.com" """, cwd=root)
    
    update_local(root=root)

    with open(os.path.join(root, "Borrar.py"), "w",encoding="utf-8") as f:
        f.write("Puedes borrar este archivo.")

    command_exec("git add .", cwd=root, response=True)
    command_exec("""git commit -m "Commit Inicial Repo. Local" """, cwd=root, response=True)
    command_exec(f"git remote add origin {remote_root_token}", cwd=root, response=True)
    command_exec("git branch -M main", cwd=root, response=True)
    command_exec(f"git push --force {remote_root_token} main ", cwd=root, response=True)

    return root, remote_root_token

def main():
    flag = True
    while flag:
        subprocess.run("cls", shell=True)                
        
        pretty_printer("Iniciar en repo existente o crear un espacio nuevo:")
        pretty_printer("\t1- Trabajar sobre un repo local existente")
        pretty_printer("\t2- Crear un espacio nuevo (Clonacion de repo)")
        pretty_printer("\t3- Crear un repositorio nuevo")    
        try:
            working_option = int(pretty_printer("R=", inputF=True))
        except:
            working_option = ""
        
        if working_option == 1:
            root = get_workspace() 
            remote = set_token(root=root)
            flag = False
        elif working_option == 2:
            root, remote = clone()        
            print("-"*70)  
            pretty_printer("Pulse enter para continuar:", inputF=True)                
            subprocess.run("cls", shell=True)
            flag = False
        elif working_option == 3:       
            root, remote = new_repo() 
            print("-"*70)  
            pretty_printer("Pulse enter para continuar:", inputF=True)                
            subprocess.run("cls", shell=True)
            flag = False
        print("-"*70)  

    update_local(root=root)        
    subprocess.run("cls", shell=True)                

    while True:                       
        active_branch = get_branches(root=root)    
        print("-"*70)  
        pretty_printer("Que deseas realizar:")    
        pretty_printer("\t1- Cambiar rama de trabajo")
        pretty_printer("\t2- Realizar un commit")
        pretty_printer("\t3- Realizar un commit + push")
        pretty_printer("\t4- Crear rama a partir de otra")
        pretty_printer("\t5- Borrar rama")
        pretty_printer("\t6- Realizar merge")        
        pretty_printer("\t0- Estatus")
        option = int(pretty_printer("R=", inputF=True))
        print("-"*70)  

        match option:
            case 1:                                
                change_branch(root=root, remote=remote, active_branch=active_branch)                        
                pretty_printer(f"\nTarea finalizada con exito !")
                print("-"*70)  
                pretty_printer("Pulse enter para continuar:", inputF=True)                
                subprocess.run("cls", shell=True)
            case 2:                
                commit(root=root, remote=remote, push=False, active_branch=active_branch)                
                pretty_printer(f"\nTarea finalizada con exito !")
                print("-"*70)  
                pretty_printer("Pulse enter para continuar:", inputF=True)                
                subprocess.run("cls", shell=True)                
            case 3:
                commit(root=root, remote=remote, push=True, active_branch=active_branch)                
                pretty_printer(f"\nTarea finalizada con exito !")
                print("-"*70)  
                pretty_printer("Pulse enter para continuar:", inputF=True)                
                subprocess.run("cls", shell=True)   
            case 4:
                new_branch(root=root, remote=remote)                
                pretty_printer(f"\nTarea finalizada con exito !")
                print("-"*70)  
                pretty_printer("Pulse enter para continuar:", inputF=True)                
                subprocess.run("cls", shell=True)   
            case 5:
                del_branch(root=root, remote=remote, active_branch=active_branch)                
                pretty_printer(f"\nTarea finalizada con exito !")
                print("-"*70)  
                pretty_printer("Pulse enter para continuar:", inputF=True)                
                subprocess.run("cls", shell=True)   
            case 6:
                merge(root=root, active_branch=active_branch)                
                pretty_printer(f"\nTarea finalizada con exito !")
                print("-"*70)  
                pretty_printer("Pulse enter para continuar:", inputF=True)                
                subprocess.run("cls", shell=True)   
            case 0:
                pending_changes(root=root)                
                pretty_printer(f"\nTarea finalizada con exito !")
                print("-"*70)  
                pretty_printer("Pulse enter para continuar:", inputF=True)                
                subprocess.run("cls", shell=True)


if __name__ == "__main__":
    main()