import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from ui.app_window import start_app
import os
import sys

def resource_path(relative_path):
    """Compatível com PyInstaller ou execução direta"""
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def mostrar_splash():
    splash = tk.Tk()
    splash.overrideredirect(True)
    splash.geometry("320x240")

    # Centralizar na tela
    x = splash.winfo_screenwidth() // 2 - 160
    y = splash.winfo_screenheight() // 2 - 120
    splash.geometry(f"+{x}+{y}")

    # Logo
    try:
        logo_path = resource_path("logo.ico")
        image = Image.open(logo_path)
        image = image.resize((64, 64))
        logo = ImageTk.PhotoImage(image)
        label_logo = tk.Label(splash, image=logo)
        label_logo.image = logo
        label_logo.pack(pady=(20, 10))
    except Exception as e:
        print(f"Erro ao carregar logo.ico: {e}")

    # Texto com porcentagem
    label_status = ttk.Label(splash, text="Carregando... 0%", font=("Arial", 11))
    label_status.pack(pady=(0, 10))

    # Barra de progresso
    progress = ttk.Progressbar(splash, orient="horizontal", length=200, mode="determinate")
    progress.pack(pady=(0, 20))
    progress["maximum"] = 100

    def atualizar_barra(percent=0):
        if percent > 100:
            splash.destroy()
            start_app()  # Chama a função principal do app
        else:
            progress["value"] = percent
            label_status.config(text=f"Carregando... {percent}%")
            splash.after(30, lambda: atualizar_barra(percent + 2))  # Ajuste de velocidade

    atualizar_barra()
    splash.mainloop()

if __name__ == "__main__":
    mostrar_splash()
