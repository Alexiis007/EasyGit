# EasyGit

<div align="center">

```text
        ███████╗ █████╗ ███████╗██╗   ██╗
        ██╔════╝██╔══██╗██╔════╝╚██╗ ██╔╝
        █████╗  ███████║███████╗ ╚████╔╝ 
        ██╔══╝  ██╔══██║╚════██║  ╚██╔╝  
        ███████╗██║  ██║███████║   ██║   
           ╚══════╝╚═╝  ╚═╝╚══════╝   ╚═╝      
                    ██████╗ ██╗████████╗
                   ██╔════╝ ██║╚══██╔══╝
                ██║  ███╗██║   ██║
                ██║   ██║██║   ██║
                ╚██████╔╝██║   ██║
                 ╚═════╝ ╚═╝   ╚═╝
```

CLI para Windows diseñada para simplificar el flujo de trabajo con Git y GitHub desde terminal.

Automatiza tareas comunes como manejo de ramas, commits, pushes y autenticación segura mediante tokens cifrados.

</div>

---

## Descripción

EasyGit es una herramienta de línea de comandos que centraliza operaciones frecuentes de Git en una interfaz interactiva.

Su objetivo es reducir la complejidad del uso de Git en proyectos diarios, especialmente en entornos Windows.

---

## Características

### Gestión de Git simplificada

- Cambio de ramas
- Creación de ramas
- Eliminación de ramas locales/remotas
- Commits rápidos
- Commit + Push en un solo paso
- Push con tracking automático
- Merge entre ramas
- Historial de commits
- Ejecución de comandos personalizados
- Acceso directo al repositorio web
- Explorador de archivos integrado

---

### Seguridad de credenciales

Los tokens de GitHub se manejan de forma segura:

- Validación previa contra GitHub API
- Cifrado con **Fernet**
- Derivación de clave con **PBKDF2-HMAC-SHA256**
- Salt único por usuario
- Contraseña maestra para acceso

---

## Inicio de sesión

EasyGit permite múltiples usuarios GitHub en un mismo entorno:

- Registro de usuarios con token cifrado
- Inicio de sesión con contraseña maestra
- Eliminación automática de credenciales inválidas o vencidas

---

## Vista de la CLI

```text
------------------------------------------------------------
Ramas existentes en el repositorio:
------------------------------------------------------------

-> dev (local - remoto)
- main (local - remoto)

------------------------------------------------------------
Estatus de rama actual - dev:
------------------------------------------------------------

-> Archivos modificados
-> Archivos nuevos

------------------------------------------------------------
Que deseas realizar:
------------------------------------------------------------

1- Cambiar rama de trabajo
2- Realizar commit
3- Commit + push
4- Crear rama
5- Borrar rama
6- Merge
7- Comando personalizado
8- Historial de commits
9- Abrir explorador de Windows
10- Actualizar ventana
11- Abrir repo web
12- Push rama
13- Cerrar sesión
```

---

## Instalación

### Requisitos

- Python 3.12+
- Git instalado y agregado al PATH
- Windows 10+

---

### Entorno virtual

```bash
python -m venv .venv
.\.venv\Scripts\activate
```

---

### Dependencias

```bash
pip install -r requirements.txt
```

---

## Generar ejecutable

Instalar PyInstaller:

```bash
pip install pyinstaller
```

---

Compilar:

```bash
pyinstaller --onefile ^
--icon=.\assets\nerv.ico ^
--name EasyGit ^
.\main\__main__.py
```

---

## Estructura del proyecto

```text
EasyGit/
│
├── assets/
├── build/
├── dist/
│
├── main/
│   ├── __main__.py
│   ├── git_actions.py
│   ├── gui.py
│   ├── tools.py
│   ├── tokens.py
│
├── .gitignore
├── EasyGit.spec
└── README.md
```

---

## Seguridad

Las credenciales se almacenan en:

```text
Desktop/credentials/
├── usuario.key
└── usuario.salt
```

Proceso:

- Token validado con GitHub
- Cifrado con Fernet
- Clave derivada con PBKDF2
- Acceso protegido por contraseña maestra

---

## Autor

**Alexsis007**

Herramienta creada para optimizar flujos de trabajo con Git desde terminal en Windows.
