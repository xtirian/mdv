import tkinter as tk
from tkinter import ttk
import tkinter.font as tkfont
from core.app_state import ALL_COLUMNS, APP_STATE

class MainContent(tk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, bg="#F5F5F5", **kwargs)

        container = tk.Frame(self, bg="#F5F5F5")
        container.pack(fill="both", expand=True, padx=24, pady=32, anchor="n")

        self.dados = []  # Guarda os dados atuais

        self.v_scrollbar = ttk.Scrollbar(container, orient="vertical")
        self.h_scrollbar = ttk.Scrollbar(container, orient="horizontal")

        self.tree = ttk.Treeview(
            container,
            columns=self.get_colunas_visiveis(),
            show="headings",
            yscrollcommand=self.v_scrollbar.set,
            xscrollcommand=self.h_scrollbar.set,
            selectmode="browse",
            height=20
        )

        self.v_scrollbar.config(command=self.tree.yview)
        self.h_scrollbar.config(command=self.tree.xview)

        self.tree.grid(row=0, column=0, sticky="nsew")
        self.v_scrollbar.grid(row=0, column=1, sticky="ns")
        self.h_scrollbar.grid(row=1, column=0, sticky="ew")

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # Fonte padrão e cabeçalho negrito
        style = ttk.Style(self)
        style.configure("Treeview",
                        font=("Arial", 11),
                        rowheight=28,
                        background="#FFFFFF",
                        foreground="#000000",
                        fieldbackground="#FFFFFF")
        style.configure("Treeview.Heading",
                        font=("Arial", 11, "bold"),
                        foreground="#CC092F")  # vermelho título

        # Estilo para linhas pares - cor suave vermelho claro
        style.map('Treeview', background=[('selected', '#CC092F')])
        style.configure("mystyle.Treeview", 
                        background="#FFFFFF", 
                        foreground="#000000",
                        fieldbackground="#FFFFFF")
        self.tree.tag_configure('oddrow', background='#FFFFFF')
        self.tree.tag_configure('evenrow', background='#FFE6E6')  # vermelho claro suave

        self.configurar_colunas()

    def get_colunas_visiveis(self):
        return [col for col in ALL_COLUMNS if col in APP_STATE["colunas_visiveis"]]
    
    def ajustar_largura_colunas(self):
        font = tkfont.Font(font=("Arial", 11))
        colunas_visiveis = self.get_colunas_visiveis()

        for col in colunas_visiveis:
            largura_max = font.measure(col) + 32  # Começa com largura do cabeçalho
            for item_id in self.tree.get_children():
                valor = self.tree.set(item_id, col)
                largura_valor = font.measure(str(valor)) + 32
                if largura_valor > largura_max:
                    largura_max = largura_valor

            self.tree.column(col, width=largura_max)


    def configurar_colunas(self):
        self.colunas_ordenadas = []  
        for col in self.tree["columns"]:
            self.tree.heading(col, text="")
            self.tree.column(col, width=0)

        colunas_visiveis = self.get_colunas_visiveis()
        self.tree.config(columns=colunas_visiveis)

        for col in colunas_visiveis:
            self.colunas_ordenadas.append(col)  # Armazena na ordem de exibição
            
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="w", minwidth=250)

    def atualizar_dados(self, dados):
        self.dados = dados 
        self.tree.delete(*self.tree.get_children())
        colunas_visiveis = self.get_colunas_visiveis()

        for i, linha in enumerate(dados):
            valores = [linha.get(col, "") for col in colunas_visiveis]
            tag = 'evenrow' if i % 2 == 1 else 'oddrow'
            self.tree.insert("", "end", values=valores, tags=(tag,))

        self.ajustar_largura_colunas()

    def atualizar_colunas(self):
        self.configurar_colunas()
        if "ordem_colunas" in APP_STATE:
            APP_STATE["ordem_colunas"] = self.colunas_ordenadas  
