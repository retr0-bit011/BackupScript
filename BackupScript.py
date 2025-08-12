#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import shutil
import datetime
import json
import sys
from pathlib import Path

# Configuración
CONFIG_FILE = Path.home() / '.daily_backup_config.json'
LOG_FILE = Path.home() / 'daily_backup.log'

def load_config():
    """Carga la configuración desde el archivo de configuración."""
    try:
        with open(CONFIG_FILE, 'r') as f:
            config = json.load(f)
            config['source_dir'] = Path(config['source_dir'])
            config['backup_dir'] = Path(config['backup_dir'])
            return config
    except (FileNotFoundError, json.JSONDecodeError):
        return None

def save_config(source_dir, backup_dir):
    """Guarda la configuración en el archivo de configuración."""
    config = {
        'source_dir': str(source_dir),
        'backup_dir': str(backup_dir),
        'last_backup': datetime.datetime.now().isoformat()
    }
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=4)

def log_message(message):
    """Registra un mensaje en el archivo de log."""
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(LOG_FILE, 'a') as f:
        f.write(f"[{timestamp}] {message}\n")

def setup():
    """Configuración inicial del script."""
    print("Configuración de la copia de seguridad diaria\n")
    
    while True:
        source_dir = input("Ingrese la ruta completa de la carpeta a respaldar: ").strip()
        source_dir = Path(source_dir)
        if source_dir.exists() and source_dir.is_dir():
            break
        print(f"Error: La carpeta {source_dir} no existe o no es un directorio válido. Intente nuevamente.")
    
    backup_base = Path.home() / "Backups"
    backup_base.mkdir(exist_ok=True)
    default_backup_dir = backup_base / f"{source_dir.name}_backups"
    
    print(f"\nSe creará una copia diaria en: {default_backup_dir}")
    confirm = input("¿Desea usar esta ubicación? (s/n): ").strip().lower()
    
    if confirm != 's':
        while True:
            backup_dir = input("Ingrese la ruta completa para guardar los backups: ").strip()
            backup_dir = Path(backup_dir)
            try:
                backup_dir.mkdir(parents=True, exist_ok=True)
                break
            except Exception as e:
                print(f"Error: No se pudo crear el directorio de backup: {e}")
    else:
        backup_dir = default_backup_dir
        backup_dir.mkdir(exist_ok=True)
    
    save_config(source_dir, backup_dir)
    print("\nConfiguración guardada correctamente.")
    print(f"Origen: {source_dir}")
    print(f"Destino: {backup_dir}")
    
    # Registrar en el log
    log_message(f"Configuración inicial completada. Origen: {source_dir}, Destino: {backup_dir}")

def perform_backup():
    """Realiza la copia de seguridad si no se ha hecho hoy."""
    config = load_config()
    if not config:
        print("No se encontró configuración. Ejecute el script sin argumentos para configurar.")
        return
    
    today = datetime.datetime.now().date()
    try:
        last_backup_date = datetime.datetime.fromisoformat(config['last_backup']).date()
    except (KeyError, ValueError):
        last_backup_date = None
    
    if last_backup_date == today:
        log_message("Copia de seguridad ya realizada hoy. Saliendo.")
        return
    
    source_dir = config['source_dir']
    backup_dir = config['backup_dir']
    
    if not source_dir.exists():
        log_message(f"Error: El directorio origen {source_dir} no existe.")
        return
    
    # Crear carpeta con la fecha actual
    today_str = today.strftime('%Y-%m-%d')
    dest_dir = backup_dir / today_str
    
    try:
        # Copiar directorio completo
        shutil.copytree(source_dir, dest_dir)
        
        # Actualizar última copia
        config['last_backup'] = datetime.datetime.now().isoformat()
        with open(CONFIG_FILE, 'w') as f:
            json.dump(config, f, indent=4)
        
        log_message(f"Copia de seguridad exitosa de {source_dir} a {dest_dir}")
    except Exception as e:
        log_message(f"Error al realizar la copia de seguridad: {str(e)}")

def main():
    if len(sys.argv) == 1:
        # Modo configuración
        setup()
    else:
        # Modo ejecución (para el inicio)
        perform_backup()

if __name__ == "__main__":
    main()