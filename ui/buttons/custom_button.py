import os
from PIL import Image
import customtkinter as ctk


class CustomButtonRed(ctk.CTkButton):
    def __init__(self, master=None, icon_type=None, **kwargs):
        super().__init__(
            master,
            fg_color="#CC092F",
            text_color="#EEEEEE",
            hover=True,
            image=self.load_icon(icon_type, color="branco"),
            font=("Arial", 16, "bold"),     
            width=200,   # por exemplo, largura maior para mais "padding"
            height=40,   
            **kwargs
        )

    def load_icon(self, icon_type, color):
        icon_filename = {
            "doc": f"adicionar-ficheiro-{color}.png",
            "pdf": f"simbolo-de-formato-de-arquivo-pdf-{color}.png",
            "excel": f"extensao-de-formato-de-arquivo-xlsx-{color}.png"
        }.get(icon_type)

        if not icon_filename:
            return None

        project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        icon_path = os.path.join(project_root, "assets", "icons", icon_filename)

        if not os.path.exists(icon_path):
            print(f"Ícone não encontrado: {icon_path}")
            return None

        image = Image.open(icon_path)
        return ctk.CTkImage(image, size=(20, 20))


class CustomButtonWhite(ctk.CTkButton):
    def __init__(self, master=None, icon_type=None, **kwargs):
        super().__init__(
            master,
            fg_color="#FFF",
            text_color="#CC092F",
            hover=True,
            image=self.load_icon(icon_type, color="vermelho"),
            font=("Arial", 16, "bold"),      
            width=200,   
            height=40,          
            border_width=1,
            border_color="#EEE",
            **kwargs
        )

    def load_icon(self, icon_type, color):
        icon_filename = {
            "doc": f"adicionar-ficheiro-{color}.png",
            "pdf": f"simbolo-de-formato-de-arquivo-pdf-{color}.png",
            "excel": f"extensao-de-formato-de-arquivo-xlsx-{color}.png"
        }.get(icon_type)

        if not icon_filename:
            return None

        project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        icon_path = os.path.join(project_root, "assets", "icons", icon_filename)

        if not os.path.exists(icon_path):
            print(f"Ícone não encontrado: {icon_path}")
            return None

        image = Image.open(icon_path)
        return ctk.CTkImage(image, size=(20, 20))
