# Para la ejecucion de comandos
import subprocess

# Importacion de herramientas de trabajo
from tools import *

# Importacion de funciones git
from git_actions import *

from tokens import *

# from gui import *

def main():
    logger(msg="-"*60, level="info")
    logger(msg="main() - Iniciando CLI", level="info")        
    logger(msg="-"*60, level="info")
    
    subprocess.run("color 0A", shell=True)                        

    token = sessions()    

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

    while True:         
        nerv_art(2)                      
        print("-"*60)  

        data_branches = get_branches(root=root)
        active_branch = data_branches["active_branch"]   
        branches = data_branches["branches"]   

        pretty_printer("Ramas existentes en el espacio de trabajo:") 
        print("-"*60) 

        for branch in branches:
            pretty_printer(f"- {branch}")      

        pretty_printer(f"\n->  Rama activa: {active_branch}")    
  
        print("-"*60)  
        status(root=root, active_branch=active_branch)                
        print("-"*60)  
        pretty_printer("Que deseas realizar:")    
        print("-"*60)  

        options = [
            "Cambiar rama de trabajo",      #1
            "Realizar un commit",           #2
            "Realizar un commit + push",    #3
            "Crear una rama",               #4
            "Borrar rama",                  #5            
            "Realizar merge",               #6
            "Salida Limpia (Experimental)", #7
            "Historial de commits",         #8
            "Abrir explorador de Windows",  #9
            "Actualizar Ventana",           #10
            "Abrir repo en navegador",      #11
            "Empujar rama",        #12
            "Cerrar sesion"                 #13            
        ]

        count = 0
        index = 0
        for i in options:            
            index+=1
            if count == 0:
                line = i    
                count += 1                
                if count == 1 and i == options[-1]:                                
                    pretty_printer(f"{index}- {line}")                    
            elif count == 1:                
                line += f" "*(35-len(line))
                pretty_printer(f"{index-1}- {line}{index}- {i}")
                count = 0                            

        print("-"*60)  
        option = only_int_options(max_number_option=len(options), zero_start=True)
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
            # command_exec("explorer .", cwd=root)         
            case 9:                
                command_exec("explorer .", cwd=root)
                subprocess.run("cls", shell=True) 
            case 10:                                
                subprocess.run("cls", shell=True) 
            case 11:                                
                command_exec(f"start {remote}", cwd=root)
                subprocess.run("cls", shell=True) 
            case 12:                
                push_branch_to_remote(root=root, remote=remote)
                print()
                print("-"*60)  
                pretty_printer(f"Tarea finalizada con exito !")
                print("-"*60)  
                pretty_printer("Pulse enter para continuar:", inputF=True)                
                subprocess.run("cls", shell=True)                      
            case 13:                
                main()                           

if __name__ == "__main__":
    main()
    
    # app = QtWidgets.QApplication([])

    # widget = MyWidget()
    # widget.resize(800, 600)
    # widget.show()

    # sys.exit(app.exec())