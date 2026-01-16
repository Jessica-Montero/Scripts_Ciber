from os import system
def cls():
    system("cls")

cls() 


from menu import show_menu
from scanner import vulnerability_scanner
from system_info import show_system_info
from effects import Colors
from effects import type_text   
import sys
import time

def wait_for_enter():
    while True:
        user_input = input("\nPresione ENTER para volver al menú principal... ")
        if user_input == "":
            break
        else:
            print("ERROR, presione la tecla indicada, por favor")

def main():
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
        print(f"\n\n{Colors.RED}[!] Programa interrumpido. \nVuelva a ejecutar el programa. {Colors.RESET}\n")
        sys.exit(0)