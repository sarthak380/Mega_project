from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4

def generate_report(history):

    styles = getSampleStyleSheet()

    elements = []

    elements.append(
        Paragraph("Chatbot Testing Report",styles["Title"])
    )

    elements.append(Spacer(1,20))

    data=[["Turn","User","Bot"]]

    for i,(u,b) in enumerate(history):

        data.append([str(i+1),u,b])

    table=Table(data)

    elements.append(table)

    doc=SimpleDocTemplate(
        "chatbot_report.pdf",
        pagesize=A4
    )

    doc.build(elements)

    return "chatbot_report.pdf"