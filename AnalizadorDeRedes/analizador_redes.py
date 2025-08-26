# sys permite interactuar con el sistema operativo
import sys

# Esta función verifica que las bibliotecas necesarias estén instaladas.
def verificar_dependencias():
    requisitos = ['dns', 'whois']
    faltantes = []

    for paquete in requisitos:
        try:
            __import__(paquete)
        except ImportError:
            faltantes.append(paquete)

    if faltantes:
        print("\n🚨 Faltan los siguientes paquetes necesarios para ejecutar el programa:")
        for f in faltantes:
            print(f" → {f}")

        print("\nSi usa 🪟 Windows:")
        print("Ejecute este comando en la terminal:\n")
        print("    py -m pip install -r requirements.txt")

        print("\nSi usa 🐧 Linux o macOS 🍎 :")
        print("Ejecute uno de estos comandos en la terminal:\n")
        print("    python3 -m pip install -r requirements.txt")
        print("    o bien")
        print("    python -m pip install -r requirements.txt")

        print("\nSi usa otro sistema operativo, use el comando adecuado para tu entorno.")

        sys.exit("\nInstale los paquetes faltantes antes de continuar.")

# Verificación al iniciar el programa
verificar_dependencias()

# Importación de bibliotecas necesarias.

# Para obtener la IP de un dominio.
import dns.resolver 
# Para consultar WHOIS: quién es el dueño de un dominio o cuándo fue creado.
import whois 
# Para detectar el sistema operativo.      
import os   
# Para ayudar a identificar el sistema con más detalle
import platform
# Para ejecutar comandos del sistema como el ping.        
import subprocess    

# Mensaje de bienvenida al sistema
print("\nBienvenido/a al sistema de Análisis de información de Redes y Sistemas Operativos\n")

# Función que se encarga de resolver nombre de dominio y si no puede indica error
def resolver_dominio(dominio):
    print(f"\nResolviendo dominio: {dominio}")

    # IPv4 - tipo A
    try:
        respuestas_v4 = dns.resolver.resolve(dominio, 'A')
        print("\nDirecciones IPv4:")
        for respuesta in respuestas_v4:
            print(f"\t{respuesta}")
    except Exception as e:
        print("\nNo se pudo obtener dirección IPv4.")

    # IPv6 - tipo AAAA
    try:
        respuestas_v6 = dns.resolver.resolve(dominio, 'AAAA')
        print("\nDirecciones IPv6:")
        for respuesta in respuestas_v6:
            print(f"\t{respuesta}")
    except Exception as e:
        print("\nNo se pudo obtener dirección IPv6.")

    print("-" * 40)

# Función que se encarga de dar la información WHOIS del dominio
def info_whois(dominio): 
    print(f"\nInformación WHOIS para: {dominio}")
    try:
        # info: consulta una base de datos pública para obtener la información y posteriormente mostrarla
        info = whois.whois(dominio)
        print(f"\tRegistrante: {info.get('name')}")
        print(f"\tOrganización: {info.get('org')}")
        print(f"\tPaís: {info.get('country')}")
        
        fecha = info.get('creation_date')
        if isinstance(fecha, list):
            fecha = fecha[0]
        print(f"\tFecha de creación: {fecha}")
    
    except Exception as e:
        print(f"\nError al obtener WHOIS: {e}")
    
    print("-" * 40)


# Función que se encarga de ejecutar comando ping con subprocess.
def ejecutar_ping(dominio):
    print(f"\nEjecutando ping a {dominio}")
    try:
        comando = ["ping", "-n", "4", dominio] if os.name == "nt" else ["ping", "-c", "4", dominio]
        resultado = subprocess.run(comando, capture_output=True, text=True, timeout=10)
        print("\nResultado del ping:\n")
        print(resultado.stdout)
    except subprocess.TimeoutExpired:
        print("\nEl ping tardó demasiado en responder.")
    except Exception as e:
        print(f"\nError al ejecutar ping: {e}")
    print("-" * 40)

# Función que se encarga de dar la información del sistema operativo
def sist_operativo():
    print("\nInformación del sistema operativo en el host local:")
    print(f"\tTipo interno del sistema: {os.name}")
    print(f"\tPlataforma: {os.sys.platform}")
    print(f"\tNombre del sistema operativo: {platform.system()}")
    print(f"\tVersión del sistema: {platform.version()}")
    print(f"\tArquitectura: {platform.machine()}")
    print(f"\tProcesador: {platform.processor()}")
    

    try:
        if hasattr(os, 'uname'):
            detalles = os.uname()
            print(f"\tDetalles del sistema (uname): {detalles}")
        elif os.name == 'nt':
            resultado = subprocess.run(['systeminfo'], capture_output=True, text=True, timeout=10)
            lineas = resultado.stdout.splitlines()
            print("\tDetalles del sistema (Windows - primeras líneas):")
            for linea in lineas[:10]:
                print("   " + linea)
        else:
            print("\nDetalles del sistema: No disponible para este sistema operativo")
    except Exception as e:
        print(f"\nError al obtener detalles del sistema: {e}")

    print("-" * 40)
    


# Función principal
def main():
    while True:
        dominio_usuario = input("\nPor favor, ingresa el dominio que deseas analizar: ").strip()

        # Validaciones del dominio
        if dominio_usuario.startswith("http://") or dominio_usuario.startswith("https://") or dominio_usuario.startswith("www."):
            print("\nPor favor, ingresa solo el dominio sin 'http://', 'https://' ni 'www.'")
            print("Ejemplo válido: 'google.com'\n")
            continue

        if not dominio_usuario or "." not in dominio_usuario:
            print("\nDominio inválido. Intenta con uno como 'google.com'")
            continue

        resolver_dominio(dominio_usuario)
        info_whois(dominio_usuario)
        ejecutar_ping(dominio_usuario)
        sist_operativo()
        

        while True:
            seguir = input("\n¿Le gustaría analizar otro dominio? (S/N): ").upper()
            if seguir == "S":
                break  
            elif seguir == "N":
                print("\nGracias por usar el sistema. ¡Hasta pronto!\n" + "-" * 40)
                return  
            else:
                print("\nPor favor, ingrese una opción válida: S/N")

# Ejecutar programa
main()