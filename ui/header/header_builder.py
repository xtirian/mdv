# ui/header.py
import customtkinter as ctk
from export.excel_exporter import export_to_excel
from export.pdf_exporter import export_to_pdf  # <-- Importa nova função
from ui.buttons import CustomButtonRed, CustomButtonWhite

class Header(ctk.CTkFrame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, height=75, **kwargs)
        self.pack_propagate(False)
        self.configure(fg_color="#FFFFFF")
        self.build()

    def build(self):
        # Título
        self.title_label = ctk.CTkLabel(
            self, padx=16, text="PDF Data Extractor", 
            font=("Arial", 20, "bold")
        )
        self.title_label.pack(side="left")

        # Container de botões
        self.button_box = ctk.CTkFrame(self, fg_color="transparent")
        self.button_box.pack(side="right")

        # Botões com handlers
        btn_excel = CustomButtonWhite(
            self.button_box, 
            text="Exportar para Excel", 
            icon_type="excel",
            command=self.handle_export_excel
        )

        #btn_pdf = CustomButtonRed(
        #    self.button_box, 
        #    text="Exportar para PDF", 
        #    icon_type="pdf",
        #    command=self.handle_export_pdf
        #)

        btn_excel.pack(side="left", padx=(16, 8))
        #btn_pdf.pack(side="left", padx=(8, 16))

    def handle_export_excel(self):
        result = export_to_excel()
        self.show_export_result(result)

    def handle_export_pdf(self):
        result = export_to_pdf()
        self.show_export_result(result)

    def show_export_result(self, result):
        if result["success"]:
            self.title_label.configure(
                text="Exportação concluída!",
                text_color="#2e7d32"  # Verde escuro
            )
            print(result["message"])  # Log no console
        else:
            self.title_label.configure(
                text=result["message"],
                text_color="#c62828"  # Vermelho escuro
            )

        # Retorna ao texto original após 5 segundos
        self.after(5000, lambda: self.title_label.configure(
            text="PDF Data Extractor",
            text_color="#000000"
        ))
