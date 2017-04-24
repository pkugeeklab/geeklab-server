from io import BytesIO

from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfbase import pdfmetrics, ttfonts
from reportlab.platypus import Paragraph, Table, TableStyle

pdfmetrics.registerFont(ttfonts.TTFont('simsun', 'pdfs/simsun.ttf'))
styles = getSampleStyleSheet()
styleN = styles['BodyText']
styleN.fontName = 'simsun'
styleN.fontSize = 12
styleN.wordWrap = 'CJK'
styleT = TableStyle([('VALIGN', (0, 0), (0, 0), 'MIDDLE')])


def drawString(can, data):
    can.drawString(170, 688, data['username'])
    can.drawString(440, 688, data['contact'])
    can.drawString(170, 654, data['title'])
    can.drawString(440, 654, data['people'])
    can.drawString(170, 592, data['principal'])
    can.drawString(335, 592, data['contactplus'])
    table_desc = Table([[Paragraph(data['desc'], styleN)]],
                       colWidths=340, rowHeights=140)
    table_desc.setStyle(styleT),
    table_desc.wrapOn(can, 0, 0)
    table_desc.drawOn(can, 170, 435)
    table_add = Table([[Paragraph(data['additional'], styleN)]],
                      colWidths=340, rowHeights=42)
    table_add.setStyle(styleT)
    table_add.wrapOn(can, 0, 0)
    table_add.drawOn(can, 170, 330)
    start_time = data['starttime']
    can.drawString(190, 624, start_time[0])
    can.drawString(228, 624, start_time[1])
    can.drawString(252, 624, start_time[2])
    can.drawString(276, 624, start_time[3])
    can.drawString(300, 624, start_time[4])
    stop_time = data['stoptime']
    can.drawString(352, 624, stop_time[0])
    can.drawString(390, 624, stop_time[1])
    can.drawString(414, 624, stop_time[2])
    can.drawString(438, 624, stop_time[3])
    can.drawString(462, 624, stop_time[4])
    pos = {'exp': (180, 408),
           'speech': (180, 393),
           'desk': (180, 378),
           'projector': (353, 408),
           'board': (353, 393),
           'tv': (353, 378)}
    for k, p in pos.items():
        if k in data['item']:
            can.drawString(p[0], p[1], '█')
