import tkinter as tk  # customtkinter não tem suporte a menus nativamente
from core.app_state import APP_STATE, ALL_COLUMNS

def build_top_menu(root, handlers=None):
    """
    Cria e configura o menu superior da aplicação.
    
    :param root: Janela principal (tk.Tk ou ctk.CTk)
    :param handlers: dicionário com callbacks para os itens de menu
    """
    handlers = handlers or {}

    menu_bar = tk.Menu(root)

    # === Menu Arquivo ===
    menu_arquivo = tk.Menu(menu_bar, tearoff=0)    
    menu_arquivo.add_command(label="Sair", command=root.quit)
    menu_bar.add_cascade(label="Arquivo", menu=menu_arquivo)

    # === Menu Editar ===
    menu_editar = tk.Menu(menu_bar, tearoff=0)
    menu_editar.add_command(label="Limpar", command=handlers.get("limpar"))
    menu_bar.add_cascade(label="Editar", menu=menu_editar)

    # ----- Menu Tabela -----
    menu_tabela = tk.Menu(menu_bar, tearoff=0)

    # Criar checkbuttons para cada coluna
    for coluna in ALL_COLUMNS:
        var = tk.BooleanVar(value=ALL_COLUMNS[coluna])
        APP_STATE["colunas_menu_vars"][coluna] = var

        def toggle(col=coluna, var_ref=var):
            if var_ref.get():
                APP_STATE["colunas_visiveis"].add(col)
            else:
                APP_STATE["colunas_visiveis"].discard(col)

            # Chama a função de atualização da tabela, se existir
            if APP_STATE["atualizar_tabela_callback"]:
                APP_STATE["atualizar_tabela_callback"]()

        menu_tabela.add_checkbutton(
            label=coluna,
            variable=var,
            command=toggle
        )

    # Comando para forçar atualização manual (caso necessário)
    menu_tabela.add_separator()
    menu_tabela.add_command(label="Atualizar agora", command=handlers.get("atualizar_tabela"))

    menu_bar.add_cascade(label="Tabela", menu=menu_tabela)

    # Aplica à janela principal
    root.config(menu=menu_bar)