# BackupScript
BackupScript es un script sencillo en Python, su función es crear una copia de seguridad de la carpeta seleccionada cada día cuando el ordenador arranque.

## Modo de uso 
1. Arrancar el script.
2. Seleccionar la ruta completa de la carpeta que se la quiere respaldar.
3. Seleccionar la ruta donde se guardará la copia de seguridad.

## Configuración para la ejecución al inicio
En Windows: Crea un acceso directo al script. Colócalo en la carpeta de Inicio (Windows + R, escribe shell:startup).
En Linux: Agrega una entrada en crontab con @reboot: (crontab -l 2>/dev/null; echo "@reboot /usr/bin/python3 /ruta/al/script.py --run") | crontab -
En Mac: Crea un Launch Agent en ~/Library/LaunchAgents/

## Funcionamiento
1. Cada vez que se inicie el equipo, el script verificará si ya se hizo una copia hoy.
2. Si no se ha hecho, realizará una copia completa de la carpeta especificada.
3. Las copias se guardan en subcarpetas con la fecha (AAAA-MM-DD).
