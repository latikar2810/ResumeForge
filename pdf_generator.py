from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet


def generate_pdf(
    filename,
    ats_score,
    resume_rating,
    matched_skills,
    missing_skills,
    suggestions
):

    doc = SimpleDocTemplate(filename)
    styles = getSampleStyleSheet()

    story = []

    story.append(Paragraph("<b>AI Resume Analyzer Report</b>", styles["Title"]))
    story.append(Paragraph(f"<b>ATS Score:</b> {ats_score}%", styles["Normal"]))
    story.append(Paragraph(f"<b>Resume Rating:</b> {resume_rating}", styles["Normal"]))
    story.append(Paragraph("<br/>", styles["Normal"]))

    story.append(Paragraph("<b>Matched Skills</b>", styles["Heading2"]))

    if matched_skills:
        for skill in matched_skills:
            story.append(Paragraph(f"• {skill}", styles["Normal"]))
    else:
        story.append(Paragraph("No matched skills found.", styles["Normal"]))

    story.append(Paragraph("<br/>", styles["Normal"]))
    story.append(Paragraph("<b>Missing Skills</b>", styles["Heading2"]))

    if missing_skills:
        for skill in missing_skills:
            story.append(Paragraph(f"• {skill}", styles["Normal"]))
    else:
        story.append(Paragraph("No missing skills.", styles["Normal"]))

    story.append(Paragraph("<br/>", styles["Normal"]))
    story.append(Paragraph("<b>Suggestions</b>", styles["Heading2"]))

    for suggestion in suggestions:
        story.append(Paragraph(f"• {suggestion}", styles["Normal"]))

    doc.build(story)