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