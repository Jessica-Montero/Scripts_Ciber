import platform
import time
from effects import Colors
from effects import type_text

def show_system_info():
    type_text(f"\n{Colors.YELLOW}[*] Analizando sistema...{Colors.RESET}\n", 0.04)
    time.sleep(0.5)
    print(f"\n{Colors.CYAN}{Colors.BOLD}[*] Información del sistema{Colors.RESET}")
    print(f"{Colors.GREEN}Sistema:{Colors.RESET} {platform.system()}")
    print(f"{Colors.GREEN}Versión:{Colors.RESET} {platform.version()}")
    print(f"{Colors.GREEN}Arquitectura:{Colors.RESET} {platform.machine()}")
