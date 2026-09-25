import io
from datetime import date
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session, joinedload
from app.database import get_db
from app.models.application import Application
from app.models.challenge import Challenge
from app.models.startup import Startup
from app.models.user import User
from app.auth import require_role

router = APIRouter(prefix="/applications", tags=["Procurement"])

@router.get("/{application_id}/procurement-order/pdf")
def generate_procurement_order(
    application_id: int,
    current_user: User = Depends(require_role("officer")),
    db: Session = Depends(get_db)
):
    """Generate a GFR Rule 149/194 compliant Procurement Order PDF."""
    app_obj = db.query(Application).options(
        joinedload(Application.startup),
        joinedload(Application.challenge)
    ).filter(Application.id == application_id).first()

    if not app_obj:
        raise HTTPException(status_code=404, detail="Application not found")
    if app_obj.status != "shortlisted":
        raise HTTPException(status_code=400, detail="Procurement orders can only be generated for shortlisted applications.")

    startup = app_obj.startup
    challenge = app_obj.challenge

    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import cm
        from reportlab.lib import colors
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable

        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4, topMargin=2*cm, bottomMargin=2*cm, leftMargin=2.5*cm, rightMargin=2.5*cm)
        styles = getSampleStyleSheet()
        story = []

        title_style = ParagraphStyle("title", parent=styles["Heading1"], fontSize=14, spaceAfter=4, alignment=1)
        sub_style = ParagraphStyle("sub", parent=styles["Normal"], fontSize=10, spaceAfter=2, alignment=1)
        label_style = ParagraphStyle("label", parent=styles["Normal"], fontSize=9, textColor=colors.grey)
        value_style = ParagraphStyle("value", parent=styles["Normal"], fontSize=10, spaceAfter=6)

        story.append(Paragraph("GOVERNMENT OF MAHARASHTRA", title_style))
        story.append(Paragraph("Startup Procurement Order", title_style))
        story.append(Paragraph("(In compliance with GFR Rule 149 / 194 - Startup Procurement)", sub_style))
        story.append(Spacer(1, 0.4*cm))
        story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#FF6600")))
        story.append(Spacer(1, 0.4*cm))

        # Reference number and date
        ref_year = date.today().year
        ref_id = f"PO/{ref_year}/{app_obj.id:05d}"
        story.append(Paragraph(f"Reference No: {ref_id}  |  Date: {date.today().strftime('%d %B %Y')}", value_style))
        story.append(Spacer(1, 0.3*cm))

        # Challenge / Procurement Details
        challenge_data = [
            ["Challenge Title", challenge.title if challenge else "N/A"],
            ["Budget Band", challenge.budget_band if challenge else "N/A"],
            ["Required Sector", challenge.required_sector if challenge else "N/A"],
            ["Application Reference", f"APP-{ref_year}-{app_obj.id:05d}"],
            ["Application Status", app_obj.status.upper()],
        ]
        t = Table(challenge_data, colWidths=[5*cm, 11*cm])
        t.setStyle(TableStyle([
            ("BACKGROUND", (0,0), (0,-1), colors.HexColor("#FFF3E0")),
            ("FONTNAME", (0,0), (0,-1), "Helvetica-Bold"),
            ("FONTSIZE", (0,0), (-1,-1), 9),
            ("GRID", (0,0), (-1,-1), 0.5, colors.grey),
            ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
            ("ROWBACKGROUNDS", (0,0), (-1,-1), [colors.whitesmoke, colors.white]),
        ]))
        story.append(Paragraph("Section 1: Procurement Details", styles["Heading3"]))
        story.append(t)
        story.append(Spacer(1, 0.4*cm))

        # Startup Details
        startup_data = [
            ["Startup Name", startup.name if startup else "N/A"],
            ["Sector", startup.sector if startup else "N/A"],
            ["DPIIT Recognized", "Yes" if startup and startup.dpiit_status else "No"],
            ["MSME Reg. No.", getattr(startup, "msme_reg_no", None) or "Not Provided"],
            ["Women-Led", "Yes" if getattr(startup, "women_led", False) else "No"],
            ["Make in India Class", getattr(startup, "make_in_india_class", None) or "Not Specified"],
        ]
        t2 = Table(startup_data, colWidths=[5*cm, 11*cm])
        t2.setStyle(TableStyle([
            ("BACKGROUND", (0,0), (0,-1), colors.HexColor("#E8F5E9")),
            ("FONTNAME", (0,0), (0,-1), "Helvetica-Bold"),
            ("FONTSIZE", (0,0), (-1,-1), 9),
            ("GRID", (0,0), (-1,-1), 0.5, colors.grey),
            ("ROWBACKGROUNDS", (0,0), (-1,-1), [colors.whitesmoke, colors.white]),
        ]))
        story.append(Paragraph("Section 2: Startup Vendor Details", styles["Heading3"]))
        story.append(t2)
        story.append(Spacer(1, 0.4*cm))

        # Proposal
        story.append(Paragraph("Section 3: Accepted Proposal Summary", styles["Heading3"]))
        story.append(Paragraph(app_obj.proposal_text or "N/A", value_style))
        story.append(Spacer(1, 0.4*cm))

        # Authorisation
        story.append(HRFlowable(width="100%", thickness=0.5, color=colors.grey))
        story.append(Spacer(1, 0.3*cm))
        story.append(Paragraph("Authorised By:", label_style))
        story.append(Paragraph(f"{current_user.name} (Officer ID: {current_user.id})", value_style))
        story.append(Paragraph("Note: This document is generated by ProcureBridge platform. Final procurement must follow GFR 2017 norms and be approved by the Competent Authority.", label_style))

        doc.build(story)
        buffer.seek(0)
        return StreamingResponse(
            buffer,
            media_type="application/pdf",
            headers={"Content-Disposition": f"attachment; filename=\"ProcurementOrder_{ref_id.replace('/', '_')}.pdf\""}
        )
    except ImportError:
        raise HTTPException(status_code=500, detail="PDF generation library not installed. Run: pip install reportlab")
