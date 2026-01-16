from effects import Colors
from effects import show_banner


def show_menu():
    show_banner ()  
    print(f"Bienvenido al uso de herramientas básicas para Ciberseguridad\n")
    print(f"\n{Colors.BOLD}════════════════════════════════════{Colors.RESET}")
    print(f"{Colors.YELLOW}  Selecciona una opción:{Colors.RESET}")
    print(f"{Colors.BOLD}════════════════════════════════════{Colors.RESET}")
    print(f"  {Colors.GREEN}[1]{Colors.RESET} Info del sistema")
    print(f"  {Colors.GREEN}[2]{Colors.RESET} Escáner educativo")
    print(f"  {Colors.RED}[0]{Colors.RESET} Salir")