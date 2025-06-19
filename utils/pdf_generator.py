from reportlab.lib.pagesizes import landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from datetime import datetime
import os


def build_complete_pdf(output_path, predim_data, verification_data, image_path, logos):
    custom_page_size = (2339, 1653)
    doc = SimpleDocTemplate(
        output_path,
        pagesize=custom_page_size,
        rightMargin=77,
        leftMargin=77,
        topMargin=77,
        bottomMargin=77
    )

    styles = getSampleStyleSheet()
    cell_style = ParagraphStyle(name="NormalCell", fontSize=20, leading=20)

    estructura_data = [
        [Paragraph("<b>Dimensiones (m)</b>", cell_style), ""],
        ["h", "3,40"],
        ["d", "0,60"],
        ["B", "2,96"],
        ["b₁", "0,86"],
        ["b₂min", "0,30"],
        ["b₂max", "0,47"],
        ["b₃", "1,63"],
        ["t", "0,48"],
        ["", ""],
        [Paragraph("<b>DISEÑO DE ZAPATA</b>", cell_style), ""],
        [Paragraph("<b>Talón</b>", cell_style), ""],
        ["1", "5/8'' @ 0,86m"],
        ["2", "5/8'' @ 0,86m"],
        [Paragraph("<b>Punta</b>", cell_style), ""],
        ["3", "5/8'' @ 0,38m"],
        ["4", "5/8'' @ 0,38m"],
        [Paragraph("<b>Temperatura</b>", cell_style), ""],
        ["5", "1/2'' @ 0,28m"],
        ["", ""],
        [Paragraph("<b>DISEÑO DEL VÁSTAGO</b>", cell_style), ""],
        [Paragraph("<b>Pantalla</b>", cell_style), ""],
        ["6", "5/8'' @ 0,36m"],
        ["7", "5/8'' @ 0,36m"],
        ["8", "5/8'' @ 0,36m"],
        [Paragraph("<b>Temperatura</b>", cell_style), ""],
        ["9", "1/2'' @ 0,30m"],
        ["10", "1/2'' @ 0,30m"]
    ]

    def draw_page_border(canvas, doc):
        canvas.saveState()
        canvas.setLineWidth(1)
        canvas.rect(doc.leftMargin - 5, doc.bottomMargin - 5,
                    doc.width + 10, doc.height + 10)
        canvas.restoreState()

    # Imagen superior
    if os.path.exists(image_path):
        img = Image(image_path, width=1368, height=685)
    else:
        img = Paragraph("IMAGEN NO DISPONIBLE", styles["Normal"])

    # Tabla de notas
    notas = [[Paragraph("<b>NOTAS</b>", cell_style)]] + [
        [Paragraph(f"• {nota}", cell_style)] for nota in predim_data["notas"]
    ]
    notas_table = Table(notas, colWidths=[683])
    notas_table.setStyle(TableStyle([
        ('BOX', (0, 0), (-1, -1), 1, colors.black),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 2),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
    ]))

    # Tabla de parámetros
    param_rows = [[Paragraph("<b>PARÁMETROS DE DISEÑO</b>", cell_style), ""]] + [
        [Paragraph(name, cell_style), str(value)]
        for name, value in predim_data["parametros"]
    ]
    param_table = Table(param_rows, colWidths=[390, 261])
    param_table.setStyle(TableStyle([
        ('BOX', (0, 0), (-1, -1), 1, colors.black),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('SPAN', (0, 0), (1, 0)),
    ]))

    # Tabla dimensiones y verificaciones
    # estructura_data = predim_data["estructura"]
    estructura_table = Table(estructura_data, colWidths=[307, 307])
    estructura_table.setStyle(TableStyle([
        ('BOX', (0, 0), (-1, -1), 1, colors.black),
        ('INNERGRID', (0, 1), (-1, -1), 0.25, colors.grey),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('SPAN', (0, 0), (1, 0)),
        ('SPAN', (0, 9), (1, 9)),
        ('SPAN', (0, 10), (1, 10)),
        ('SPAN', (0, 13), (1, 13)),
        ('SPAN', (0, 16), (1, 16)),
        ('SPAN', (0, 18), (1, 18)),
        ('SPAN', (0, 20), (1, 20)),
        ('SPAN', (0, 21), (1, 21)),
        ('SPAN', (0, 26), (1, 26)),
    ]))

    # Estructura general del layout
    izquierda = Table(
        [[img], [Table([[notas_table, param_table]])]], colWidths=[1462])
    derecha = estructura_table
    layout_table = Table([[izquierda, derecha]], colWidths=[1462, 724])
    layout_table.setStyle(TableStyle([('VALIGN', (0, 0), (-1, -1), 'TOP')]))

    # Footer
    fecha_footer = datetime.now().strftime("%B %Y").upper()
    footer_style = ParagraphStyle(
        name="FooterText", fontSize=20, alignment=1, leading=24)
    footer_data = [[
        Image(logos["logo_civil"], width=364, height=120),
        Image(logos["logo_ufpso"], width=420, height=100),
        Paragraph("CARTILLA DISEÑO DE MUROS DE CONTENCIÓN", footer_style),
        Paragraph("ING. DIEGO CHINCHILLA JÁCOME<br/>"
                  "ING. MAYELI VERGEL CARRASCAL<br/>"
                  "DIR. NELSON AFANADOR GARCIA<br/>"
                  "CODIR. JESUS RODRIGUEZ GUERRERO", footer_style),
        Paragraph("SIN ESCALA", footer_style),
        Paragraph(fecha_footer, footer_style),
        Paragraph("HOJA: 1/1", footer_style),
    ]]
    footer_col_widths = [364, 449, 276, 504, 195, 200, 200]
    footer_table = Table(
        footer_data, colWidths=footer_col_widths, rowHeights=120)
    footer_table.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "MIDDLE")]))

    # Ensamblar
    elements = [layout_table, Spacer(1, 12), footer_table]
    doc.build(elements, onFirstPage=draw_page_border)
