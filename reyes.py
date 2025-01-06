import os
import subprocess
import platform
import tkinter as tk
from tkinter import messagebox, simpledialog
import threading

# --- Utilidades ---
def verificar_instalacion(herramienta):
    try:
        subprocess.run([herramienta, "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(f"{herramienta} ya está instalada.")
    except subprocess.CalledProcessError:
        print(f"{herramienta} no está instalada. Procediendo con la instalación...")
        instalar_herramienta(herramienta)

def obtener_so():
    sistema = platform.system().lower()
    return sistema

def instalar_herramienta(herramienta):
    sistema = obtener_so()
    if sistema == 'linux':
        if os.path.exists("/usr/bin/apt-get"):  # Para sistemas basados en Debian (Ubuntu, etc.)
            if herramienta == "wpscan":
                subprocess.run(["gem", "install", "wpscan"], check=True)
            elif herramienta == "nmap":
                subprocess.run(["sudo", "apt-get", "install", "-y", "nmap"], check=True)
            elif herramienta == "hashcat":
                subprocess.run(["sudo", "apt-get", "install", "-y", "hashcat"], check=True)
            elif herramienta == "hydra":
                subprocess.run(["sudo", "apt-get", "install", "-y", "hydra"], check=True)
            elif herramienta == "setoolkit":
                subprocess.run(["sudo", "apt-get", "install", "-y", "setoolkit"], check=True)
        elif os.path.exists("/usr/bin/pacman"):  # Para Arch Linux
            if herramienta == "wpscan":
                subprocess.run(["gem", "install", "wpscan"], check=True)
            elif herramienta == "nmap":
                subprocess.run(["sudo", "pacman", "-S", "--noconfirm", "nmap"], check=True)
            elif herramienta == "hashcat":
                subprocess.run(["sudo", "pacman", "-S", "--noconfirm", "hashcat"], check=True)
            elif herramienta == "hydra":
                subprocess.run(["sudo", "pacman", "-S", "--noconfirm", "hydra"], check=True)
            elif herramienta == "setoolkit":
                subprocess.run(["sudo", "pacman", "-S", "--noconfirm", "setoolkit"], check=True)
        else:
            print(f"No se puede instalar {herramienta} automáticamente en este sistema operativo.")
    else:
        print(f"No se puede instalar {herramienta} automáticamente en este sistema operativo.")

# --- Funciones de la GUI ---
def instalar_herramientas_gui():
    herramienta = simpledialog.askstring("Instalar Herramienta", "Introduce la herramienta que deseas instalar:\n(wpscan, nmap, hashcat, hydra, setoolkit)")
    if herramienta:
        instalar_herramienta(herramienta)

def abrir_ping_tipo():
    # Ventana de selección de tipo de ping
    ping_window = tk.Toplevel(root)
    ping_window.title("Tipos de Ping")
    ping_window.geometry("400x300")
    
    # Crear botones para los diferentes tipos de ping
    tk.Button(ping_window, text="Ping Normal", bg="green", fg="white", font=("Courier", 12), command=lambda: hacer_ping("normal", ping_window)).pack(pady=10)
    tk.Button(ping_window, text="Ping de la Muerte", bg="green", fg="white", font=("Courier", 12), command=lambda: hacer_ping("ping_muerte", ping_window)).pack(pady=10)
    tk.Button(ping_window, text="Ping con Opciones", bg="green", fg="white", font=("Courier", 12), command=lambda: hacer_ping("opciones", ping_window)).pack(pady=10)

def hacer_ping(tipo, ventana):
    ip = simpledialog.askstring("Ping", "Introduce la IP o dominio:")
    if ip:
        if tipo == "normal":
            comando = ["ping", ip]
        elif tipo == "ping_muerte":
            comando = ["ping", "-f", ip]  # Ping de la muerte (requiere permisos elevados)
        elif tipo == "opciones":
            opciones = simpledialog.askstring("Opciones Ping", "Introduce las opciones que deseas (ej. -c 10 para 10 paquetes):")
            comando = ["ping"] + opciones.split() + [ip]
        
        # Ejecutar el comando y mostrar el resultado
        ejecutar_comando(comando, ventana)

def ejecutar_comando(comando, ventana):
    # Creamos una ventana donde se verá el progreso
    resultado_window = tk.Toplevel(ventana)
    resultado_window.title("Resultado del Comando")
    resultado_window.geometry("500x300")

    text_widget = tk.Text(resultado_window, height=15, width=60)
    text_widget.pack(padx=10, pady=10)

    # Hacer funcionar el comando en un hilo para no congelar la interfaz
    threading.Thread(target=ejecutar_y_mostrar, args=(comando, text_widget)).start()

def ejecutar_y_mostrar(comando, text_widget):
    # Ejecutar el comando y capturar su salida
    proceso = subprocess.Popen(comando, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    for line in proceso.stdout:
        text_widget.insert(tk.END, line)
        text_widget.yview(tk.END)  # Desplazar la vista hacia abajo para ver la nueva línea

    for line in proceso.stderr:
        text_widget.insert(tk.END, line)
        text_widget.yview(tk.END)

    proceso.wait()

# Funciones para los ataques de Hashcat y Hydra
def atacar_hashcat():
    archivo_hash = simpledialog.askstring("Hashcat", "Introduce el archivo de hashes para atacar:")
    diccionario = simpledialog.askstring("Hashcat", "Introduce la ruta del diccionario:")
    if archivo_hash and diccionario:
        ejecutar_comando(["hashcat", "-m", "0", archivo_hash, diccionario])

def ataque_hydra():
    servicio = simpledialog.askstring("Hydra", "Introduce el servicio objetivo (ej. ssh, ftp):")
    ip = simpledialog.askstring("Hydra", "Introduce la IP o dominio de destino:")
    usuario = simpledialog.askstring("Hydra", "Introduce el nombre de usuario:")
    diccionario = simpledialog.askstring("Hydra", "Introduce la ruta del diccionario de contraseñas:")
    if servicio and ip and usuario and diccionario:
        ejecutar_comando(["hydra", "-l", usuario, "-P", diccionario, ip, servicio])

# Función para phishing (definido sin argumento ventana)
def phishing_email():
    email = simpledialog.askstring("Phishing Email", "Introduce el correo objetivo para phishing:")
    if email:
        ejecutar_comando(["setoolkit", "--phishing", "--target", email])

# --- Interfaz gráfica principal ---
def herramientas_gui():
    herramientas_window = tk.Toplevel(root)
    herramientas_window.title("Herramientas")
    herramientas_window.geometry("500x500")

    # Botones de herramientas
    tk.Button(herramientas_window, text="Phishing Email", bg="green", fg="white", font=("Courier", 12), command=phishing_email).pack(pady=10)
    tk.Button(herramientas_window, text="Escanear Web", bg="green", fg="white", font=("Courier", 12), command=abrir_escaneo_web).pack(pady=10)
    tk.Button(herramientas_window, text="Escanear Puertos", bg="green", fg="white", font=("Courier", 12), command=abrir_escaneo_puertos).pack(pady=10)
    tk.Button(herramientas_window, text="Escanear Red", bg="green", fg="white", font=("Courier", 12), command=abrir_escaneo_red).pack(pady=10)
    tk.Button(herramientas_window, text="Ataque Hashcat", bg="green", fg="white", font=("Courier", 12), command=atacar_hashcat).pack(pady=10)
    tk.Button(herramientas_window, text="Ataque Hydra", bg="green", fg="white", font=("Courier", 12), command=ataque_hydra).pack(pady=10)
    tk.Button(herramientas_window, text="Ping", bg="green", fg="white", font=("Courier", 12), command=abrir_ping_tipo).pack(pady=10)

def salir():
    root.quit()

# --- Interfaz gráfica principal ---
def iniciar_gui():
    global root
    root = tk.Tk()
    root.title("Simulador de Ingeniería Social")
    root.geometry("500x500")
    root.config(bg="black")

    # Menú principal de botones
    tk.Button(root, text="Instalar Herramientas", bg="green", fg="white", font=("Courier", 12), command=instalar_herramientas_gui).pack(pady=20)
    tk.Button(root, text="Abrir Herramientas", bg="green", fg="white", font=("Courier", 12), command=herramientas_gui).pack(pady=20)
    tk.Button(root, text="Salir", bg="red", fg="white", font=("Courier", 12), command=salir).pack(pady=20)

    root.mainloop()

if __name__ == "__main__":
    iniciar_gui()
