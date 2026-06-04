Libreria para generar archivos exe:
    pip install pyinstaller

Comando para generarlo:
    pyinstaller --onefile main.py

-> Opcionales

Sin consola:
    --noconsole

icono:
    --icon=icon.ico

error de imports no identificados:
    --hidden-import modulo

cambio de nombre del exe:
    pyinstaller --onefile --name EasyGit main.py

Comando final: 
    pyinstaller --onefile --icon=.\assets\nerv.ico --name EasyGit .\main\__main__.py

    Si al correr el .exe generado se tiene errores de librerias puedes
    probar borrando los archivos dist y build, despues generar de nuevo.

    Igual es necesario que tengas un .venv    

--------------------------------------------------------------------
Instalacion de librerias .venv
--------------------------------------------------------------------
Activar .venv
    .\.venv\Scripts\activate
Instalacion
    python -m pip install modulo
Verifica
    python -c "import modulo; print('ok')"


---- > Error si la hora del PC no esta bien
---- > Errore porque Git no esta instalado
---- > Agregar acceso rapido (opcion) de crear un repo en esccritorio 


--------------------------------------------------------------------
Pendientes
--------------------------------------------------------------------
1- Identificar ramas remotas al borrarlas y aplicar "git push origin --delete RAMA"

2- Puedo crear ramas a partir de ramas que no existen - Agregar validacion

3- del_branch() reefactorizar

4-Nueva opcion mover modificaciones de archivos a otra rama - git stash --include-untracked

5 Identificar cuando se va un token clavado

6- Deteccion de commits de diferencia contra main: git cherry main pdf-detallado-layout-header

7-Cree una rama con el nombre remote/origin/ al inicio :(

8- Reflejar rama en remoto: git push -u origin pdf-detallado-layout-header

9- Borrar rama remota cuando la local ya no existe:git push origin --delete pdf-detallado-layout-header

10- Error cuanto insertas la ruta local de un repo y se inserta una ruta con terminacion a un ejecutable Ejemplo: C:\Users\cjuarez\Desktop\EasyGit\main\git_actions.py