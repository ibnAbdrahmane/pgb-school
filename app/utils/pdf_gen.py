from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.pdfgen import canvas
import os
from flask import current_app
from app.models.models import Eleve, Note, Cours, Bulletin, Classe
from app import db
from datetime import datetime


def generate_carte_identite(eleve):
    upload_folder = current_app.config['UPLOAD_FOLDER']
    path = os.path.join(upload_folder, 'cartes', f'carte_{eleve.id}.pdf')

    c = canvas.Canvas(path, pagesize=(9.5 * cm, 6 * cm))
    w, h = 9.5 * cm, 6 * cm

    # Background gradient effect
    c.setFillColorRGB(0.06, 0.09, 0.18)
    c.rect(0, 0, w, h, fill=1, stroke=0)

    # Accent stripe
    c.setFillColorRGB(0.2, 0.6, 1.0)
    c.rect(0, h - 0.8 * cm, w, 0.8 * cm, fill=1, stroke=0)

    # School name
    c.setFillColorRGB(1, 1, 1)
    c.setFont("Helvetica-Bold", 10)
    c.drawCentredString(w / 2, h - 0.55 * cm, "ÉCOLE PGB")

    # Photo placeholder
    photo_x, photo_y = 0.3 * cm, 1.8 * cm
    if eleve.photo:
        photo_path = os.path.join(upload_folder, eleve.photo)
        if os.path.exists(photo_path):
            try:
                c.drawImage(photo_path, photo_x, photo_y, width=2 * cm, height=2.5 * cm,
                            preserveAspectRatio=True, mask='auto')
            except Exception:
                _draw_photo_placeholder(c, photo_x, photo_y)
        else:
            _draw_photo_placeholder(c, photo_x, photo_y)
    else:
        _draw_photo_placeholder(c, photo_x, photo_y)

    # Info text
    c.setFillColorRGB(0.8, 0.9, 1.0)
    c.setFont("Helvetica-Bold", 7.5)
    c.drawString(2.8 * cm, h - 1.3 * cm, f"{eleve.user.last_name.upper()} {eleve.user.first_name}")

    c.setFont("Helvetica", 6.5)
    c.setFillColorRGB(0.7, 0.8, 0.9)

    info_lines = [
        f"Matricule: {eleve.matricule}",
        f"Classe: {eleve.classe.nom if eleve.classe else 'N/A'}",
        f"Né(e): {eleve.date_naissance.strftime('%d/%m/%Y') if eleve.date_naissance else 'N/A'}",
        f"Carte N°: {eleve.numero_carte}",
    ]
    y_pos = h - 1.9 * cm
    for line in info_lines:
        c.drawString(2.8 * cm, y_pos, line)
        y_pos -= 0.45 * cm

    # Footer
    c.setFillColorRGB(0.4, 0.5, 0.6)
    c.setFont("Helvetica", 5)
    c.drawCentredString(w / 2, 0.25 * cm, f"Année scolaire 2024-2025 | Valable jusqu'au 30/06/2025")

    # Border
    c.setStrokeColorRGB(0.2, 0.6, 1.0)
    c.setLineWidth(1.5)
    c.rect(0.1 * cm, 0.1 * cm, w - 0.2 * cm, h - 0.2 * cm, fill=0)

    c.save()
    return path


def _draw_photo_placeholder(c, x, y):
    c.setFillColorRGB(0.2, 0.3, 0.5)
    c.rect(x, y, 2 * cm, 2.5 * cm, fill=1, stroke=0)
    c.setFillColorRGB(0.5, 0.6, 0.7)
    c.setFont("Helvetica", 5)
    c.drawCentredString(x + 1 * cm, y + 1.2 * cm, "PHOTO")


def generate_bulletin(eleve_id, trimestre):
    upload_folder = current_app.config['UPLOAD_FOLDER']
    eleve = Eleve.query.get(eleve_id)
    if not eleve:
        return None

    notes_list = Note.query.filter_by(eleve_id=eleve_id, trimestre=trimestre).all()
    if not notes_list:
        return None

    # Calculate moyenne
    total_points = sum(n.valeur * n.cours.coefficient for n in notes_list if n.valeur is not None)
    total_coeff = sum(n.cours.coefficient for n in notes_list if n.valeur is not None)
    moyenne = round(total_points / total_coeff, 2) if total_coeff > 0 else 0

    mention = _get_mention(moyenne)

    # Calculate rang
    all_eleves_moyennes = []
    if eleve.classe:
        for e in eleve.classe.eleves:
            e_notes = Note.query.filter_by(eleve_id=e.id, trimestre=trimestre).all()
            if e_notes:
                tp = sum(n.valeur * n.cours.coefficient for n in e_notes if n.valeur is not None)
                tc = sum(n.cours.coefficient for n in e_notes if n.valeur is not None)
                m = tp / tc if tc > 0 else 0
                all_eleves_moyennes.append((e.id, m))
    all_eleves_moyennes.sort(key=lambda x: x[1], reverse=True)
    rang = next((i + 1 for i, (eid, _) in enumerate(all_eleves_moyennes) if eid == eleve_id), 1)

    filename = f"bulletin_{eleve_id}_T{trimestre}.pdf"
    filepath = os.path.join(upload_folder, 'bulletins', filename)

    _build_bulletin_pdf(filepath, eleve, notes_list, moyenne, rang, mention, trimestre)

    existing = Bulletin.query.filter_by(eleve_id=eleve_id, trimestre=trimestre).first()
    if existing:
        existing.moyenne_generale = moyenne
        existing.rang = rang
        existing.mention = mention
        existing.pdf_path = f"bulletins/{filename}"
    else:
        bulletin = Bulletin(
            eleve_id=eleve_id, trimestre=trimestre,
            annee_scolaire='2024-2025',
            moyenne_generale=moyenne, rang=rang,
            mention=mention, pdf_path=f"bulletins/{filename}"
        )
        db.session.add(bulletin)
    db.session.commit()
    return filepath


def _build_bulletin_pdf(filepath, eleve, notes_list, moyenne, rang, mention, trimestre):
    doc = SimpleDocTemplate(filepath, pagesize=A4,
                            rightMargin=1.5 * cm, leftMargin=1.5 * cm,
                            topMargin=1.5 * cm, bottomMargin=1.5 * cm)
    styles = getSampleStyleSheet()
    story = []

    # Header
    title_style = ParagraphStyle('title', fontSize=18, fontName='Helvetica-Bold',
                                  alignment=TA_CENTER, textColor=colors.HexColor('#0d1b2a'),
                                  spaceAfter=4)
    sub_style = ParagraphStyle('sub', fontSize=10, alignment=TA_CENTER,
                                textColor=colors.HexColor('#2563eb'), spaceAfter=12)

    story.append(Paragraph("ÉCOLE PGB", title_style))
    story.append(Paragraph(f"Bulletin de notes — Trimestre {trimestre} | 2024-2025", sub_style))

    # Student info table
    info_data = [
        ['Nom & Prénom', f"{eleve.user.last_name.upper()} {eleve.user.first_name}",
         'Matricule', eleve.matricule],
        ['Classe', eleve.classe.nom if eleve.classe else 'N/A',
         'Année scolaire', '2024-2025'],
    ]
    info_table = Table(info_data, colWidths=[4 * cm, 7 * cm, 3.5 * cm, 4 * cm])
    info_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#e8f0fe')),
        ('BACKGROUND', (2, 0), (2, -1), colors.HexColor('#e8f0fe')),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (2, 0), (2, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('ROWBACKGROUNDS', (0, 0), (-1, -1), [colors.white, colors.HexColor('#f8fafc')]),
        ('PADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(info_table)
    story.append(Spacer(1, 0.4 * cm))

    # Notes table
    notes_header = [['Matière', 'Coeff.', 'Note /20', 'Points', 'Appréciation']]
    notes_data = notes_header
    for note in notes_list:
        if note.valeur is not None:
            appre = _get_appreciation(note.valeur)
            points = round(note.valeur * note.cours.coefficient, 2)
            notes_data.append([
                note.cours.nom,
                str(note.cours.coefficient),
                f"{note.valeur:.2f}",
                f"{points:.2f}",
                appre
            ])

    notes_table = Table(notes_data, colWidths=[7 * cm, 2.5 * cm, 3 * cm, 3 * cm, 4 * cm])
    notes_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0d1b2a')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e2e8f0')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8fafc')]),
        ('PADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(notes_table)
    story.append(Spacer(1, 0.4 * cm))

    # Summary
    summary_data = [
        ['Moyenne générale', f"{moyenne:.2f}/20", 'Mention', mention, 'Rang', f"{rang}e"],
    ]
    summary_table = Table(summary_data, colWidths=[4 * cm, 3 * cm, 2.5 * cm, 3.5 * cm, 2 * cm, 4.5 * cm])
    bg = _mention_color(mention)
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor(bg)),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('PADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.white),
    ]))
    story.append(summary_table)
    story.append(Spacer(1, 1 * cm))

    # Signatures
    sig_data = [['Signature du Directeur', '', 'Cachet de l\'école', '', 'Signature du Parent']]
    sig_table = Table(sig_data, colWidths=[5 * cm, 1 * cm, 5 * cm, 1 * cm, 5 * cm])
    sig_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('TOPPADDING', (0, 0), (-1, -1), 30),
        ('LINEBELOW', (0, 0), (0, 0), 1, colors.grey),
        ('LINEBELOW', (2, 0), (2, 0), 1, colors.grey),
        ('LINEBELOW', (4, 0), (4, 0), 1, colors.grey),
    ]))
    story.append(sig_table)

    doc.build(story)


def _get_mention(moyenne):
    if moyenne >= 16:
        return "Très Bien"
    elif moyenne >= 14:
        return "Bien"
    elif moyenne >= 12:
        return "Assez Bien"
    elif moyenne >= 10:
        return "Passable"
    else:
        return "Insuffisant"


def _get_appreciation(note):
    if note >= 16:
        return "Excellent"
    elif note >= 14:
        return "Très bien"
    elif note >= 12:
        return "Bien"
    elif note >= 10:
        return "Passable"
    else:
        return "Insuffisant"


def _mention_color(mention):
    colors_map = {
        "Très Bien": "#dcfce7",
        "Bien": "#d1fae5",
        "Assez Bien": "#fef9c3",
        "Passable": "#fff7ed",
        "Insuffisant": "#fee2e2",
    }
    return colors_map.get(mention, "#f8fafc")
