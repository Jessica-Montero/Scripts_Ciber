
#Librerias necesarias para la ejecución del sistema
import os
import sys
import platform
import shutil

# --------------------------
# VERIFICACIÓN DE DEPENDENCIAS
# --------------------------
# Esta función verifica que todas las dependencias necesarias estén instaladas:
def verificar_dependencias():
    try:
        requisitos_python = ["scapy", "evtx", "fpdf", "requests", "bs4"]
        faltantes_python = []

        for paquete in requisitos_python:
            try:
                __import__(paquete)
            except ImportError:
                faltantes_python.append(paquete)

        herramientas_externas = {"nmap": "herramienta para escaneo de redes"}
        faltantes_externas = []

        for herramienta in herramientas_externas:
            if not shutil.which(herramienta):
                faltantes_externas.append(herramienta)

        if faltantes_python or faltantes_externas:
            print("\n----- Dependencias faltantes -----")
            if faltantes_python:
                print("Paquetes Python faltantes: " + ", ".join(faltantes_python))
            if faltantes_externas:
                print("Herramientas externas faltantes: " + ", ".join(faltantes_externas))

            so = platform.system()
            print(f"\nSO detectado: {so}")

            if faltantes_python:
                if so == "Windows":
                    print("\nEjecute en la terminal:")
                    print(" py -m pip install " + " ".join(faltantes_python))
                elif so in ("Linux", "Darwin"):
                    print("\nEjecute en la terminal:")
                    print(" python3 -m pip install " + " ".join(faltantes_python))
                    print(" o bien")
                    print(" python -m pip install " + " ".join(faltantes_python))
                else:
                    print("\nSistema no reconocido. Instale manualmente los paquetes Python faltantes.")

            if faltantes_externas:
                print("\nPara instalar herramientas externas:")
                for h in faltantes_externas:
                    if h == "nmap":
                        if so == "Windows":
                            print(" - Nmap: descargar desde https://nmap.org/download.html")
                        elif so == "Linux":
                            print(" - Nmap: sudo apt install nmap  # Debian/Ubuntu")
                            print("          sudo yum install nmap  # RedHat/CentOS")
                        elif so == "Darwin":
                            print(" - Nmap: brew install nmap")
                        else:
                            print(f" - {h}: instalar manualmente según su sistema.")
            sys.exit("\nInstale las dependencias antes de continuar.")
        else:
            print("\nTodas las dependencias están instaladas correctamente.")
    except Exception as e:
        print(f"Error al verificar dependencias: {e}")
        sys.exit(1)

verificar_dependencias()

# Librerias necesarias para cada módulo

from scapy.all import sniff, IP, TCP, UDP, ICMP
import time
from datetime import datetime
import subprocess
from collections import defaultdict
from evtx import PyEvtxParser
import requests
from bs4 import BeautifulSoup
import re
import smtplib
from email.message import EmailMessage
import xml.etree.ElementTree as ET
from fpdf import FPDF
from email.header import Header

# --------------------------
# MÓDULO 1: MONITOREO DE RED
# Monitorea tráfico de red en tiempo real, alerta sobre escaneos, tráfico ICMP/UDP sospechoso y 
# puertos críticos, y guarda los hallazgos en un log.
# --------------------------
def monitoreoRed():
    
    print("\n----- Monitoreo de red -----\n")

    tcp_count = defaultdict(int)
    icmp_count = defaultdict(int)
    udp_count = defaultdict(int)

    time_window = 10
    tcp_threshold = 20
    icmp_threshold = 10
    udp_threshold = 10
    last_reset = time.time()
    puertos_criticos = [22, 21, 3389]
    log_file = "hallazgos_red.txt"

    def procesar_paquete(pkt):
        nonlocal last_reset
        ts = datetime.now().strftime("%H:%M:%S")
        mensaje = ""

        try:
            if IP in pkt:
                src = pkt[IP].src
                dst = pkt[IP].dst

                if TCP in pkt:
                    dport = pkt[TCP].dport
                    if pkt[TCP].flags == "S":
                        tcp_count[src] += 1
                        if tcp_count[src] > tcp_threshold:
                            mensaje = f"[{ts}] ALERTA: Posible escaneo de puertos desde {src}"
                    if dport in puertos_criticos:
                        mensaje = f"[{ts}] ALERTA: Intento de conexión a puerto crítico {dport} desde {src}"

                elif ICMP in pkt:
                    icmp_count[src] += 1
                    if icmp_count[src] > icmp_threshold:
                        mensaje = f"[{ts}] ALERTA: Posible ataque ICMP desde {src}"

                elif UDP in pkt:
                    udp_count[src] += 1
                    if udp_count[src] > udp_threshold:
                        mensaje = f"[{ts}] ALERTA: Posible tráfico UDP sospechoso desde {src}"

                if mensaje:
                    print(mensaje)
                    try:
                        with open(log_file, "a") as f:
                            f.write(mensaje + "\n")
                    except Exception as e:
                        print(f"\nError al escribir log: {e}")

            if time.time() - last_reset > time_window:
                tcp_count.clear()
                icmp_count.clear()
                udp_count.clear()
                last_reset = time.time()
        except Exception as e:
            print(f"\nError procesando paquete: {e}")

    print("\nMonitoreo de red iniciado... (Ctrl+C para detener)")
    try:
        sniff(prn=procesar_paquete, store=False)
    except KeyboardInterrupt:
        print("\nMonitoreo detenido por usuario.")
    except Exception as e:
        print(f"\nError durante monitoreo: {e}")

    print("\nMonitoreo de red finalizado.")
    input("\nPresione ENTER para volver al menú principal. \n* Para generar el informe, seleccione la opción 8 del menú principal.")    

# --------------------------
# MÓDULO 2: ANÁLISIS DE REGISTROS
# Analiza logs del sistema para detectar intentos fallidos de login y 
# cambios sospechosos en usuarios, registrando alertas en un archivo.
# --------------------------
def analisisRegistros():
    print("\n----- Análisis de registros -----\n")
    
    so = platform.system()
    hallazgos_file = "hallazgos_registros.txt"

    if so == "Linux":
        log_file = "/var/log/auth.log"
        try:
            with open(log_file, "r") as f:
                lineas = f.readlines()
        except Exception as e:
            print(f"\nNo se pudo leer el archivo {log_file}: {e}")
            input("\nPresione ENTER para volver al menú principal.")
            return

        fallos_login = defaultdict(int)
        cambios_usuario = defaultdict(int)
        umbral_fallos = 5

        for linea in lineas:
            try:
                if "Failed password" in linea or "authentication failure" in linea:
                    partes = linea.split()
                    ip = partes[-3] if len(partes) >= 4 else "desconocida"
                    user = partes[-5] if len(partes) >= 6 else "desconocido"
                    fallos_login[ip] += 1
                    if fallos_login[ip] >= umbral_fallos:
                        try:
                            with open(hallazgos_file, "a") as f:
                                f.write(f"ALERTA: {fallos_login[ip]} intentos fallidos de login desde {ip} (usuario {user})\n")
                        except Exception as e:
                            print(f"\nError al escribir hallazgo: {e}")

                if "New user" in linea:
                    partes = linea.split()
                    usuario = partes[-1]
                    cambios_usuario[usuario] += 1
                    if cambios_usuario[usuario] > 3:
                        try:
                            with open(hallazgos_file, "a") as f:
                                f.write(f"\nALERTA: Múltiples cambios en la cuenta de usuario {usuario}\n")
                        except Exception as e:
                            print(f"\nError al escribir hallazgo: {e}")
            except Exception as e:
                print(f"\nError procesando línea de log: {e}")

    elif so == "Windows":
        archivo_evtx = "C:\\Windows\\System32\\winevt\\Logs\\Security.evtx"
        try:
            parser = PyEvtxParser(archivo_evtx)
        except PermissionError:
            print(f"\nNo se pudo acceder al archivo {archivo_evtx}. Intente ejecutar como Administrador.")
            input("\nPresione ENTER para volver al menú principal.")
            return
        except Exception as e:
            print(f"\nError al leer archivo EVTX: {e}")
            input("\nPresione ENTER para volver al menú principal.")
            return

        fallos_login = defaultdict(int)
        try:
            for record in parser.records_json():
                datos = record["data"]
                if "Account Name" in datos and "Failed" in datos:
                    ip = "desconocida"
                    fallos_login[ip] += 1
                    if fallos_login[ip] >= 5:
                        try:
                            with open(hallazgos_file, "a") as f:
                                f.write(f"\nALERTA: {fallos_login[ip]} intentos fallidos desde {ip}\n")
                        except Exception as e:
                            print(f"\nError al escribir hallazgo: {e}")
        except Exception as e:
            print(f"\nError procesando registros EVTX: {e}")

    print(f"\nAnálisis de registros finalizado. Hallazgos guardados en '{hallazgos_file}'.")
    input("\nPresione ENTER para volver al menú principal.\n* Para generar el informe, seleccione la opción 8 del menú principal.")

# --------------------------
# MÓDULO 3: DETECCIÓN DE VULNERABILIDADES
# Escanea hosts con Nmap, detecta servicios y vulnerabilidades, y 
# guarda un informe legible en un archivo de texto.
# --------------------------
def procesarNmapXML(xml_file, salida_txt="hallazgos_vuln_legible.txt"):
    if not os.path.exists(xml_file):
        print(f"Archivo {xml_file} no encontrado.")
        return

    try:
        tree = ET.parse(xml_file)
        root = tree.getroot()
        with open(salida_txt, "w", encoding="utf-8") as f:
            for host in root.findall('host'):
                ip = host.find('address').attrib.get('addr')
                f.write(f"Host: {ip}\n")
                f.write("-" * 40 + "\n")
                for port in host.findall('ports/port'):
                    portid = port.attrib.get('portid')
                    protocol = port.attrib.get('protocol')
                    state = port.find('state').attrib.get('state')
                    service_elem = port.find('service')
                    service = service_elem.attrib.get('name') if service_elem is not None else "desconocido"
                    product = service_elem.attrib.get('product') if service_elem is not None else ""
                    version = service_elem.attrib.get('version') if service_elem is not None else ""
                    f.write(f"Puerto: {portid}/{protocol} | Estado: {state} | Servicio: {service} {product} {version}\n")
                f.write("\n")
        
    except Exception as e:
        print(f"\nError procesando XML: {e}")

def vulnerabilidades():
    print("\n----- Detección de vulnerabilidades -----\n")
    
    try:
        print("ATENCIÓN: No interrumpa el escaneo. Este proceso puede tardar varios minutos...\n")
        objetivos_input = input("IPs/rangos a escanear (separados por comas): ")
        objetivos = [x.strip() for x in objetivos_input.split(",") if x.strip()]
        if not objetivos:
            print("\nNo se ingresaron objetivos para Nmap.")
            return
        

        salida_txt = "hallazgos_vuln.txt"

        resultado = subprocess.run(
            ["nmap", "-sV", "-T4", "-Pn", "-oX", salida_txt] + objetivos,
            capture_output=True,
            text=True,
            check=True
        )
 
        procesarNmapXML(salida_txt)
        print("\nEscaneo Nmap finalizado, resultados en 'hallazgos_vuln_legible.txt'.")
    except subprocess.CalledProcessError as e:
        print(f"\nError ejecutando Nmap: {e.stderr}")
    except FileNotFoundError:
        print("\nNmap no está instalado o no se encuentra en el PATH.")
    except Exception as e:
        print(f"\nError inesperado en módulo de vulnerabilidades: {e}")

    input("\nPresione ENTER para volver al menú principal. \n* Para generar el informe, seleccione la opción 8 del menú principal.")    

# --------------------------
# MÓDULO 4: PREVENCIÓN DE ATAQUES
# Módulo 4: Simula y gestiona la prevención de ataques bloqueando IPs con múltiples intentos fallidos y 
# permitiendo reglas predefinidas, registrando todo en el firewall y logs.
# --------------------------
def prevencionAtaques():
    print("\n----- Prevención de ataques mejorada -----\n")
    print("Nota: Si una IP falla 5 veces, se bloqueará automáticamente.\n")

    intentos = defaultdict(int)
    bloqueadas = {}
    reglas = []  # reglas predefinidas
    log_file = "prevencion.txt"
    so = platform.system()

    def bloquear_ip(ip):
        bloqueadas[ip] = time.time() + 3600  # bloqueada 1 hora
        print(f"\nALERTA: IP {ip} bloqueada temporalmente 1 hora.")
        try:
            with open(log_file, "a", encoding="utf-8") as f:
                f.write(f"{datetime.now()} - IP {ip} bloqueada temporalmente\n")
        except Exception as e:
            print(f"\nError escribiendo log de bloqueo: {e}")

        try:
            if so == "Linux":
                os.system(f"sudo iptables -A INPUT -s {ip} -j DROP")
            elif so == "Windows":
                os.system(f'netsh advfirewall firewall add rule name="Bloqueo {ip}" dir=in action=block remoteip={ip}')
            else:
                print("\nSistema operativo no reconocido. Bloqueo real no aplicado.")
        except Exception as e:
            print(f"\nError aplicando bloqueo real: {e}")

    def agregar_regla():
        tipo = input("Tipo de regla (IP/PUERTO/PROTOCOLO): ").strip().upper()
        valor = input("Valor de la regla: ").strip()
        reglas.append((tipo, valor))
        print(f"Regla agregada: {tipo} = {valor}")

    while True:
        try:
            print("\nOpciones:")
            print("1 - Registrar intento de acceso a su sistema")
            print("2 - Mostrar IPs bloqueadas")
            print("3 - Desbloquear IP")
            print("4 - Agregar regla predefinida")
            print("5 - Mostrar reglas predefinidas")
            print("6 - Salir")

            opcion = input("\nSeleccione una opción: ").strip()

            if opcion == "6":
                break

            elif opcion == "1":
                ip = input("\nIP que intenta acceder a su sistema: ").strip()
                exito = input("Fue exitoso? (s/n): ").strip().lower() == "s"
                # Validación reglas predefinidas
                bloqueo_por_regla = any(
                    r[0] == "IP" and r[1] == ip for r in reglas
                )
                if bloqueo_por_regla:
                    bloquear_ip(ip)
                    continue

                if not exito:
                    intentos[ip] += 1
                    print(f"\nIntentos fallidos de {ip}: {intentos[ip]}")
                    if intentos[ip] >= 5 and ip not in bloqueadas:
                        bloquear_ip(ip)
                else:
                    intentos[ip] = 0

            elif opcion == "2":
                if bloqueadas:
                    print("\nIPs bloqueadas actualmente:")
                    for ip in bloqueadas:
                        print(f"- {ip}")
                else:
                    print("\nNo hay IPs bloqueadas.")

            elif opcion == "3":
                if bloqueadas:
                    print("\nIPs bloqueadas actualmente:")
                    for ip in bloqueadas:
                        print(f"- {ip}")
                    ip_desbloquear = input("\nIngrese la IP que desea desbloquear: ").strip()
                    if ip_desbloquear in bloqueadas:
                        del bloqueadas[ip_desbloquear]
                        print(f"IP {ip_desbloquear} desbloqueada.")
                        if so == "Linux":
                            os.system(f"sudo iptables -D INPUT -s {ip_desbloquear} -j DROP")
                        elif so == "Windows":
                            os.system(f'netsh advfirewall firewall delete rule name="Bloqueo {ip_desbloquear}"')
                    else:
                        print("\nIP no encontrada en bloqueadas.")
                else:
                    print("\nNo hay IPs bloqueadas.")

            elif opcion == "4":
                agregar_regla()

            elif opcion == "5":
                if reglas:
                    print("\nReglas predefinidas:")
                    for r in reglas:
                        print(f"- {r[0]} = {r[1]}")
                else:
                    print("\nNo hay reglas definidas.")

            else:
                print("\nOpción no válida. Intente de nuevo.\n")

        except Exception as e:
            print(f"\nError en la simulación de ataques: {e}")

    print("\nPrevención de ataques finalizada.")
    input("\nPresione ENTER para volver al menú principal.\n* Para generar el informe, seleccione la opción 8 del menú principal.")

# --------------------------
# MÓDULO 5: ANÁLISIS DE TRÁFICO WEB
# Analiza URLs para detectar patrones sospechosos de ataques web 
# (inyección SQL, scripts), registrando alertas en un archivo de hallazgos.
# --------------------------
def traficoWeb():
    print("\n----- Análisis de tráfico web -----\n")
    
    hallazgos_file = "analisis_web.txt"
    
    try:
        entradas = input("Ingrese las URLs a analizar (separadas por comas): ")
        urls = [url.strip() for url in entradas.split(",") if url.strip()]
        if not urls:
            print("\nNo se ingresaron URLs. Volviendo al menú principal.")
            return
    except Exception as e:
        print(f"Error leyendo URLs: {e}")
        return
    
    try:
        with open(hallazgos_file, "w") as f:
            for url in urls:
                try:
                    response = requests.get(url, timeout=5)
                    contenido = response.text
                    patrones_sospechosos = [
                        r"(?:')|(?:--)|(?:#)|(\bOR\b|\bAND\b).*?=",
                        r"<script.*?>.*?</script>"
                    ]
                    for patron in patrones_sospechosos:
                        coincidencias = re.findall(patron, contenido, re.IGNORECASE)
                        if coincidencias:
                            f.write(f"{datetime.now()} ALERTA: Posible amenaza detectada en {url} con patrón {patron}\n")
                            print(f"ALERTA detectada en {url} con patrón {patron}")
                except Exception as e_url:
                    f.write(f"{datetime.now()} ERROR al analizar {url}: {e_url}\n")
                    print(f"\nERROR al analizar {url}: {e_url}")
    except Exception as e_file:
        print(f"\nError escribiendo archivo de hallazgos web: {e_file}")

    print(f"\nAnálisis web finalizado. Hallazgos guardados en '{hallazgos_file}'.")
    input("\nPresione ENTER para volver al menú principal. \n* Para generar el informe, seleccione la opción 8 del menú principal.")

# --------------------------
# MÓDULO 6: ALERTAS Y NOTIFICACIONES
# Registra alertas de seguridad en un log, muestra notificaciones en pantalla y 
# permite enviarlas por correo electrónico.
# --------------------------
def alertasNotificaciones(tipo, ip, descripcion):
   
    log_file = "alertas.txt"

    try:
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(f"[{datetime.now()}] ALERTA tipo: {tipo}, IP: {ip}, Detalle: {descripcion}\n")
    except Exception as e:
        print(f"\nError escribiendo alerta en log: {e}")

    print(f"[{datetime.now()}] ALERTA tipo: {tipo}, IP: {ip}, Detalle: {descripcion}")

    
    while True:
        respuesta = input("\n¿Desea enviar esta alerta por correo? (s/n): ").strip().lower()
        if respuesta in ['s', 'n']:
            break
        print("\nEntrada inválida. Por favor ingrese 's' para sí o 'n' para no.")

    if respuesta == 's':
        try:
            remitente = "tu_email@gmail.com"
            destinatario = "destino_email@gmail.com"
            msg = EmailMessage()

            msg['Subject'] = Header(f"Alerta de seguridad: {tipo}", 'utf-8')
            msg['From'] = remitente
            msg['To'] = destinatario
            msg.set_content(f"\nSe ha detectado una alerta de tipo {tipo}.\nIP: {ip}\nDetalle: {descripcion}", charset="utf-8")

            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login(remitente, "tu_contraseña_app")
                smtp.send_message(msg)
            print("Correo enviado exitosamente.")
        except smtplib.SMTPAuthenticationError:
            print("\nError: autenticación fallida. Verifique usuario/contraseña.")
        except smtplib.SMTPConnectError:
            print("Error: no se pudo conectar al servidor SMTP.")
        except Exception as e:
            print(f"\nError inesperado al enviar correo: {e}")
    else:
        print("\nAlerta no enviada por correo.")

    print("\nNota: en entornos reales, se debe cambiar el remitente y destinatario...")
    input("\n*Presione ENTER para volver al menú principal.")

# --------------------------
# MÓDULO 7: REGISTRO DE INCIDENTES
# Permite registrar manualmente incidentes de seguridad, guardando tipo, descripción e IP 
# en un archivo de registro.
# --------------------------
def incidentes():
    print("\n----- Registro manual de incidente -----\n")
    archivo = "registro_incidentes.txt"

    try:
        tipo = input("Tipo de incidente: ")
        descripcion = input("Descripción: ")

        while True:
            ip = input("Si hay una IP registrada en el evento anótela, de lo contrario presione 'N': ")
            ip = ip.strip()
            if ip.lower() == 'n':
                ip = 'N'
                break
            # Validar formato de IP básica
            elif re.match(r"^\d{1,3}(\.\d{1,3}){3}$", ip):
                break
            else:
                print("Error: ingrese una IP válida o 'N'.")

        with open(archivo, "a") as f:
            f.write(f"[{datetime.now()}] Tipo: {tipo} - Descripcion: {descripcion} - IP: {ip} \n")
        print(f"\nIncidente registrado en '{archivo}'.")
    except Exception as e:
        print(f"\nError registrando incidente: {e}")

    input("\n*Para generar el informe en PDF, seleccione la opción 8 del menú principal. \nPresione ENTER para continuar.")

# --------------------------
# MÓDULO 8: INFORMES DE SEGURIDAD
# Genera un informe PDF de seguridad con hallazgos de todos los módulos y recomendaciones generales.
# --------------------------
def generarInformeSeguridadPDF():
    print("\n----- Informes de seguridad: formato PDF -----\n")
    print("Este informe contiene los hallazgos encontrados en las opciones del menú principal")

    try:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", 'B', 16)
        # Título seguro con fecha
        titulo = f"Informe de Seguridad - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        pdf.cell(0, 10, titulo, ln=True, align='C')
        pdf.ln(10)

        archivos = {
            "Monitoreo de Red": "hallazgos_red.txt",
            "Análisis de Registros": "hallazgos_registros.txt",
            "Vulnerabilidades": "hallazgos_vuln_legible.txt",
            "Prevención de Ataques": "prevencion.txt",
            "Registro de Incidentes": "registro_incidentes.txt",
            "Análisis Web": "analisis_web.txt"
        }

        # DETALLE DE HALLAZGOS
        for nombre_mod, archivo in archivos.items():
            pdf.set_font("Arial", 'B', 14)
            pdf.cell(0, 10, nombre_mod, ln=True)
            pdf.set_font("Arial", '', 12)
            if os.path.exists(archivo):
                with open(archivo, "r", encoding="utf-8", errors="ignore") as f:
                    lineas = f.readlines()
                for l in lineas[:10]:
                    pdf.multi_cell(0, 8, l.strip())
                if len(lineas) > 10:
                    pdf.multi_cell(0, 8, f"... Para efecto académico se limitó la impresión de hallazgos. \nSe omite la impresión de ({len(lineas)-10} más)")
            else:
                pdf.multi_cell(0, 8, "Archivo no encontrado.")
            pdf.ln(5)
            
        # ---------------------------
        # RECOMENDACIONES GENERALES
        # ---------------------------
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(0, 10, "Recomendaciones Generales", ln=True)
        pdf.set_font("Arial", '', 12)

        recomendaciones = [
            "1. Revisar y actualizar regularmente las contraseñas y accesos de usuarios.",
            "2. Aplicar parches y actualizaciones de seguridad en sistemas y aplicaciones.",
            "3. Monitorear de manera continua el tráfico de red para detectar actividades sospechosas.",
            "4. Capacitar al personal en ciberseguridad y concienciación sobre ataques comunes.",
            "5. Mantener copias de seguridad de información crítica y probar su restauración periódicamente.",
            "6. Implementar medidas de autenticación fuerte y control de accesos a sistemas sensibles.",
            "7. Revisar periódicamente los registros de eventos y alertas para anticipar incidentes.",
            "8. Aplicar políticas de bloqueo de IPs y firewall según los hallazgos de monitoreo."
        ]

        for rec in recomendaciones:
            pdf.multi_cell(0, 8, rec)    


        i = 1
        while os.path.exists(f"Informe_Seguridad{i}.pdf"):
            i += 1
        nombre_pdf = f"Informe_Seguridad{i}.pdf"
        pdf.output(nombre_pdf)
        print(f"[*] Informe PDF generado: {nombre_pdf}")

    except PermissionError:
        print("\nError: el archivo PDF está abierto o no tiene permisos de escritura.")
    except Exception as e:
        print(f"\nError inesperado al generar PDF: {e}")

    input("\nPresione ENTER para volver al menú principal.")
    
# ============================
# MENÚ PRINCIPAL
# ============================
def main():
    while True:
        print("\nBienvenido al Sistema: SECUREPY (Security in Python)")
        print("\n----- Menú principal -----")
        print("1. Monitoreo de red")
        print("2. Análisis de registros")
        print("3. Detección de vulnerabilidades")
        print("4. Prevención de ataques")
        print("5. Análisis de tráfico web")
        print("6. Alertas y notificaciones")
        print("7. Registro de incidentes")
        print("8. Informes de seguridad")
        print("9. Salir")

        try:
            opcion = int(input("\nSeleccione una opción: "))
        except ValueError:
            print("\nPor favor ingrese un número válido.")
            continue

        if opcion == 1:
            monitoreoRed()
        elif opcion == 2:
            analisisRegistros()
        elif opcion == 3:
            vulnerabilidades()
        elif opcion == 4:
            prevencionAtaques()
        elif opcion == 5:
            traficoWeb()
        elif opcion == 6:
            print("\n----- Alertas y notificaciones -----\n")
            tipo = input("Tipo de alerta: ")
            ip = input("IP involucrada: ")
            descripcion = input("Descripción de la alerta: ")
            alertasNotificaciones(tipo, ip, descripcion)
        elif opcion == 7:
            incidentes()
        elif opcion == 8:
            generarInformeSeguridadPDF()
        elif opcion == 9:
            print("\nSECUREPY. ¡Nos vemos pronto! \n----- FIN DEL SISTEMA -----")
            break
        else:
            print("\nError de selección, intente nuevamente")
            continue

# ============ FLUJO PRINCIPAL ============
main()