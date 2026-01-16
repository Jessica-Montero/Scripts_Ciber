from os import system
def cls():
    system("cls")

cls()    

import sys
import time
import platform
import getpass
import shutil
import os


class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    PINK = '\033[38;5;218m'
    RESET = '\033[0m'
    BOLD = '\033[1m'


# efecto máquina de escribir
def type_text(text, delay=0.03):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()  
        time.sleep(delay)


def show_system_info():
    type_text(f"\n{Colors.YELLOW}[*] Analizando sistema...{Colors.RESET}\n", 0.04)
    time.sleep(0.5)
    print(f"\n{Colors.CYAN}{Colors.BOLD}[*] Información del sistema{Colors.RESET}")
    print(f"{Colors.GREEN}Sistema operativo:{Colors.RESET} {platform.system()}")
    print(f"{Colors.GREEN}Versión:{Colors.RESET} {platform.version()}")
    print(f"{Colors.GREEN}Arquitectura:{Colors.RESET} {platform.machine()}")


def vulnerability_scanner():
    findings = []

    # Usuario
    user = getpass.getuser().lower()
    if user in ["administrator", "root"]:
        findings.append((
            "PRIV-001",
            "Usuario administrador en sesión activa",
            "ALTO"
        ))

    # Sistema operativo
    os_name = platform.system()
    findings.append((
        "INFO-001",
        f"Sistema operativo detectado: {os_name}",
        "INFO"
    ))

    # Disco (multiplataforma)
    path = "/" if os_name != "Windows" else "C:\\"
    total, used, free = shutil.disk_usage(path)
    free_gb = free // (1024 ** 3)

    if free_gb < 10:
        findings.append((
            "DISK-001",
            "Espacio en disco crítico (<10GB)",
            "CRÍTICO"
        ))

    # Backups
    if not os.path.exists("backups"):
        findings.append((
            "BACKUP-001",
            "No se detectó carpeta de respaldos",
            "MEDIO"
        ))


    type_text(f"\n{Colors.YELLOW}[*] Analizando sistema...{Colors.RESET}\n", 0.04)
    time.sleep(0.5)

    if not findings:
        print(f"{Colors.GREEN}[✓] No se detectaron problemas críticos{Colors.RESET}")
        return

    for code, desc, severity in findings:
        if severity == "CRÍTICO":
            color = Colors.RED
        elif severity == "ALTO":
            color = Colors.YELLOW
        elif severity == "MEDIO":
            color = Colors.BLUE
        else:
            color = Colors.GREEN

        if severity == "CRÍTICO":
            type_text(
                f"{Colors.RED}[!] {code}: {desc} - [{severity}]{Colors.RESET}\n",
                0.03
            )
        else:
            print(f"{color}[!] {code}: {desc} - [{severity}]{Colors.RESET}")

    time.sleep(1)


def show_banner():
    banner = f"""{Colors.PINK}{Colors.BOLD}

 ██ ███ ███ █ █ ██  ███ ███ █ █     ███  █  █   █ █ ███ ███ 
█   █   █   █ █ █ █  █   █  █ █      █  █ █ █   █ █  █   █  
█   ██  █   █ █ ██   █   █   █       █  █ █ █   ██   █   █  
 █  █   █   █ █ █ █  █   █   █       █  █ █ █   █ █  █   █  
  █ █   █   █ █ █ █  █   █   █       █  █ █ █   █ █  █   █  
██  ███ ███  █  █ █ ███  █   █       █   █  ███ █ █ ███  █  

{Colors.MAGENTA}[*] For Educational Purposes Only...{Colors.RESET}
"""
    print(banner)
    time.sleep(1)


def show_menu():
    print(f"\n{Colors.BOLD}════════════════════════════════════{Colors.RESET}")
    print(f"{Colors.YELLOW}  Selecciona una opción:{Colors.RESET}")
    print(f"{Colors.BOLD}════════════════════════════════════{Colors.RESET}")
    print(f"  {Colors.GREEN}[1]{Colors.RESET} Info del sistema")
    print(f"  {Colors.GREEN}[2]{Colors.RESET} Escáner educativo")
    print(f"  {Colors.RED}[0]{Colors.RESET} Salir")


def wait_for_enter():
    while True:
        user_input = input("\nPresione ENTER para volver al menú principal... ")
        if user_input == "":
            break
        else:
            print("ERROR, presione la tecla indicada, por favor")


def main():
    show_banner()

    while True:
        show_menu()
        option = input(f"{Colors.CYAN}[?] Opción: {Colors.RESET}")

        if option == "1":
            show_system_info()
            wait_for_enter()
        elif option == "2":
            vulnerability_scanner()
            wait_for_enter()
        elif option == "0":
            type_text(f"\n{Colors.PINK}Gracias, nos vemos pronto...{Colors.RESET}\n", 0.04)
            time.sleep(0.5)
            print("")
            break
        else:
            print(f"{Colors.RED}Opción inválida{Colors.RESET} \nVolviendo al menú principal...")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.RED}[!] Programa interrumpido.\nVuelva a ejecutar el programa.{Colors.RESET}\n")
        sys.exit(0)
