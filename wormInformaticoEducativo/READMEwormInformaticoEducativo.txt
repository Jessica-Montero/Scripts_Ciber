# Gusano Educativo (Worm)

## Descripción
Este proyecto contiene un **gusano (worm) informático educativo** diseñado para demostraciones controladas de propagación en entornos de práctica.  
**Objetivo:** Enseñar cómo funcionan los gusanos, la persistencia en sistemas y la manipulación de archivos, de forma segura y educativa.

---

## 🔍 Funcionalidades principales

### 1. Recolección de información del sistema
- Obtiene detalles del sistema operativo, arquitectura, procesador y nombre de red del equipo.

### 2. Autoejecución
Se configura para ejecutarse automáticamente al iniciar el sistema:  
- **Windows:** se copia en la carpeta de Startup  
- **Linux/macOS:** modifica el archivo `.bashrc`

### 3. Búsqueda de archivos `.txt`
- Navega por carpetas comunes del usuario (Escritorio, Documentos, Descargas, etc.)  
- Permite seleccionar manualmente directorios para análisis.

### 4. Infección de archivos
- Crea copias de los archivos `.txt` encontrados, añadiendo al final

--- INFECTADO ---

- Copia todo el código del gusano original en los archivos copiados.

---

##⚠️ Características importantes
- **No destructivo:** Solo crea copias con `_infectado.txt` sin modificar los originales.  
- **Educativo:** Diseñado para prácticas académicas de seguridad informática.  
- **Multiplataforma:** Funciona en Windows, Linux y macOS.

---

## 🎯 Objetivo educativo
Demostrar cómo un gusano se propaga aprovechando:  
- Acceso al sistema de archivos  
- Mecanismos de persistencia (autoejecución)  
- Engaño al usuario mediante archivos aparentemente normales

---

## ⚠️ Advertencia
Este código debe usarse **solo en entornos controlados y con autorización explícita**.  
Replicar malware sin consentimiento es **ilegal** en la mayoría de jurisdicciones.