import os
import tkinter as tk
from tkinter import ttk  
from ui.buttons import CustomButtonRed, CustomButtonWhite
from ui.side_bar.components import DocumentCard
from tkinter import filedialog
from pdf.pdf_extractor import extract_from_pdfs
from core.app_state import APP_STATE


class Sidebar(tk.Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, bg="#FFF", **kwargs)
        self.config(pady=16)
        self.configure(width=75)

        self.imported_documents = {
            # Adicione mais para testar o scroll...
        }
        self.build()
    
    def limpar_documentos(self):
        """Limpa todos os documentos importados"""
        print("\n=== LIMPANDO SIDEBAR ===")
        
        # 1. Limpa os dados locais
        self.imported_documents.clear()
        print("1. Dados locais limpos")
        
        # 2. Destroi todos os widgets dos documentos
        for widget in self.scrollable_docs.scrollable_frame.winfo_children():
            widget.destroy()
        print("2. Widgets destruídos")
        
        # 3. Adiciona mensagem de "vazio"
        tk.Label(
            self.scrollable_docs.scrollable_frame,
            text="Nenhum documento carregado",
            bg="#FFF",
            fg="#999"
        ).pack(pady=20)
        
        # 4. Força atualização
        self.update_idletasks()
        print("3. UI atualizada")
        
        print("✅ Sidebar completamente limpa\n")
    
    def build(self):
        btn1 = CustomButtonRed(self, text="Importar PDF", icon_type="doc", command=self.handle_import)
        btn1.pack(padx=16, pady=(0,8))  # Preencher largura e padding lateral

        spacer = tk.Frame(self, height=10, bg="#FFFFFF")
        spacer.pack()

        separator = ttk.Separator(self, orient="horizontal")
        separator.pack(fill="x")

        title = tk.Label(self, text="Documentos importados", font=("Arial", 14, "bold"), bg="#FFFFFF", pady=16)
        title.pack(anchor="w", padx=16)

        self.scrollable_docs = ScrollableFrame(self)
        self.scrollable_docs.pack(fill="y", expand=True, padx=(0,4), pady=(0, 16))

        self.build_imported_docs_section()


    def build_imported_docs_section(self):
        # Limpa cards antigos
        for widget in self.scrollable_docs.scrollable_frame.winfo_children():
            widget.destroy()

        # Cria novos cards
        for doc_id, data in self.imported_documents.items():
            selected = data.get("selected", False)
            card = DocumentCard(self.scrollable_docs.scrollable_frame, doc_id, data, selected=selected)
            card.pack(fill="x", pady=2)

    
    def handle_import(self):
        file_paths = filedialog.askopenfilenames(filetypes=[("PDF Files", "*.pdf")])
        if not file_paths:
            return

        # Se já existir label, destrói para criar um novo
        if hasattr(self, "loading_label"):
            self.loading_label.destroy()

        self.loading_label = tk.Label(self, text="", bg="#FFF", fg="blue", font=("Arial", 12, "italic"))
        self.loading_label.pack(pady=10)

        self.import_pdf(file_paths)


    def import_pdf(self, file_paths, index=0):
        total = len(file_paths)
        if index >= total:
            # Acabou a importação
            self.loading_label.config(text="Importação concluída!")
            self.after(1500, self.loading_label.destroy)
            self.build_imported_docs_section()
            
            # ATUALIZA A TABELA APENAS NO FINAL DE TODAS AS IMPORTAÇÕES
            if APP_STATE.get("atualizar_tabela_callback"):
                dados_para_tabela = []
                for doc_id, doc_data in APP_STATE.get("dados_extraidos", {}).items():
                    if doc_data:  # Se houver dados extraídos
                        dados_para_tabela.extend(doc_data)
                
                APP_STATE["atualizar_tabela_callback"](dados_para_tabela)
            return

        path = file_paths[index]
        file_name = os.path.basename(path)
        size = f"{os.path.getsize(path) // 1024}KB"

        # Atualiza UI
        self.loading_label.config(text=f"Importando {index+1} de {total}: {file_name}")
        self.update_idletasks()

        # Registra o documento
        doc_id = len(self.imported_documents) + 1
        self.imported_documents[doc_id] = {
            "title": file_name,
            "size": size,
            "date": "",  # Pode implementar extract_metadata depois
            "selected": False,
            "path": path
        }

        # Atualiza estado global
        APP_STATE["pdfs_carregados"] = {k: v["path"] for k, v in self.imported_documents.items()}

        try:
            # Extração dos dados (com tratamento de erro)
            dados = extract_from_pdfs([path])
            if "dados_extraidos" not in APP_STATE:
                APP_STATE["dados_extraidos"] = {}
            APP_STATE["dados_extraidos"][doc_id] = dados
        except Exception as e:
            print(f"Erro ao extrair {path}: {str(e)}")
            APP_STATE["dados_extraidos"][doc_id] = None

        # Agenda próximo arquivo
        self.after(100, lambda: self.import_pdf(file_paths, index + 1))

# ScrollableFrame igual ao seu, só certifique-se do bg e sticky
class ScrollableFrame(tk.Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        
        self.canvas = tk.Canvas(self, borderwidth=0, highlightthickness=0, bg="#FFF")
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg="#FFF")
        
        self.scrollable_frame_id = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        
        self.scrollable_frame.bind("<Configure>", self._on_frame_configure)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.scrollbar.grid(row=0, column=1, sticky="ns")
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.canvas.bind("<Configure>", self._on_canvas_configure)
    
    def _on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
    
    def _on_canvas_configure(self, event):
        canvas_width = event.width
        self.canvas.itemconfig(self.scrollable_frame_id, width=canvas_width)