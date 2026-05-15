# Para la ejecucion de comandos
import subprocess

# Importacion de herramientas de trabajo
from tools import *

# Importacion de funciones git
from git_actions import *

from tokens import *

def main():    
    subprocess.run("color 0A", shell=True)                    
    
    token = ""
    flag = True

    while flag:
        subprocess.run("cls", shell=True)        
        nerv_art(2)        

        print("-"*60)  
        pretty_printer("Inicio de sesion")        
        users = list_users()
        pretty_printer("\t1- Registrar un token usuario nuevo")
        pretty_printer("\t2- Iniciar sesion")
        try:
            option = int(pretty_printer("R=", inputF=True))
        except:
            option = ""

        if option == 1:            
            print("-"*60)  
            pretty_printer("Registre su nueva sesion:")            
            print("-"*60)  
            
            user = pretty_printer("Ingrese el usuario git:\n", inputF=True)

            if user in users:
                pretty_printer(f"El usuario {user} ya esta registrado !")
                pretty_printer(f"Por favor solo inicie sesion.")
                print("-"*60)  
                pretty_printer("Presione enter para continuar", inputF=True)
                continue

            if not save_token(user=user):
                pretty_printer("No puede registrar este token porque esta vencido !")
                pretty_printer("Por favor intente de nuevo.")
                print("-"*60)  
                pretty_printer("Presione enter para continuar", inputF=True)
                continue

            pretty_printer("Usuario registrado con exito !")
            pretty_printer("Ahora debere iniciar sesion con el.")
            print("-"*60)  
            pretty_printer("Presione enter para continuar", inputF=True)
            continue

        elif option == 2:
            user = pretty_printer("Ingrese el usuario git:\n", inputF=True)
            
            if user not in users:
                pretty_printer(f"El usuario {user} no esta registrado aun !")
                pretty_printer("Por favor intente primero registrarlo")
                print("-"*60)  
                pretty_printer("Presione enter para continuar", inputF=True)
                continue
        
            token = get_token(user=user)                                    

            if not vigenci_token(token=token):
                pretty_printer("El token esta vencido !")
                pretty_printer("Registrese de nuevo.")
                print("-"*60)  
                pretty_printer("Presione enter para continuar", inputF=True)
                del_user(user=user) 
                continue
            else:
                flag = False


    flag = True
    while flag:
        subprocess.run("cls", shell=True)                        

        nerv_art(2)        

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
            remote = set_token(root=root, token=token)
            flag = False
        elif working_option == 2:
            root, remote = clone(token=token)        
            print("-"*60)  
            pretty_printer("Pulse enter para continuar:", inputF=True)                
            subprocess.run("cls", shell=True)
            flag = False
        elif working_option == 3:       
            root, remote = new_repo(token=token) 
            print("-"*60)  
            pretty_printer("Pulse enter para continuar:", inputF=True)                
            subprocess.run("cls", shell=True)
            flag = False
        print("-"*60)  

    update_local(root=root)            
    subprocess.run("cls", shell=True)                    

    while True:         
        nerv_art(2)                      
        print("-"*60)  
        active_branch = get_branches(root=root)    
        print("-"*60)  
        status(root=root, active_branch=active_branch)                
        print("-"*60)  
        pretty_printer("Que deseas realizar:")    
        print("-"*60)  
        pretty_printer("\t1- Cambiar rama de trabajo")
        pretty_printer("\t2- Realizar un commit")
        pretty_printer("\t3- Realizar un commit + push")
        pretty_printer("\t4- Crear rama a partir de otra")
        pretty_printer("\t5- Borrar rama")
        pretty_printer("\t6- Realizar merge")        
        pretty_printer("\t7- Salida Limpia (Experimental)")   
        pretty_printer("\t8- Historial de commits")        
        pretty_printer("\t0- Regresar al menu anterior")        
        option = int(pretty_printer("R=", inputF=True))
        print("-"*60)  

        match option:
            # change_branch(root=root, remote=remote, active_branch=active_branch)                        
            case 1:                                
                change_branch(root=root, remote=remote, active_branch=active_branch)                        
                print()
                print("-"*60)  
                pretty_printer(f"Tarea finalizada con exito !")
                print("-"*60)  
                pretty_printer("Pulse enter para continuar:", inputF=True)                
                subprocess.run("cls", shell=True)
            # commit(root=root, remote=remote, push=False, active_branch=active_branch)                
            case 2:                
                commit(root=root, remote=remote, push=False, active_branch=active_branch)                
                print()
                print("-"*60)  
                pretty_printer(f"Tarea finalizada con exito !")
                print("-"*60)  
                pretty_printer("Pulse enter para continuar:", inputF=True)                
                subprocess.run("cls", shell=True)                
            # commit(root=root, remote=remote, push=True, active_branch=active_branch)                
            case 3:
                commit(root=root, remote=remote, push=True, active_branch=active_branch)                
                print()
                print("-"*60)  
                pretty_printer(f"Tarea finalizada con exito !")
                print("-"*60)  
                pretty_printer("Pulse enter para continuar:", inputF=True)                
                subprocess.run("cls", shell=True)   
            # new_branch(root=root, remote=remote)                
            case 4:
                new_branch(root=root, remote=remote)                
                print()
                print("-"*60)  
                pretty_printer(f"Tarea finalizada con exito !")
                print("-"*60)  
                pretty_printer("Pulse enter para continuar:", inputF=True)                
                subprocess.run("cls", shell=True)   
            # del_branch(root=root, remote=remote, active_branch=active_branch)                
            case 5:
                del_branch(root=root, remote=remote, active_branch=active_branch)                
                print()
                print("-"*60)  
                pretty_printer(f"Tarea finalizada con exito !")
                print("-"*60)  
                pretty_printer("Pulse enter para continuar:", inputF=True)                
                subprocess.run("cls", shell=True)   
            # merge(root=root, active_branch=active_branch)                
            case 6:
                merge(root=root, active_branch=active_branch)                
                print()
                print("-"*60)  
                pretty_printer(f"Tarea finalizada con exito !")
                print("-"*60)  
                pretty_printer("Pulse enter para continuar:", inputF=True)                
                subprocess.run("cls", shell=True)   
            # exit(root=root)                
            case 7:
                exit_clean(root=root)                
                print()
                print("-"*60)  
                pretty_printer(f"Tarea finalizada con exito !")
                print("-"*60)  
                pretty_printer("Pulse enter para continuar:", inputF=True)                
                subprocess.run("cls", shell=True)               
            # hist_commits(root=root, active_branch=active_branch)                
            case 8:                
                hist_commits(root=root, active_branch=active_branch)
                print()
                print("-"*60)  
                pretty_printer(f"Tarea finalizada con exito !")
                print("-"*60)  
                pretty_printer("Pulse enter para continuar:", inputF=True)                
                subprocess.run("cls", shell=True)          
            case 0:                
                main()                           

if __name__ == "__main__":
    main()