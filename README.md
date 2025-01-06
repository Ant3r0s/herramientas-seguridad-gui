# Herramientas de Seguridad con Interfaz Gráfica

Este proyecto es una colección de herramientas de seguridad diseñadas para ejecutarse desde una interfaz gráfica simple y funcional, enfocada en usuarios que desean realizar pruebas de pentesting y análisis sin necesidad de usar la consola directamente.

## Características

- **Interfaz gráfica intuitiva (rollo Matrix)**.
- Instalación automática de herramientas como:
  - `Hashcat`
  - `Hydra`
  - Tipos de Ping personalizados
  - Phishing de correos
- Resultados visibles directamente en la interfaz gráfica.
- Soporte para distribuciones basadas en Arch Linux y otras.

## Requisitos

- Python 3.x
- Librerías de Python:
  - `tkinter`
  - `subprocess`
  - `os`
  - `requests`
- Permisos de superusuario para algunas herramientas.

## Instalación

1. **Clona el repositorio:**
   ```bash
   git clone https://github.com/Ant3r0s/herramientas-seguridad-gui.git
   cd herramientas-seguridad-gui
