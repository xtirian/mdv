from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from datetime import datetime
import tkinter as tk
from tkinter import filedialog
from core.app_state import APP_STATE

def export_to_pdf():
    try:
        if not APP_STATE.get("dados_extraidos"):
            return {"success": False, "message": "Nenhum dado disponível para exportação"}

        ordem_colunas = APP_STATE.get("ordem_colunas", [])
        todos_dados = []

        for doc_id, dados_list in APP_STATE["dados_extraidos"].items():
            if dados_list:
                todos_dados.extend(dados_list)

        if not todos_dados:
            return {"success": False, "message": "Nenhum dado válido encontrado"}

        # Monta os dados em formato de tabela
        headers = [col for col in ordem_colunas if col in todos_dados[0]]
        table_data = [headers]  # cabeçalho
        for item in todos_dados:
            row = [item.get(col, "") for col in headers]
            table_data.append(row)

        # Cria janela para salvar
        root = tk.Tk()
        root.withdraw()

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        default_filename = f"consorcios_exportados_{timestamp}.pdf"

        filepath = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("Arquivos PDF", "*.pdf"), ("Todos os arquivos", "*.*")],
            initialfile=default_filename,
            title="Salvar arquivo PDF como..."
        )

        if not filepath:
            return {"success": False, "message": "Exportação cancelada pelo usuário"}

        # Criar documento PDF
        doc = SimpleDocTemplate(filepath, pagesize=landscape(A4), rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=20)
        styles = getSampleStyleSheet()
        elementos = []

        # Título
        titulo = Paragraph("Relatório de Consórcios Exportado", styles["Title"])
        elementos.append(titulo)
        elementos.append(Spacer(1, 12))

        # Tabela
        tabela = Table(table_data, repeatRows=1)
        tabela.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#CC092F")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 8),
            ("BOTTOMPADDING", (0, 0), (-1, 0), 6),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.whitesmoke, colors.lightgrey]),
        ]))

        elementos.append(tabela)
        doc.build(elementos)

        return {
            "success": True,
            "message": f"PDF salvo com sucesso em:\n{filepath}",
            "filepath": filepath
        }

    except Exception as e:
        return {
            "success": False,
            "message": f"Erro durante exportação para PDF: {str(e)}"
        }
