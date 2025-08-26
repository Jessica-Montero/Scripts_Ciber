# Keylogger Educativo en Python

Este código es un **keylogger educativo** que captura las teclas presionadas por el usuario junto con información del sistema. Está diseñado **solo con fines de aprendizaje y pruebas en entornos controlados**.

---

##  Funcionalidades

1. **Recolección de información del sistema**  
   - Detecta el sistema operativo: Windows, Linux o macOS.  
   - Obtiene el modelo del procesador usando comandos del sistema:  
     - Linux: `lscpu`  
     - Windows: `wmic cpu get caption`  
     - macOS: `sysctl -n machdep.cpu.brand_string`

2. **Registro de teclas**  
   - Usa `pynput.keyboard` para monitorear el teclado.  
   - Guarda cada tecla presionada en `keylog.txt` junto con información del sistema.

3. **Formato de registro**  
   ```text
   sistema: Windows, procesador: Intel(R) Core(TM) i7-10750H, tecla: a
   sistema: Windows, procesador: Intel(R) Core(TM) i7-10750H, tecla: b
   Tecla especial: Key.space
   Tecla especial: Key.enter

Mecanismo de parada

El keylogger se detiene al presionar la tecla ESC.

* Aspectos éticos y legales

Este código no debe usarse sin consentimiento.

Su uso no autorizado es ilegal en la mayoría de países.

Úsalo solo en entornos controlados y con permiso explícito (por ejemplo, tu propio equipo).

* Tecnologías utilizadas

pynput.keyboard → Captura de teclas.

platform → Detección del sistema operativo.

subprocess → Ejecución de comandos del sistema y obtención de información del hardware.

* Uso legítimo

Pruebas de seguridad en tus propios equipos.

Monitoreo autorizado (por ejemplo, supervisión parental).

Investigación forense con consentimiento explícito.

Si encuentras un keylogger en un sistema sin tu consentimiento:

Desconéctate de internet.

Ejecuta un escaneo antivirus.

Cambia todas tus contraseñas.
