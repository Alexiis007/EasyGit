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

-------------
Instalacion de librerias .venv
--------------
Activar .venv
    .\.venv\Scripts\activate
Instalacion
    python -m pip install modulo
Verifica
    python -c "import modulo; print('ok')"


