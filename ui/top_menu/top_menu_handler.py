from core.app_state import APP_STATE, ALL_COLUMNS

def get_menu_handlers(app_context):
    """Retorna os handlers (ações) dos itens do menu superior."""
    def limpar_tabela():
        # 1. Limpa os dados globais
        APP_STATE.update({
            "dados": [],
            "dados_extraidos": {},
            "pdfs_carregados": {}
        })
        
        # 2. Reseta colunas visíveis
        APP_STATE["colunas_visiveis"] = set(ALL_COLUMNS.keys())
        for var in APP_STATE["colunas_menu_vars"].values():
            var.set(True)
        
        # 3. Atualiza tabela
        if APP_STATE.get("atualizar_tabela_callback"):
            APP_STATE["atualizar_tabela_callback"]([])
        
        # 4. Chama a sidebar DE FORMA EXPLÍCITA
        if APP_STATE.get("sidebar_instance"):
            APP_STATE["sidebar_instance"].limpar_documentos()
        elif APP_STATE.get("atualizar_sidebar_callback"):
            APP_STATE["atualizar_sidebar_callback"]()
        
        print("✅ Sistema completamente limpo")
        
    return {
        "abrir": lambda: print("Abrir PDFs..."),
        "exportar": lambda: print("Exportando Excel..."),
        "limpar": limpar_tabela,  # Usa a função atualizada
        "atualizar_tabela": lambda: (
            APP_STATE["atualizar_tabela_callback"](APP_STATE["dados"]) 
            if APP_STATE["atualizar_tabela_callback"] 
            else None
        ),
    }
