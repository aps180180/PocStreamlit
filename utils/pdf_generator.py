"""
Módulo para geração de relatórios em PDF
"""
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from datetime import datetime
from io import BytesIO
from config.empresa import (
    SISTEMA_NOME,
    SISTEMA_SUBTITULO,
    PDF_AUTOR,
    PDF_CRIADOR,
    PDF_PRODUTOR,
    PDF_ASSUNTO_CLIENTES,
    PDF_ASSUNTO_PRODUTOS
)

def adicionar_cabecalho_rodape_clientes(canvas, doc):
    """
    Adiciona cabeçalho e rodapé personalizados para relatório de clientes
    
    Args:
        canvas: Canvas do PDF
        doc: Documento PDF
    """
    canvas.saveState()
    
    # Configurações
    page_width = A4[0]
    page_height = A4[1]
    
    # ============ CABEÇALHO ============
    # Box colorido no topo
    canvas.setFillColorRGB(0.2, 0.47, 0.73)  # Azul #3498DB
    canvas.rect(0, page_height - 2.5*cm, page_width, 2.5*cm, fill=True, stroke=False)
    
    # Nome da empresa/sistema em branco
    canvas.setFillColorRGB(1, 1, 1)
    canvas.setFont('Helvetica-Bold', 20)
    canvas.drawString(2*cm, page_height - 1.5*cm, SISTEMA_NOME)
    
    # Subtítulo
    canvas.setFont('Helvetica', 10)
    canvas.drawString(2*cm, page_height - 2*cm, SISTEMA_SUBTITULO)
    
    # Data no canto direito do cabeçalho
    data_atual = datetime.now().strftime("%d/%m/%Y")
    canvas.setFont('Helvetica', 9)
    canvas.drawRightString(page_width - 2*cm, page_height - 1.8*cm, f"Data: {data_atual}")
    
    # ============ RODAPÉ ============
    # Linha horizontal no rodapé
    canvas.setStrokeColorRGB(0.8, 0.8, 0.8)
    canvas.setLineWidth(0.5)
    canvas.line(2*cm, 2*cm, page_width - 2*cm, 2*cm)
    
    # Texto do rodapé à esquerda
    canvas.setFillColorRGB(0.5, 0.5, 0.5)
    canvas.setFont('Helvetica', 8)
    texto_rodape = f"{SISTEMA_NOME} | {PDF_ASSUNTO_CLIENTES}"
    canvas.drawString(2*cm, 1.5*cm, texto_rodape)
    
    # Número da página no centro
    canvas.setFont('Helvetica-Bold', 9)
    pagina_texto = f"Página {doc.page}"
    text_width = canvas.stringWidth(pagina_texto, 'Helvetica-Bold', 9)
    canvas.drawString((page_width - text_width) / 2, 1.5*cm, pagina_texto)
    
    # Timestamp à direita
    canvas.setFont('Helvetica', 8)
    timestamp = datetime.now().strftime("%H:%M:%S")
    canvas.drawRightString(page_width - 2*cm, 1.5*cm, timestamp)
    
    canvas.restoreState()

def adicionar_cabecalho_rodape_produtos(canvas, doc):
    """
    Adiciona cabeçalho e rodapé personalizados para relatório de produtos
    
    Args:
        canvas: Canvas do PDF
        doc: Documento PDF
    """
    canvas.saveState()
    
    # Configurações
    page_width = A4[0]
    page_height = A4[1]
    
    # ============ CABEÇALHO ============
    # Box colorido no topo
    canvas.setFillColorRGB(0.15, 0.68, 0.38)  # Verde #27AE60
    canvas.rect(0, page_height - 2.5*cm, page_width, 2.5*cm, fill=True, stroke=False)
    
    # Nome da empresa/sistema em branco
    canvas.setFillColorRGB(1, 1, 1)
    canvas.setFont('Helvetica-Bold', 20)
    canvas.drawString(2*cm, page_height - 1.5*cm, SISTEMA_NOME)
    
    # Subtítulo
    canvas.setFont('Helvetica', 10)
    canvas.drawString(2*cm, page_height - 2*cm, SISTEMA_SUBTITULO)
    
    # Data no canto direito do cabeçalho
    data_atual = datetime.now().strftime("%d/%m/%Y")
    canvas.setFont('Helvetica', 9)
    canvas.drawRightString(page_width - 2*cm, page_height - 1.8*cm, f"Data: {data_atual}")
    
    # ============ RODAPÉ ============
    # Linha horizontal no rodapé
    canvas.setStrokeColorRGB(0.8, 0.8, 0.8)
    canvas.setLineWidth(0.5)
    canvas.line(2*cm, 2*cm, page_width - 2*cm, 2*cm)
    
    # Texto do rodapé à esquerda
    canvas.setFillColorRGB(0.5, 0.5, 0.5)
    canvas.setFont('Helvetica', 8)
    texto_rodape = f"{SISTEMA_NOME} | {PDF_ASSUNTO_PRODUTOS}"
    canvas.drawString(2*cm, 1.5*cm, texto_rodape)
    
    # Número da página no centro
    canvas.setFont('Helvetica-Bold', 9)
    pagina_texto = f"Página {doc.page}"
    text_width = canvas.stringWidth(pagina_texto, 'Helvetica-Bold', 9)
    canvas.drawString((page_width - text_width) / 2, 1.5*cm, pagina_texto)
    
    # Timestamp à direita
    canvas.setFont('Helvetica', 8)
    timestamp = datetime.now().strftime("%H:%M:%S")
    canvas.drawRightString(page_width - 2*cm, 1.5*cm, timestamp)
    
    canvas.restoreState()

def gerar_relatorio_clientes_pdf(clientes, filtros=None):
    """
    Gera relatório de clientes em PDF com cabeçalho e rodapé profissionais
    
    Args:
        clientes: Lista de tuplas (id, nome, email)
        filtros: Dict com informações de filtros aplicados
        
    Returns:
        BytesIO com conteúdo do PDF
    """
    buffer = BytesIO()
    
    # Criar documento com margens ajustadas e metadados
    doc = SimpleDocTemplate(
        buffer, 
        pagesize=A4,
        leftMargin=2*cm,
        rightMargin=2*cm,
        topMargin=3.5*cm,
        bottomMargin=3*cm,
        title=PDF_ASSUNTO_CLIENTES,
        author=PDF_AUTOR,
        creator=PDF_CRIADOR,
        producer=PDF_PRODUTOR,
        subject=PDF_ASSUNTO_CLIENTES
    )
    
    elements = []
    styles = getSampleStyleSheet()
    
    # Estilo para título do relatório
    titulo_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=16,
        textColor=colors.HexColor('#2C3E50'),
        spaceAfter=10,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    # Estilo para subtítulo
    subtitulo_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Normal'],
        fontSize=9,
        textColor=colors.HexColor('#7F8C8D'),
        spaceAfter=15,
        alignment=TA_CENTER
    )
    
    # Título do relatório
    elements.append(Paragraph("RELATÓRIO DE CLIENTES", titulo_style))
    
    # Data e hora de geração
    data_hora = datetime.now().strftime("%d/%m/%Y às %H:%M:%S")
    elements.append(Paragraph(f"Gerado em: {data_hora}", subtitulo_style))
    
    # Informações de filtros
    if filtros:
        filtros_style = ParagraphStyle(
            'Filtros',
            parent=styles['Normal'],
            fontSize=8,
            textColor=colors.HexColor('#34495E'),
            spaceAfter=15,
            alignment=TA_LEFT,
            leftIndent=10,
            rightIndent=10
        )
        elements.append(Paragraph(f"<b>Filtros aplicados:</b> {filtros}", filtros_style))
    
    elements.append(Spacer(1, 5))
    
    # Box com informações resumidas
    info_box_data = [[
        Paragraph(f"<b>Total de Clientes:</b> {len(clientes)}", styles['Normal']),
        Paragraph(f"<b>Status:</b> Ativo", styles['Normal'])
    ]]
    
    info_table = Table(info_box_data, colWidths=[9*cm, 9*cm])
    info_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#EBF5FB')),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#3498DB')),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
    ]))
    elements.append(info_table)
    elements.append(Spacer(1, 15))
    
    # Criar tabela de dados
    data = [['Código', 'Nome Completo', 'E-mail']]
    
    for cliente in clientes:
        data.append([
            str(cliente[0]),
            str(cliente[1]),
            str(cliente[2])
        ])
    
    # Criar e estilizar tabela
    table = Table(data, colWidths=[2.5*cm, 7.5*cm, 8*cm])
    table.setStyle(TableStyle([
        # Estilo do cabeçalho
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498DB')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('TOPPADDING', (0, 0), (-1, 0), 12),
        
        # Estilo do corpo
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        ('ALIGN', (0, 1), (0, -1), 'CENTER'),
        ('ALIGN', (1, 1), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#BDC3C7')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F8F9FA')]),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 1), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
    ]))
    
    elements.append(table)
    
    # Construir PDF
    doc.build(elements, onFirstPage=adicionar_cabecalho_rodape_clientes, onLaterPages=adicionar_cabecalho_rodape_clientes)
    buffer.seek(0)
    return buffer

def gerar_relatorio_produtos_pdf(produtos, filtros=None):
    """
    Gera relatório de produtos em PDF com cabeçalho e rodapé profissionais
    
    Args:
        produtos: Lista de tuplas (id, nome, preco)
        filtros: Dict com informações de filtros aplicados
        
    Returns:
        BytesIO com conteúdo do PDF
    """
    buffer = BytesIO()
    
    # Criar documento com metadados
    doc = SimpleDocTemplate(
        buffer, 
        pagesize=A4,
        leftMargin=2*cm,
        rightMargin=2*cm,
        topMargin=3.5*cm,
        bottomMargin=3*cm,
        title=PDF_ASSUNTO_PRODUTOS,
        author=PDF_AUTOR,
        creator=PDF_CRIADOR,
        producer=PDF_PRODUTOR,
        subject=PDF_ASSUNTO_PRODUTOS
    )
    
    elements = []
    styles = getSampleStyleSheet()
    
    # Estilo para título do relatório
    titulo_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=16,
        textColor=colors.HexColor('#27AE60'),
        spaceAfter=10,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    # Estilo para subtítulo
    subtitulo_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Normal'],
        fontSize=9,
        textColor=colors.HexColor('#7F8C8D'),
        spaceAfter=15,
        alignment=TA_CENTER
    )
    
    # Título do relatório
    elements.append(Paragraph("RELATÓRIO DE PRODUTOS", titulo_style))
    
    # Data e hora de geração
    data_hora = datetime.now().strftime("%d/%m/%Y às %H:%M:%S")
    elements.append(Paragraph(f"Gerado em: {data_hora}", subtitulo_style))
    
    # Informações de filtros
    if filtros:
        filtros_style = ParagraphStyle(
            'Filtros',
            parent=styles['Normal'],
            fontSize=8,
            textColor=colors.HexColor('#34495E'),
            spaceAfter=15,
            alignment=TA_LEFT,
            leftIndent=10,
            rightIndent=10
        )
        elements.append(Paragraph(f"<b>Filtros aplicados:</b> {filtros}", filtros_style))
    
    elements.append(Spacer(1, 5))
    
    # Calcular totais
    total_produtos = len(produtos)
    valor_total = sum([float(p[2]) for p in produtos]) if produtos else 0
    
    # Box com informações resumidas
    info_box_data = [[
        Paragraph(f"<b>Total de Produtos:</b> {total_produtos}", styles['Normal']),
        Paragraph(f"<b>Valor Total:</b> R$ {valor_total:,.2f}", styles['Normal'])
    ]]
    
    info_table = Table(info_box_data, colWidths=[9*cm, 9*cm])
    info_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#E8F8F5')),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#27AE60')),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
    ]))
    elements.append(info_table)
    elements.append(Spacer(1, 15))
    
    # Criar tabela de dados
    data = [['Código', 'Nome do Produto', 'Preço Unitário']]
    
    for produto in produtos:
        data.append([
            str(produto[0]),
            str(produto[1]),
            f"R$ {float(produto[2]):,.2f}"
        ])
    
    # Criar e estilizar tabela
    table = Table(data, colWidths=[2.5*cm, 10.5*cm, 5*cm])
    table.setStyle(TableStyle([
        # Estilo do cabeçalho
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#27AE60')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('TOPPADDING', (0, 0), (-1, 0), 12),
        
        # Estilo do corpo
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        ('ALIGN', (0, 1), (0, -1), 'CENTER'),
        ('ALIGN', (1, 1), (1, -1), 'LEFT'),
        ('ALIGN', (2, 1), (2, -1), 'RIGHT'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#BDC3C7')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F8F9FA')]),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 1), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
    ]))
    
    elements.append(table)
    
    # Construir PDF
    doc.build(elements, onFirstPage=adicionar_cabecalho_rodape_produtos, onLaterPages=adicionar_cabecalho_rodape_produtos)
    buffer.seek(0)
    return buffer
