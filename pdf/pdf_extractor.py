import pdfplumber
from typing import List, Dict
import re
from datetime import datetime


def extract_from_pdfs(file_paths: List[str]) -> List[Dict[str, str]]:
    """Extrai dados de extratos de consórcio com precisão"""
    dados_consorcio = []
    
    for path in file_paths:
        with pdfplumber.open(path) as pdf:
            texto_completo = "\n".join(page.extract_text() for page in pdf.pages if page.extract_text())
            dados = parse_extrato_consorcio(texto_completo)
            dados_consorcio.append(dados)
    
    return dados_consorcio

def parse_extrato_consorcio(texto: str) -> Dict[str, str]:
    """Parser refinado para extrair todos os campos corretamente"""
    dados = {
        "Data e Hora": extrair_data_hora_segunda_linha(texto),
        "Grupo": extrair_valor(texto, "Grupo:"),
        "Cota": extrair_valor(texto, "Cota:"),
        "Nome do Cliente": extrair_nome_cliente(texto),
        "Contrato": extrair_valor(texto, "Contrato:"),
        "Pessoa": "Jurídica" if "Pessoa: Jurídica" in texto else "Física",
        "CPF/CNPJ": extrair_valor(texto, "CPF/CNPJ:"),
        "Data Venda": extrair_valor(texto, "Data Venda:"),
        "Plano Básico": extrair_valor(texto, "Plano Básico:")+ " meses",
        "Cidade": extrair_cidade(texto),
        "Telefone": extrair_telefone(texto),
        "Valor Crédito": extrair_valor_credito(texto),
        "Produto": extrair_produto(texto),
        "SubProduto": extrair_subproduto(texto),
        "Sit. Cobrança": extrair_situacao_cobranca(texto),
        "Dt. Contemplação": extrair_valor(texto, "Dt. Contemplação:"),
        "Tipo Contempl.": extrair_tipo_contemplacao(texto),
        "Líquido a Pagar": extrair_liquido_pagar(texto),
        "% Pago": extrair_percentual_pago(texto),
        "Último Reajuste": extrair_valor(texto, "Último reajuste em:"),
        "Parcelas Faltantes": extrair_parcelas_faltantes(texto),
        "Saldo Devedor": extrair_saldo_devedor(texto),
        "Val. Disponíveis Encerramento": "0",
    }

    
    return dados

# Funções auxiliares específicas para cada campo
import re

def extrair_tipo_contemplacao(texto: str) -> str:
    # Padrão para capturar o tipo (ignora maiúsculas/minúsculas)
    padrao = r"Tipo\s+Contempl\.?:\s*(.*?)(?:\s+[A-Z][a-z]+:|$)"
    match = re.search(padrao, texto, re.IGNORECASE)
    
   
    if not match:
        return "NÃO CONTEMPLADO"
    
    tipo = match.group(1).strip().upper().split(" VALOR A DEVOLVER")[0].strip()
    
    print(tipo)    

    if not tipo:
        return "---"
    elif "VALOR A DEVOLVER" in tipo:
        return "NÃO CONTEMPLADO"
    elif "LANCE" in tipo:
        return "LANCE"
    else:
        return tipo

def extrair_data_hora_segunda_linha(texto: str) -> str:
    linhas = texto.strip().splitlines()
    if len(linhas) < 2:
        return "---"

    segunda_linha = linhas[1].strip()

    # Regex para data e hora: dd/mm/aaaa hh:mm:ss
    padrao_data_hora = r"^\d{2}/\d{2}/\d{4} \d{2}:\d{2}:\d{2}$"

    if re.match(padrao_data_hora, segunda_linha):
        try:
            # Valida se a data e hora são reais
            datetime.strptime(segunda_linha, "%d/%m/%Y %H:%M:%S")
            return segunda_linha
        except ValueError:
            return "---"
    else:
        return "---"


def extrair_nome_cliente(texto: str) -> str:
    padrao = r"Cota:\s*\d+-\d{1,2}\s+(.*?)\s+Contrato:?"
    match = re.search(padrao, texto, re.IGNORECASE)
    
    if match:
        nome = match.group(1).strip()
        nome = re.sub(r'\s+', ' ', nome).strip()
        return nome if nome else "---"
    return "---"


def extrair_valor_credito(texto: str) -> str:
    padrao = r"Valor Crédito:\s*([\d\.,]+)"
    matches = re.findall(padrao, texto)
    if matches:
        return matches[-1].replace(".", "").replace(",", ".")
    return "0"

def extrair_produto(texto: str) -> str:
    padrao = r"Produto:\s*(.+)"
    match = re.search(padrao, texto)
    return match.group(1).strip() if match else "---"

def extrair_subproduto(texto: str) -> str:
    padrao = r"SubProduto:\s*(.+)"
    match = re.search(padrao, texto)
    return match.group(1).strip() if match else "---"

def extrair_situacao_cobranca(texto: str) -> str:
    padrao = r"Sit\. de Cobrança:\s*([A-ZÇÃ\s]+)"
    match = re.search(padrao, texto)
    return match.group(1).strip() if match else "---"

def extrair_liquido_pagar(texto: str) -> float:
    padrao = r"(?:Valor\s+[àa]\s+Devolver:)\s*([\d\.]+,\d{2})"
    match = re.search(padrao, texto, re.IGNORECASE)
    return float(match.group(1).replace(".", "").replace(",", ".")) if match else 0.0



def extrair_percentual_pago(texto: str) -> float:
    padrao = r"TOTAL\s+([\d,]+)"
    match = re.search(padrao, texto, re.IGNORECASE)
    if match:
        return float(match.group(1).replace(",", "."))
    return 0.0



def extrair_parcelas_faltantes(texto: str) -> str:
    padrao = r"Resumo Parcelas a Pagar.*?Qtde Total:\s*([\d.,]+)"
    match = re.search(padrao, texto, re.DOTALL)
    return match.group(1) if match else "0"


def extrair_saldo_devedor(texto: str) -> str:
    padrao_secao = r"Valores\s+/\s+Percentuais\s+a\s+Pagar.*?(TOTAL\s+[\d\.]+,\d{2}.*?)\n"
    matches = re.findall(r"TOTAL\s+([\d\.]+,\d{2})", texto, re.IGNORECASE)

    if not matches:
        return "0.00"
    
    valor = matches[-1].replace(".", "").replace(",", ".")
    return valor


def extrair_telefone(texto: str) -> str:
    padrao = r"Telefone:\s*(\d{2}\s*\d{8,9})"
    match = re.search(padrao, texto)
    return match.group(1) if match else "---"

def extrair_valor(texto: str, marcador: str) -> str:
    """Função genérica para extrair valores após marcadores"""
    padrao = re.escape(marcador) + r"\s*([^\n]+)"
    match = re.search(padrao, texto)
    if match:
        valor = match.group(1).strip()
        # Limpeza básica para valores monetários
        if any(c.isdigit() for c in valor):
            return valor.split()[0].replace(".", "").replace(",", ".")
        return valor.split()[0] if valor.split() else "---"
    return "---"

def extrair_cidade(texto):
    match = re.search(r'Cidade:\s*(.*?)\s+UF:', texto, re.IGNORECASE)
    if match:
        return match.group(1).strip()
    return ""


def formatar_dinheiro(valor_str):
    try:
        # Remove R$ e espaços
        valor_limpo = valor_str.replace("R$", "").replace(" ", "")
        
        # Verifica se há vírgula ou ponto para determinar o separador decimal
        if "," in valor_limpo:
            # Remove pontos (separadores de milhar) e substitui vírgula por ponto
            partes = valor_limpo.split(",")
            parte_inteira = partes[0].replace(".", "")
            valor_limpo = f"{parte_inteira}.{partes[1]}"
        elif "." in valor_limpo:
            # Verifica se o ponto é separador decimal (último ponto)
            partes = valor_limpo.split(".")
            if len(partes) > 2:
                # Se há mais de um ponto, o último é decimal
                parte_inteira = "".join(partes[:-1])
                valor_limpo = f"{parte_inteira}.{partes[-1]}"
        
        valor_float = float(valor_limpo)
        
        # Formata: separador de milhar com ponto, decimal com vírgula
        valor_formatado = f"R$ {valor_float:,.2f}".replace(",", "v").replace(".", ",").replace("v", ".")
        return valor_formatado
    except (ValueError, AttributeError):
        return valor_str  # Retorna original se falhar


