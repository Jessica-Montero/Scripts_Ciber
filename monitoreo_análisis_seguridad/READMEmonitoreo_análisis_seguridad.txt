# SECUREPY (Security in Python)

## Descripción
SECUREPY es un **sistema de monitoreo y análisis de seguridad** desarrollado en Python.  
Proporciona una suite integral de herramientas para **detectar, analizar y prevenir amenazas de ciberseguridad en tiempo real**, siendo útil tanto para estudiantes como para profesionales.

---

## 🛡️ Objetivo Principal
Proporcionar una suite de ciberseguridad que monitorea redes, analiza registros, detecta vulnerabilidades y genera informes de seguridad de manera educativa y práctica.

---

## 📦 Módulos Principales

### 1. Monitoreo de Red
- Analiza tráfico en tiempo real usando **Scapy**.  
- Detecta escaneos de puertos, tráfico ICMP/UDP sospechoso y conexiones a puertos críticos.  
- Registra hallazgos en `hallazgos_red.txt`.  

### 2. Análisis de Registros
- Examina logs del sistema (`auth.log` en Linux, `Security.evtx` en Windows).  
- Detecta intentos fallidos de login y cambios sospechosos en usuarios.  

### 3. Detección de Vulnerabilidades
- Escanea hosts y servicios con **Nmap**.  
- Genera reportes legibles de puertos abiertos y servicios detectados.  

### 4. Prevención de Ataques
- Simula bloqueo de IPs tras múltiples intentos fallidos.  
- Permite agregar reglas personalizadas (IPs o puertos).  
- Integra con `iptables` (Linux) y `netsh` (Windows) para bloqueos reales.  

### 5. Análisis de Tráfico Web
- Escanea URLs en busca de patrones maliciosos (inyección SQL, scripts).  
- Guarda resultados en `analisis_web.txt`.  

### 6. Alertas y Notificaciones
- Registra alertas en `alertas.txt`.  
- Permite enviar alertas por correo electrónico (configurable con Gmail).  

### 7. Registro de Incidentes
- Permite registrar manualmente incidentes de seguridad.  
- Guarda tipo, descripción e IP en `registro_incidentes.txt`.  

### 8. Informes de Seguridad
- Genera un **PDF profesional** con hallazgos de todos los módulos.  
- Incluye recomendaciones generales de seguridad.  

---

## ⚙️ Características Técnicas
- **Multiplataforma:** Funciona en Windows, Linux y macOS.  
- **Dependencias:** Scapy, evtx, fpdf, requests, BeautifulSoup (bs4).  
- **Interfaz por Menú:** Fácil de usar desde la terminal.  
- **Persistencia de Datos:** Guarda logs y hallazgos en archivos de texto.  

---

## 🎯 Uso Previsto
- **Administradores de sistemas:** Monitoreo de redes y servidores.  
- **Analistas de seguridad:** Investigación de incidentes y generación de reportes.  
- **Estudiantes de ciberseguridad:** Herramienta educativa para aprender detección de amenazas y análisis forense.  

---

## ⚠️ Consideraciones
- Algunas funcionalidades (como bloqueo de IPs) requieren permisos de administrador.  
- El envío de correos requiere configurar credenciales de Gmail.  
- El escaneo con Nmap puede ser lento y requiere instalación previa.  

---

## 📌 Conclusión
SECUREPY es una herramienta educativa y profesional que integra múltiples técnicas de ciberseguridad en un solo sistema.  
Ideal para aprender sobre **detección de amenazas, análisis forense y respuesta ante incidentes**.