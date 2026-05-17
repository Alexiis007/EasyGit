# Para logs
import logging

# Utilidades con ruteo y de mas
import os

# Para borrar carpeta en exit_clean()
import shutil

# importacion de herramientas de trabajo
from tools import *

# Logger Config
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)    

def get_workspace():
    # logger.info("get_workspace - Obtencion de espacio de trabajo.")
    # print("-"*60)

    flag = True
    while flag:
        root = pretty_printer("Digite la ruta de trabajo (Donde este el archivo .git): \n", inputF=True)    
        root = root.strip()

        if len(root) != 0 and os.path.exists(root):
            flag = False            
        else:
            pretty_printer("Ruta erronea !!!")
            print("-"*60)
        
    pretty_printer("Verificando la existencia del archivo .git")
    
    list_dir = command_exec("dir /a", cwd=root, response=True)

    if not ".git" in list_dir:
        command_exec("cls", root)
        logger.error("get_workspace - Obtencion de espacio de trabajo. Ruta incorrecta.")
        print("-"*60)
        pretty_printer("La ruta de trabajo establecida no contiene una archivo .git.")
        pretty_printer("Por favor intente de nuevo.")
        print("-"*60)
        get_workspace()
    else:
        pretty_printer("Archivo .git encontrado.")
        pretty_printer("Ruta establecida !")                

    print("-"*60)

    return root

def set_remote_token(root:str, token:str):
    # logger.info("setToken - Establecimiento del token.")
    # print("-"*60)

    remote_root = command_exec("git remote -v", response=True, cwd=root)
    remote_root = str(remote_root).split("\n")[0].replace("\t", " ").split(" ")    

    remote_root_token = ""

    for i in remote_root:
        if "http" in i:
            remote_root_token = i

    user = remote_root_token.split("/")[3]

    command_exec(f""" git config user.name "{user}" """, cwd=root)
    command_exec(f""" git config user.email "{user}@github.com" """, cwd=root)

    # token = pretty_printer(f"Ingrese token de trabajo para el usuario {user}:\n", inputF=True)        

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
    # print("-"*60)

    pretty_printer("Ramas existentes en el espacio de trabajo:")   
    print("-"*60) 

    res = command_exec("git branch -a", response=True, cwd=root)
    
    active_branch = ""

    for i in res.split('\n'):
        if len(str(i)) > 0:
            pretty_printer(f"- {i}")
        if "*" in i:
            active_branch = i.split(" ")[-1]
        
    pretty_printer(f"\n->  Rama activa: {active_branch}")    

    return active_branch

def change_branch(root:str, remote:str, active_branch:str):
    # # logger.info("change_branch - Cambio de rama de trabajo.")
    # # print("-"*60)

    pretty_printer("A que rama desea cambiar:")
    branch = pretty_printer("Opcion: ", inputF=True)
    print("-"*60)

    pretty_printer(f"Esta cambiando de la rama {active_branch} a la rama {branch}.")
    pretty_printer(f"Antes es necesario guardar los cambios de su rama activa actual...")
    pretty_printer(f"\t1- Cancela todo y regresemos")
    pretty_printer(f"\t2- Guardemos todo ahora mismo")
    pretty_printer(f"\t3- Si ya todo esta guardado, solo continuemos")
    option = int(pretty_printer(f"Opcion:", inputF=True))

    flag = True
    while flag:        
        if option == 1:
            return
        elif option == 2:
            commit = pretty_printer(f"Denos un mensaje de commit:", inputF=True)
            command_exec(f'''git add .''', cwd=root)
            command_exec(f'''git commit -m "{commit}"''', cwd=root, response=True)
            command_exec(f'''git push -u {remote} {active_branch}''', cwd=root, response=True)
            command_exec(f'''git switch {branch}''', cwd=root, response=True)
            flag = False
        elif option == 3:
            res = command_exec(f'''git switch {branch}''', cwd=root, response=True)
            if "Please commit your changes" in res:
                print("-"*60)
                pretty_printer("Tienes cambios no commiteados...")
                pretty_printer("Seras regresado al menu, reviza bien tus cambios.")
            flag = False
        else:        
            print("-"*60)    
            pretty_printer("Solo se pueden las opciones mostradas !")
            option = int(pretty_printer(f"Opcion:", inputF=True))

    update_local(root=root)        

def commit(root:str, remote:str, push:bool, active_branch:str):
    # # logger.info("change_branch - Cambio de rama de trabajo.")
    # # print("-"*60)

    pretty_printer("Opcion de guardado: ")
    pretty_printer("\t1- Guardar todo")
    pretty_printer("\t2- Especificar archivos")
    pretty_printer("\t3- Cancelar commit")
    option = int(pretty_printer("R=", inputF=True)) 

    command_exec(f'''git fetch''', cwd=root, response=True)    

    if option == 1:
        print("-"*60)
        commit = pretty_printer(f"Denos un mensaje de commit:\n", inputF=True)            
        command_exec(f'''git add .''', cwd=root)
        command_exec(f'''git commit -m "{commit}"''', cwd=root, response=True)                
    elif option == 2:
        print("-"*60)
        files = str(pretty_printer("Separados por espacios ingrese los archivos que desea guardar:\n", inputF=True))
        command_exec(f'''git add {files}''', cwd=root)

        print("-"*60)
        commit = pretty_printer(f"Denos un mensaje de commit:\n", inputF=True)            
        command_exec(f'''git commit -m "{commit}"''', cwd=root, response=True)     
    elif option == 3:
        return
    else:
        return

    if push:        
        command_exec(f'''git push -u {remote} {active_branch}''', cwd=root, response=True)
        command_exec(f'''git fetch''', cwd=root, response=True)    

def new_branch(root:str, remote:str):
    # # logger.info("change_branch - Cambio de rama de trabajo.")
    # # print("-"*60)

    branch = pretty_printer("A partir de que rama deseas partir: ", inputF=True)    

    command_exec(f'''git switch {branch}''', cwd=root, response=True)
    update_local(root=root)      

    new_branch = str(pretty_printer("Que nombre deseas ponerle a esta nueva rama: ", inputF=True)).strip().replace(" ", "")

    command_exec(f"git switch -c {new_branch}", cwd=root, response=True)
    update_local(root=root)      

    option = int(pretty_printer("Deseas reflejar tu nueva rama en el repo remoto? (1 Si) o (2 No): ", inputF=True))

    if option == 1:
        command_exec(f'''git push -u {remote} {new_branch}''', cwd=root, response=True)
        update_local(root=root)      

def update_local(root:str):
    # # logger.info("change_branch - Cambio de rama de trabajo.")
    # # print("-"*60)
    command_exec(f'''git fetch''', cwd=root, response=True)
    command_exec(f'''git pull''', cwd=root, response=True)    

def del_branch(root:str, remote:str, active_branch:str):
    # # logger.info("change_branch - Cambio de rama de trabajo.")
    # # print("-"*60)

    update_local(root=root)

    branch = pretty_printer("Que rama deseas borrar: ", inputF=True)   

    denied = ["main", "master", "origin"]

    if branch.lower() in denied:
        pretty_printer("No puedes eliminar main...")
        return
    
    if active_branch == branch:
        pretty_printer(f"No puedes borrar {branch} porque actualmente estas en ella...") 
        return

    pretty_printer(f"Estas seguro de que deseas eliminar la rama {branch}:")
    pretty_printer("\t1- Si, continuar")
    pretty_printer("\t2- No, regresar")
    option = int(pretty_printer("R=", inputF=True))

    if option == 1:
        res = command_exec(f"git branch -d {branch}", cwd=root, response=True)           

        if "git branch -D" in res:
            print("-"*60)
            pretty_printer(f"Ojo ! {branch} tiene commits que probablemente no exitan en main")
            pretty_printer("\t1- Salir y revizar esos commits")
            pretty_printer("\t2- Forzar eliminacion de la rama")
            option = int(pretty_printer("R= ", inputF=True))

            if option == 2:
                command_exec(f"git branch -D {branch}", cwd=root, response=True)   
            else:
                return

        option = int(pretty_printer("Deseas reflejar tu nueva rama en el repo remoto? (1 Si) o (2 No): ", inputF=True))

        if option == 1:
            command_exec(f'''git push -u {remote} {branch}''', cwd=root, response=True)
            update_local(root=root)   
        else:
            return    
    else:
        return

def pending_changes(root:str):
    # # logger.info("change_branch - Cambio de rama de trabajo.")
    # # print("-"*60)
    response = command_exec("git status", cwd=root, response=True)

    if "Changes not staged for commit" in response:
        pretty_printer("Faltan cambios por commitear !")
        return False
    else:
        return True
 
def status(root:str, active_branch:str):
    # # logger.info("change_branch - Cambio de rama de trabajo.")
    # # print("-"*60)

    pretty_printer(f"Estatus de rama actual - {active_branch}:")
    print("-"*60)
            
    commits_not_stage = []
    untracked_files = []
    data_ignore = [
        "__pycache__",
        "dist",
        "build",
        "venv"
    ]

    # Llenado de listados de cambios y archivos nuevos
    status = command_exec("git status", cwd=root, response=True)
    if len(status) > 0:
        status = status.split("\n")
        count = 0

        for line in status:                        
            if "Changes not staged for commit" in line:
                for i in range(count, len(status)):
                    if "(use" not in status[i] and "\tmodified" in status[i]:
                        commits_not_stage.append(status[i])
                    elif "\n" in status[i]:
                        break            
            elif "Untracked files" in line:
                for i in range(count, len(status)):
                    if "(use" not in status[i] and "\t" in status[i]:
                        untracked_files.append(status[i])
                    elif "\n" in status[i]:
                        break                        
            count+=1        
    else:
        pretty_printer("No se tiene nungun status...")
    
    # Eliminación de elementos ignore. [:] crea una copia de el array
    for line in commits_not_stage[:]:
        for ignore in data_ignore:
            if ignore in line:
                commits_not_stage.remove(line)

    for line in untracked_files[:]:
        for ignore in data_ignore:
            if ignore in line:
                untracked_files.remove(line)
        
    # Listado de archivos modificados    
    pretty_printer(f"-> Archivos modificados({len(commits_not_stage)}) - {active_branch}:")    
        
    count = 0
    for i in commits_not_stage:
        count+=1
        pretty_printer(f"\t{count}- Archivo modificado: {i.replace("\tmodified:   ", "")}")
    if count == 0:
        pretty_printer("\tNo hay archivos modificados.")
    
    # Listado de archivos nuevos
    pretty_printer(f"\n-> Archivos nuevos creados({len(untracked_files)}) - {active_branch}:")    
    
    count = 0
    for i in untracked_files:
        count+=1
        pretty_printer(f"\t{count}- Nuevo archivo detectado: {i.replace("\t", "")}")

    if count == 0:
        pretty_printer("\tNo hay archivos nuevos detectados.")
        
def hist_commits(root:str, active_branch:str):
    command_exec("cls", cwd=root)
    print("-"*60)  
    pretty_printer(f"Historial de commits - {active_branch}:")    
    print("-"*60)  

    hist_commits = command_exec("git log -5", cwd=root, response=True)

    if len(hist_commits) > 0:
        pretty_printer(hist_commits)
    else:
        pretty_printer("Nada por mostrar...")

def merge(root:str, active_branch:str):
    # # logger.info("change_branch - Cambio de rama de trabajo.")
    # # print("-"*60)

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

    pretty_printer(f"-> Existe la posibilidad de conflictos posteriores,\nlos cuales debes resolver en tu editor VS.")
    pretty_printer(f"-> La rama {merge} al finalizar el merge seguira existiendo,\nesta la puedes borrar despues")
    pretty_printer(f"-> Recuerda hacer un push de tu rama {branch}")

def clone(token:str):
    https = pretty_printer("Ingrese el HTTPS de su repo: ", inputF=True)
    user = pretty_printer("Ingrese el nombre de su usuario en git: ", inputF=True)
    # token = pretty_printer("Ingrese el token de su sesion git: ", inputF=True)    

    repo_name = https.split("/")[-1].replace(".git", "")
    
    print("-"*60)  
    flag = True

    while flag:        
        root = pretty_printer("Ingresa la ruta local donde deseas crear el repo: ", inputF=True)
        if not os.path.exists(os.path.join(root, repo_name)):
            flag = False
        else:
            pretty_printer(f"Ya existe un directorio (repo) con el nombre {repo_name} en")
            pretty_printer(f"la ruta {root}")
            pretty_printer(f"Por favor revisa bien donde crearas tu repo...")
            print("-"*60)  

    remote_root_token = https.replace("github.com", f"{user}:{token}@github.com")    

    command_exec(f"git clone {remote_root_token}", cwd=root, response=True)

    print("-"*60)  
    pretty_printer(f"Reposistorio {repo_name} creado con exito en la ruta:")
    pretty_printer(root,"\n")

    root = os.path.join(root, repo_name)

    command_exec(f""" git config user.name "{user}" """, cwd=root)
    command_exec(f""" git config user.email "{user}@github.com" """, cwd=root)

    return root, remote_root_token
    
def new_repo(token:str):
    https = pretty_printer("Ingrese el HTTPS de su nuevo repo (Antes creelo en git): ", inputF=True)
    user = pretty_printer("Ingrese el nombre de su usuario en git: ", inputF=True)
    # token = pretty_printer("Ingrese el token de su sesion git: ", inputF=True)    

    repo_name = https.split("/")[-1].replace(".git", "")
    remote_root_token = https.replace("github.com", f"{user}:{token}@github.com") 
    
    print("-"*60)  
    flag = True

    while flag:        
        root = pretty_printer("Ingresa la ruta local donde desea comenzar su nuevo repo: ", inputF=True)
        if not os.path.exists(os.path.join(root, repo_name)):
            flag = False
        else:
            pretty_printer(f"Ya existe un directorio (repo) con el nombre {repo_name} en")
            pretty_printer(f"la ruta {root}")
            pretty_printer(f"Por favor revisa bien donde crearas tu repo...")
            print("-"*60)  

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

    print("-"*60)  

    return root, remote_root_token

def exit_clean(root:str):
    pretty_printer("Salida borrara todo rastro del repo local")
    pretty_printer("Asegurese de tener todos los cambios ya en el remoto")
    pretty_printer("Esta seguro de continuar con la accion:")
    pretty_printer("\t1- Si")
    pretty_printer("\t2- No")
    option = int(pretty_printer("R=", inputF=True))
    print("-"*60)  

    if option == 1:        
        if os.path.exists(root):            
            try:
                os.chdir("C:/")
                shutil.rmtree(root)
            except PermissionError:
                pretty_printer("La carpeta está en uso !")
                return
            
            if not os.path.exists(root):
                pretty_printer("Eliminacion completa...")
        else:
            pretty_printer("El archivo no existe !")
    elif option == 2:
        return
    else:
        return