# Para logs
import logging

# Para el metodo de escritura 
import sys
import time

# Para la ejecucion de comandos
import subprocess

# Utilidades con ruteo y de mas
import os

# Para borrar carpeta en exit_clean()
import shutil


# Logger Config
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def colors(txt:str, color:int):
    # Verde Hacker
    if color == 1:
        return f"\033[92m{txt}\033[0m"
    else:
        return txt

def nerv_art(option:int=1):
    if option == 1:
        art = """
            ███╗   ██╗███████╗██████╗ ██╗   ██╗
            ████╗  ██║██╔════╝██╔══██╗██║   ██║
            ██╔██╗ ██║█████╗  ██████╔╝██║   ██║
            ██║╚██╗██║██╔══╝  ██╔══██╗╚██╗ ██╔╝
            ██║ ╚████║███████╗██║  ██║ ╚████╔╝
            ╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝  ╚═══╝
        """
    elif option == 2:
        art = """
            ███╗   ██╗███████╗██████╗ ██╗   ██╗
            ████╗  ██║██╔════╝██╔══██╗██║   ██║
            ██╔██╗ ██║█████╗  ██████╔╝██║   ██║
            ██║╚██╗██║██╔══╝  ██╔══██╗╚██╗ ██╔╝
            ██║ ╚████║███████╗██║  ██║ ╚████╔╝
            ╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝  ╚═══╝            
                        Alexsis007        
        """

    pretty_printer(art)    

def pretty_printer(txt: str, inputF:bool = False, fast=True):    
    if fast:
        sys.stdout.write(colors(txt, 1))
    else:
        for letra in txt:
            sys.stdout.write(colors(letra, 1))
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
        return f"{output.stdout}\n{output.stderr}"
