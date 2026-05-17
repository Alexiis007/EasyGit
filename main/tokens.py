# Importacion de las herramientas
from tools import *

import os
import base64
import requests

import pwinput

from getpass import getpass

from cryptography.fernet import Fernet

from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

from cryptography.hazmat.primitives import hashes

def set_token(user:str):

    token = pretty_printer(
        "Ingrese el token del usuario:\n",
        inputF=True
    )

    if not vigenci_token(token=token):        
        return False

    # password personalizada
    password = pwinput.pwinput(
        prompt="Ingrese la contraseña maestra:\n",
        mask="*"
    ).encode()

    # generar salt
    salt = os.urandom(16)

    # derivar llave desde password
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=480000,
    )

    key = base64.urlsafe_b64encode(
        kdf.derive(password)
    )

    cipher = Fernet(key)

    # cifrar token
    safe_token = cipher.encrypt(
        token.encode()
    )

    # ruta escritorio
    desktop = os.path.join(
        os.path.expanduser("~"),
        "Desktop"
    )

    # carpeta credentials
    credentials_folder = os.path.join(
        desktop,
        "credentials"
    )

    # crear carpeta si no existe
    os.makedirs(credentials_folder, exist_ok=True)

    # guardar token cifrado
    with open(
        os.path.join(
            credentials_folder,
            f"{user}.key"
        ),
        "wb"
    ) as f:

        f.write(safe_token)

    # guardar salt
    with open(
        os.path.join(
            credentials_folder,
            f"{user}.salt"
        ),
        "wb"
    ) as f:

        f.write(salt)

    return True

def get_token(user:str):    
    password = pwinput.pwinput(
        prompt="Ingrese la contraseña maestra:\n",
        mask="*"
    ).encode()

    desktop = os.path.join(
        os.path.expanduser("~"),
        "Desktop"
    )

    credentials_folder = os.path.join(
        desktop,
        "credentials"
    )

    # leer token cifrado
    with open(
        os.path.join(
            credentials_folder,
            f"{user}.key"
        ),
        "rb"
    ) as f:

        encrypted_token = f.read()

    # leer salt
    with open(
        os.path.join(
            credentials_folder,
            f"{user}.salt"
        ),
        "rb"
    ) as f:

        salt = f.read()

    # regenerar key
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=480000,
    )

    key = base64.urlsafe_b64encode(
        kdf.derive(password)
    )

    cipher = Fernet(key)

    try:
        token = cipher.decrypt(
            encrypted_token
        ).decode()

        pretty_printer(f"Clave correcta !!")
        return token

    except:
        pretty_printer("Contraseña incorrecta.")        
        return None
    
def list_users():
    print("-"*60)  
    pretty_printer("Usuarios Registrados:")
    print("-"*60)  
    desktop = os.path.join(
        os.path.expanduser("~"),
        "Desktop"
    )

    credentials_folder = os.path.join(
        desktop,
        "credentials"
    )

    name_users = []

    if os.path.exists(credentials_folder):
        users = command_exec("dir /a", cwd=credentials_folder, response=True)        
        users = users.split("\n")

        count = 0
        for user in users:
            if ".key" in user:
                count+=1
                user = user.split(" ")[-1]                
                pretty_printer(f"\t{count}- {user.replace(".key", "")}")
                name_users.append(user.replace(".key", ""))
    else:
        pretty_printer("\tNingun usuario registrado")                        
    print("-"*60)  

    return name_users

def vigenci_token(token:str):
    headers = {
        "Authorization": f"token {token}"
    }

    response = requests.get(
        "https://api.github.com/user",
        headers=headers
    )    

    if response.status_code == 401:
        return False
    else:
        return True
    
def del_user(user:str):
    desktop = os.path.join(
        os.path.expanduser("~"),
        "Desktop"
    )

    credentials_folder = os.path.join(
        desktop,
        "credentials"
    )

    file_key = os.path.join(
        credentials_folder,
        "user.key"
    )

    file_salt = os.path.join(
        credentials_folder,
        "user.salt"
    )

    if os.path.exists(file_key):
        os.remove(file_key)

    if os.path.exists(file_salt):
        os.remove(file_salt)        

def sessions():
    
    token = ""
    flag = True

    while flag:
        subprocess.run("cls", shell=True)        
        nerv_art(2)        

        print("-"*60)  
        pretty_printer("Inicio de sesion")        

        users = list_users()
        
        pretty_printer("\t1- Iniciar sesion")
        pretty_printer("\t2- Registrar un token usuario nuevo")
        try:
            option = int(pretty_printer("R=", inputF=True))
            print("-"*60)  
        except:
            continue
        
        if option == 1:
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

        elif option == 2:            
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

            if not set_token(user=user):
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

    return token   