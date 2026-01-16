import platform
import getpass
import shutil
import os
import time
from effects import Colors
from effects import type_text

def vulnerability_scanner():
    findings = []

    user = getpass.getuser().lower()
    if user in ["administrator", "root"]:
        findings.append((
            "PRIV-001",
            "Usuario administrador en sesión activa",
            "ALTO"
        ))

    os_name = platform.system()
    findings.append((
        "INFO-001",
        f"Sistema operativo detectado: {os_name}",
        "INFO"
    ))

    total, used, free = shutil.disk_usage("/")
    free_gb = free // (1024**3)

    if free_gb < 10:
        findings.append((
            "DISK-001",
            "Espacio en disco crítico (<10GB)",
            "CRÍTICO"
        ))

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
