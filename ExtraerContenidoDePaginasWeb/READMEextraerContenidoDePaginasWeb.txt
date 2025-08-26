# Extractor y Analizador de Contenido Web

## Descripción
Este proyecto es un **extractor y analizador de contenido web** desarrollado en Python.  
Permite obtener información de páginas HTML, incluyendo enlaces, párrafos y correos electrónicos, y simula navegación web para análisis educativo.

---

## 🎯 Funcionalidades principales

### 1. Extracción de enlaces
- Obtiene todos los enlaces (`<a href>`) de la página principal.  
- Utiliza **BeautifulSoup** para parsear el HTML.

### 2. Navegación simulada
- Simula un navegador web usando **mechanize**.  
- Sigue los primeros 5 enlaces y muestra sus títulos.

### 3. Extracción de texto
- Obtiene los párrafos (`<p>`) de la página.  
- Muestra los primeros 5 párrafos de contenido.

### 4. Detección de correos electrónicos
- Busca patrones de emails usando expresiones regulares.  
- **Ejemplo:** `usuario@dominio.com`

### 5. Análisis de subpáginas
- Accede a los primeros 5 enlaces encontrados.  
- Extrae títulos, párrafos y correos de cada subpágina.

---

## 🔧 Tecnologías utilizadas
- `requests` → Para descargar contenido HTML  
- `mechanize` → Simula un navegador web (clic en enlaces, navegación)  
- `BeautifulSoup` → Analiza y extrae datos del HTML  
- `re` → Expresiones regulares para encontrar correos electrónicos  

---

## 🖥️ Flujo de ejecución
1. Verifica que estén instaladas las dependencias (`bs4`, `mechanize`, `requests`).  
2. Solicita una URL válida (debe empezar con `http://` o `https://`).  
3. Descarga el HTML de la página con `requests`.  
4. Simula navegación web con `mechanize`.  
5. Extrae enlaces, párrafos y correos con `BeautifulSoup`.  
6. Analiza las primeras 5 subpáginas.  
7. Pregunta al usuario si desea analizar otra URL.  

---

## 🎓 Uso educativo
Ideal para:  
- Aprender a extraer datos de páginas web.  
- Practicar web scraping y análisis de contenido.  
- Detectar información relevante como enlaces y correos electrónicos de forma segura.