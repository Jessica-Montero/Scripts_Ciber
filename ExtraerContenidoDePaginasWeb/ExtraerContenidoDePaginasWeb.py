import sys

# Esta función verifica que las bibliotecas necesarias estén instaladas.
def verificar_dependencias():
    requisitos = ['bs4', 'mechanize', 'requests']
    faltantes = []

    for paquete in requisitos:
        try:
            __import__(paquete)
        except ImportError:
            faltantes.append(paquete)

    if faltantes:
        print("\nFaltan los siguientes paquetes necesarios para ejecutar el programa:")
        for f in faltantes:
            print(f" → {f}")
            
        print ("\nSi utiliza 🪟 Windows: ")
        print("Ejecuta este comando en la terminal:\n")
        print("'py -m pip install -r dependenciasCodigo.txt'")
        print("\nSi utiliza 🐧 Linux/macOS 🍎")
        print("Ejecuta uno de estos comandos en la terminal:\n")
        print("'python3 -m pip install -r dependenciasCodigo.txt'")
        print("o")
        print("'python -m pip install -r dependenciasCodigo.txt'")
        print("\nSi utiliza otro Sistema Operativo use el comando adecuado para su sistema.")
 
        sys.exit("\nInstala los paquetes faltantes antes de continuar.")

# Verificación al iniciar el programa
verificar_dependencias()

# Importación de bibliotecas necesarias

#re permite trabajar con expresiones regulares.
import re 
#requests permite hacer peticiones HTTP para descargar el contenido de páginas web.
import requests
#mechanize simula un navegador web básico en Python.
import mechanize
#BeautifulSoup analiza y extrae contenido específico del HTML
from bs4 import BeautifulSoup


# Mensaje de bienvenida al sistema
print("\nBienvenido/a al sistema de Extracción y análisis de páginas web.")

# Función principal para inspeccionar una URL
# Esta función solicita y valida una URL, luego analiza su contenido.
def inspeccionar_url():
    while True:
        buscar_url = input("\nPor favor, ingresa la URL que deseas analizar (debe comenzar con 'http://' o 'https://'): ").strip()
        if buscar_url.startswith(("http://", "https://")):
            break
        else:
            print("\nLa URL ingresada no es válida. Asegúrate de que comience con 'http://' o 'https://'. Intenta de nuevo ")

    # Se obtiene el HTML con requests y se usa manejo de errores.
    try:
        respuesta = requests.get(buscar_url)
        respuesta.raise_for_status()
        print("\nPágina obtenida exitosamente con *requests*")
        html = respuesta.text
    except requests.exceptions.RequestException as e:
        print(f"\nOcurrió un error al obtener la página: {e}")
        return

    # Se usa mechanize para simular un navegador
    try:
        br = mechanize.Browser()
        br.set_handle_robots(False)
        br.addheaders = [('User-agent', 'Mozilla/5.0')]
        br.open(buscar_url)
        print("\nNavegador *mechanize* inicializado correctamente")

        # Se inicia mechanize y se abre la página.
        print("\nExplorando enlaces con mechanize...\n")
        for i, link in enumerate(br.links()):
            if i >= 5:
                break
            try:
                print(f"Enlace {i+1}: {link.url}")
                br.follow_link(link)
                pagina = br.response().read()
                pagina_soup = BeautifulSoup(pagina, 'html.parser')
                title = pagina_soup.title.string if pagina_soup.title else "Sin título"
                print("Título:", title)
                print("-" * 40)
                br.back()
            except Exception as e:
                print(f"\nLo siento, no se pudo seguir el enlace: {e}")

    except Exception as e:
        print(f"\nLo siento,No se pudo abrir la página con mechanize: {e}")

    # Se extraen los enlaces del HTML utilizando BeautifulSoup.
    soup = BeautifulSoup(html, 'html.parser')
    links = [link.get('href') for link in soup.find_all('a', href=True)]
    print("\nEnlaces encontrados en la página con BeautifulSoup:")
    if links:
        for link in links[:10]:
            print(" -", link)
    else:
        print("\nLo siento, no se encontraron enlaces en esta página.")

    # Extrae los primeros párrafos.
    parrafos = soup.find_all('p')
    print("\nPrimeros párrafos encontrados:")
    if parrafos:
        for p in parrafos[:5]:
            print(" →", p.get_text(strip=True))
    else:
        print("\nLo siento, no se encontraron párrafos en esta página.")

    # Busqueda de correos
    # La siguente línea busca todos los textos en sub_html que tengan el formato de un correo electrónico y devuelve una lista con todos ellos.
    emails = re.findall(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", html)
    print("\nCorreos electrónicos detectados:")
    if emails:
        for email in emails:
            print(" →", email)
    else:
        print("\nLo siento, no se encontraron correos en la página principal.")

    #Se analizan los primeros enlaces encontrados de las subpáginas y se extrae información útil.
    print("\nAnalizando algunas subpáginas...\n")
    for i, link in enumerate(links[:5]):
        full_url = link if link.startswith('http') else buscar_url + link
        try:
            sub_respuesta = requests.get(full_url)
            sub_respuesta.raise_for_status()
            sub_html = sub_respuesta.text
            sub_soup = BeautifulSoup(sub_html, 'html.parser')
            print(f"Subpágina {i+1}: {full_url}")

            # Título
            titulo = sub_soup.title.string if sub_soup.title else "Sin título"
            print("Título:", titulo)

            # Primer párrafo
            sub_parrafo = sub_soup.find('p')
            if sub_parrafo:
                print("Primer párrafo:", sub_parrafo.get_text(strip=True))
            else:
                print("\nLo siento, no se encontró ningún párrafo.")

            # Correos en subpágina
            sub_emails = re.findall(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", sub_html)
            if sub_emails:
                print("Correos encontrados:")
                for email in sub_emails:
                    print("    →", email)
            else:
                print("\nLo siento, no se encontraron correos.")

            print("-" * 50)
        except requests.exceptions.RequestException as e:
            print(f"\nNo se pudo acceder a {full_url}: {e}")

# Función que permite controlar el flujo del programa y consulta si desea analizar otro sitio web o no.
# Si el usuario no desea continuar se indica el final del programa.
# Se valida que la opción esté correcta, si no lo está vuelve al ciclo y pregunta de nuevo. 
def main():
    while True:
        inspeccionar_url()
        while True:
            seguir = input("\n¿Te gustaría analizar otra URL? (S/N): ").upper()
            if seguir == "S":
                break
            elif seguir == "N":
                print("\nGracias por usar el sistema. ¡Hasta pronto!")
                return
            else:
                print("\nPor favor, ingresa una opción válida: S/N ")

# Ejecución principal
main()