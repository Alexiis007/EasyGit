# Importacion de las herramientas
from tools import *

import os
import base64

from getpass import getpass

from cryptography.fernet import Fernet

from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

from cryptography.hazmat.primitives import hashes

def set_token():

    user = pretty_printer(
        "Ingrese el usuario git:\n",
        inputF=True
    )

    token = pretty_printer(
        "Ingrese el token del usuario:\n",
        inputF=True
    )

    # password personalizada
    password = getpass(
        "Ingrese una contraseña maestra:\n"
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

    pretty_printer(
        "Token cifrado y almacenado correctamente."
    )

def get_token():    
    user = pretty_printer(
        "Ingrese el usuario git:\n",
        inputF=True
    )


    password = getpass(
        "Ingrese la contraseña maestra:\n"
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
        pretty_printer(f"Token: {token}")

    except:
        pretty_printer("Contraseña incorrecta.")        
    
