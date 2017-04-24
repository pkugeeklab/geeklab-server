from io import BytesIO

from PyPDF2 import PdfFileReader, PdfFileWriter
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfbase import pdfmetrics, ttfonts
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph, Table, TableStyle

import pdfs.genActivity as genActivity
pdfmetrics.registerFont(ttfonts.TTFont('simsun', 'pdfs/simsun.ttf'))
styles = getSampleStyleSheet()
styleN = styles['BodyText']
styleN.fontName = 'simsun'
styleN.fontSize = 12
styleN.wordWrap = 'CJK'
styleT = TableStyle([('VALIGN', (0, 0), (0, 0), 'MIDDLE')])


def addInfo(table_type, data):
    packet = BytesIO()
    can = canvas.Canvas(packet, pagesize=A4)
    can.setFont('simsun', 12)
    if table_type == 'device':
        can.drawString(10, 100, "Hello world")
    elif table_type == 'activity':
        genActivity.drawString(can, data)
    can.save()

    packet.seek(0)
    new_pdf = PdfFileReader(packet)
    existing_pdf = PdfFileReader(open("pdfs/activity.pdf", "rb"))
    output = PdfFileWriter()
    page = existing_pdf.getPage(0)
    page.mergePage(new_pdf.getPage(0))
    output.addPage(page)
    outputStream = BytesIO()
    output.write(outputStream)
    outputStream.seek(0)
    return outputStream
