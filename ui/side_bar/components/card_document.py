from PIL import Image
import os
import customtkinter as ctk


class DocumentCard(ctk.CTkFrame):
    def __init__(self, master, doc_id, data, selected=False, **kwargs):
        super().__init__(master, fg_color="transparent", corner_radius=0, **kwargs)
        self.doc_id = doc_id
        self.data = data
        self.selected = selected

        self.build_card()

    def build_card(self):
        bg_color = "#FFF5F5" if self.selected else "#FFFFFF"
        title_color = "#CC092F" if self.selected else "#000000"

        # Container principal do card
        container = ctk.CTkFrame(self, fg_color=bg_color, corner_radius=0)
        container.pack(fill="x", pady=4)
        container.configure(height=75)
        container.pack_propagate(False)

        # Conteúdo interno com paddings
        content = ctk.CTkFrame(container, fg_color=bg_color)
        content.pack(fill="x", padx=(16, 24), pady=(12, 12))

        # Ícone PDF
        icon = self.load_icon("pdf")
        icon_label = ctk.CTkLabel(content, image=icon, text="", bg_color=bg_color)
        icon_label.image = icon
        icon_label.pack(side="left", padx=(0, 12))

        # Textos
        text_frame = ctk.CTkFrame(content, fg_color=bg_color)
        text_frame.pack(side="left", fill="both", expand=True)

        title = ctk.CTkLabel(
            text_frame,
            text=self.data["title"],
            font=("Arial", 12, "bold"),
            text_color=title_color,
            anchor="w"
        )
        title.pack(anchor="w")

        subtitle = ctk.CTkLabel(
            text_frame,
            text=f"{self.data['size']}  {self.data['date']}",
            font=("Arial", 10),
            text_color="#666666",
            anchor="w"
        )
        subtitle.pack(anchor="w")

    def load_icon(self, icon_type):
        icon_filename = {
            "pdf": "simbolo-de-formato-de-arquivo-pdf-vermelho.png" if self.selected else "simbolo-de-formato-de-arquivo-pdf-preto.png"
        }.get(icon_type)

        if not icon_filename:
            return None

        # Caminho relativo ao diretório raiz do projeto
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
        icon_path = os.path.join(project_root, "assets", "icons", icon_filename)

        if not os.path.exists(icon_path):
            print(f"[ERRO] Ícone não encontrado: {icon_path}")
            return None

        image = Image.open(icon_path)
        return ctk.CTkImage(image, size=(20, 20))
