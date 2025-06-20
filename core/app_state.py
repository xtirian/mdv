# core/app_state.py

# Todas as colunas possíveis
ALL_COLUMNS = {
    "Grupo": True, 
    "Cota": True, 
    "Nome do Cliente": True, 
    "Contrato": True, 
    "Data e Hora": True, 
    "Pessoa": True, 
    "CPF/CNPJ": True, 
    "Data Venda": True,
    "Plano Básico": True,
    "Cidade": True, 
    "Telefone": True, 
    "Valor Crédito": True, 
    "Produto": True, 
    "SubProduto": True, 
    "Sit. Cobrança": True, 
    "Dt. Contemplação": True, 
    "Tipo Contempl.": True, 
    "Líquido a Pagar": True,  
    "% Pago": True, 
    "Último Reajuste": True, 
    "Parcelas Faltantes": True, 
    "Saldo Devedor": True, 
    "Val. Disponíveis Encerramento": True
}

# Estado global da aplicação
APP_STATE = {
    "colunas_visiveis": set(ALL_COLUMNS),  # inicialmente todas visíveis
    "colunas_menu_vars": {},               # preenchido depois pelo menu
    "atualizar_sidebar_callback": None,
    "atualizar_tabela_callback": None,
    "dados_extraidos": {},
    "pdfs_carregados": {},
    "ordem_colunas": [],  # Nova chave para armazenar a ordem
    "main_content_ref": None  # Referência ao MainContent
}

