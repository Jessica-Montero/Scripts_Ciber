# Analizador de Redes y Sistemas Operativos

## Descripción
Este proyecto es un **analizador de redes y sistemas operativos** desarrollado en Python.  
Permite realizar diagnósticos de dominios y obtener información detallada del sistema local de manera educativa y práctica.

---

## 🎯 Funcionalidades principales

### 1. Resolución DNS
- Obtiene las direcciones IPv4 (tipo A) y IPv6 (tipo AAAA) de un dominio.  
- **Ejemplo:** Para `google.com` muestra sus IPs asociadas.

### 2. Consulta WHOIS
- Proporciona información sobre el registrante del dominio:  
  - Nombre del registrante  
  - Organización  
  - País  
  - Fecha de creación del dominio  

### 3. Prueba de conectividad (Ping)
- Ejecuta un comando ping al dominio (4 intentos).  
- Muestra el tiempo de respuesta y estadísticas de conectividad.

### 4. Información del sistema local
- Detecta y muestra detalles del sistema operativo donde se ejecuta:  
  - Tipo de sistema (Windows, Linux, macOS)  
  - Versión del SO  
  - Arquitectura (32/64 bits)  
  - Procesador  
  - Detalles adicionales según el SO  

---

## 🔧 Tecnologías utilizadas
- `dns.resolver` → Para consultas DNS  
- `whois` → Para información de registro de dominios  
- `subprocess` → Para ejecutar comandos del sistema (ping)  
- `platform` y `os` → Para detectar el sistema operativo  

---

## 🖥️ Multiplataforma
Funciona en:  
- ✅ Windows (nt)  
- ✅ Linux/Unix  
- ✅ macOS (Darwin)  

---

## 📋 Flujo de ejecución
1. Verifica que estén instaladas las dependencias (`dns` y `whois`).  
2. Solicita al usuario un dominio (ej: `google.com`).  
3. Realiza las cuatro funciones de análisis (DNS, WHOIS, Ping, sistema local).  
4. Pregunta si desea analizar otro dominio.  

---

## ⚠️ Validaciones
- Rechaza dominios que incluyan `http://`, `https://` o `www`.  
- Verifica que el dominio tenga al menos un punto (`.`).  
- Maneja errores como timeouts o dominios no resolubles.  

---

## 🎓 Uso educativo
Ideal para:  
- Aprender sobre redes DNS.  
- Entender cómo funciona WHOIS.  
- Practicar diagnóstico de conectividad.  
- Conocer detalles del sistema operativo donde se ejecuta.