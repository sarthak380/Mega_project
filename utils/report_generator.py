from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from datetime import datetime

def generate_report(history, persona_name="Unknown", bot_type="Unknown", metrics=None, evaluation_results=None, conclusion=None):
    """
    Generate a well-formatted PDF report for chatbot testing
    """

    # Create filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"chatbot_report_{persona_name.lower().replace(' ', '_')}_{timestamp}.pdf"

    # Initialize document
    doc = SimpleDocTemplate(
        filename,
        pagesize=A4,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=72
    )

    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Title'],
        fontSize=24,
        spaceAfter=30,
        alignment=1,  # Center alignment
        textColor=colors.darkblue
    )

    subtitle_style = ParagraphStyle(
        'Subtitle',
        parent=styles['Heading2'],
        fontSize=14,
        spaceAfter=20,
        textColor=colors.darkgreen
    )

    normal_style = ParagraphStyle(
        'Normal',
        parent=styles['Normal'],
        fontSize=10,
        spaceAfter=10
    )

    elements = []

    # Title
    elements.append(Paragraph("🤖 AI Chatbot Testing Report", title_style))
    elements.append(Spacer(1, 20))

    # Report metadata
    metadata = [
        ["Report Generated:", datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
        ["Bot Type:", bot_type],
        ["Persona:", persona_name],
        ["Total Turns:", str(len(history))],
        ["Test Duration:", "Multi-turn conversation simulation"]
    ]

    if metrics:
        metadata.append(["PAS:", f"{metrics.get('PAS', 0)}%"])
        metadata.append(["BVS:", f"{metrics.get('BVS', 0)}%"])
        metadata.append(["TRA:", f"{metrics.get('TRA', 0)}%"])
        metadata.append(["DEI:", f"{metrics.get('DEI', 0)}%"])
        metadata.append(["CRRS:", f"{metrics.get('CRRS', 0)}%"])

    # Metadata table
    metadata_table = Table(metadata, colWidths=[2*inch, 4*inch])
    metadata_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
        ('TEXTCOLOR', (0, 0), (0, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))

    elements.append(metadata_table)
    elements.append(Spacer(1, 30))

    if evaluation_results:
        elements.append(Paragraph("🧾 Persona Evaluation Summary", subtitle_style))
        elements.append(Spacer(1, 15))

        summary_data = [["Persona", "PAS", "BVS", "TRA", "DEI", "CRRS"]]
        for result in evaluation_results:
            metrics = result["metrics"]
            summary_data.append([
                result["persona"],
                f"{metrics['PAS']}%",
                f"{metrics['BVS']}%",
                f"{metrics['TRA']}%",
                f"{metrics['DEI']}%",
                f"{metrics['CRRS']}%"
            ])

        summary_table = Table(summary_data, colWidths=[2.2*inch, 0.8*inch, 0.8*inch, 0.8*inch, 0.8*inch, 0.8*inch])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ]))
        elements.append(summary_table)
        elements.append(Spacer(1, 30))

        if conclusion:
            elements.append(Paragraph("📌 Final Conclusion", subtitle_style))
            elements.append(Paragraph(conclusion, normal_style))
            elements.append(Spacer(1, 20))

    else:
        # Conversation section header
        elements.append(Paragraph("📝 Conversation Transcript", subtitle_style))
        elements.append(Spacer(1, 15))

        if history:
            # Table headers
            data = [["Turn", "Restaurant Message", "Customer Response"]]

            # Add conversation data
            for i, (restaurant_msg, customer_response) in enumerate(history, 1):
                # Truncate long messages for better display
                restaurant_truncated = restaurant_msg[:100] + "..." if len(restaurant_msg) > 100 else restaurant_msg
                customer_truncated = customer_response[:100] + "..." if len(customer_response) > 100 else customer_response

                data.append([
                    str(i),
                    Paragraph(restaurant_truncated, normal_style),
                    Paragraph(customer_truncated, normal_style)
                ])

            # Create table with proper column widths
            col_widths = [0.5*inch, 2.5*inch, 2.5*inch]
            conversation_table = Table(data, colWidths=col_widths, repeatRows=1)

            # Table styling
            table_style = TableStyle([
                # Header styling
                ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
                ('TOPPADDING', (0, 0), (-1, 0), 8),

                # Data row styling
                ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
                ('ALIGN', (0, 1), (0, -1), 'CENTER'),
                ('ALIGN', (1, 1), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 1), (-1, -1), 9),
                ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
                ('TOPPADDING', (0, 1), (-1, -1), 6),

                # Grid lines
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                ('LINEBELOW', (0, 0), (-1, 0), 2, colors.black),
            ])

            if len(data) > 2:
                for row_index in range(1, len(data), 2):
                    if row_index < len(data):
                        table_style.add('BACKGROUND', (0, row_index), (-1, row_index), colors.lightgrey)

            conversation_table.setStyle(table_style)
            elements.append(conversation_table)
        else:
            elements.append(Paragraph("No conversation data available.", normal_style))

    elements.append(Spacer(1, 30))

    # Footer
    footer_style = ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontSize=8,
        textColor=colors.grey,
        alignment=1  # Center
    )
    elements.append(Paragraph("Generated by Multi-Agent Persona Control System", footer_style))

    # Build PDF
    doc.build(elements)

    return filename