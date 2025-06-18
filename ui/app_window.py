import os
import tkinter as tk
from tkinter import ttk
from pdf.pdf_extractor import extract_from_pdfs
from export.excel_exporter import export_to_excel
from ui.top_menu import build_top_menu, get_menu_handlers
from ui.side_bar import Sidebar
from ui.header import Header
from ui.main_content import MainContent
from core.app_state import APP_STATE
import sys

def start_app():
    root = tk.Tk()
    root.title("MDV Consórcios - Report App")
    root.minsize(1000, 600)  
    try:
        root.iconbitmap(resource_path("logo.ico"))
    except Exception as e:
        print(f"Erro ao carregar ícone: {e}")
    root.state('zoomed')

    # Configuração do menu (mantenha sua implementação atual)
    menu_handlers = get_menu_handlers(app_context=root)
    build_top_menu(root, menu_handlers)

    # Layout principal
    sidebar = Sidebar(root, width=int(1200*0.25))
    APP_STATE["sidebar_instance"] = sidebar  
    sidebar.pack(side="left", fill="y")

    right_container = tk.Frame(root)
    right_container.pack(side="left", fill="both", expand=True)

    header = Header(right_container)
    header.pack(side="top", fill="x")

    # Container do conteúdo principal
    main_content_frame = tk.Frame(right_container, bg="#F5F5F5")
    main_content_frame.pack(side="top", fill="both", expand=True)

    # Criação do componente MainContent
    main_content = MainContent(main_content_frame)
    main_content.pack(fill="both", expand=True, padx=20, pady=20)

    
    # Registra o callback corretamente (usando atualizar_dados)
    APP_STATE["atualizar_tabela_callback"] = main_content.atualizar_dados
    APP_STATE["main_content_ref"] = main_content
    APP_STATE["ordem_colunas"] = main_content.colunas_ordenadas

    # Dados de exemplo (pode remover depois)
    exemplo = [{
        "Grupo": "010020",
        "Cota": "234-1",
        "Nome do Cliente": "---",
        "Contrato": "7995138",
        "Data e Hora": "15/05/2025 16:32:01",
        "CPF/CNPJ": "14.189.784/0001-52",
        "Valor Crédito": "484.791,95",
        "Produto": "IMO IMOBILI",
        "Sit. Cobrança": "EXCLUIDO"
    }]
    main_content.atualizar_dados(exemplo)

    root.mainloop()


def resource_path(relative_path):
    """Converte caminhos relativos para caminhos absolutos compatíveis com PyInstaller"""
    try:
        base_path = sys._MEIPASS  # Pasta temporária do executável
    except AttributeError:
        base_path = os.path.abspath(".")  # Pasta normal em desenvolvimento
    
    return os.path.join(base_path, relative_path)