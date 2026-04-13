import os
import markdown
import uuid
import logging
from fpdf import FPDF, HTMLMixin

# Configuration logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class HTMLPDF(FPDF, HTMLMixin):
    pass

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PDF_DIR = os.path.join(BASE_DIR, 'pdfs')
FONT_REG = "C:\\Windows\\Fonts\\arial.ttf"
FONT_BOLD = "C:\\Windows\\Fonts\\arialbd.ttf"

os.makedirs(PDF_DIR, exist_ok=True)

def generate_pdf(md_text):
    """Logique centrale de génération PDF."""
    try:
        html_content = markdown.markdown(md_text, extensions=['tables', 'fenced_code'])
        face = "arial" if os.path.exists(FONT_REG) else "helvetica"
        full_html = f'<font face="{face}" size="11">{html_content}</font>'

        fname = f"doc_{uuid.uuid4().hex[:8]}.pdf"
        fpath = os.path.join(PDF_DIR, fname)
        
        pdf = HTMLPDF()
        try:
            if os.path.exists(FONT_REG):
                pdf.add_font('arial', '', FONT_REG)
            if os.path.exists(FONT_BOLD):
                pdf.add_font('arial', 'B', FONT_BOLD)
            pdf.set_font(face, '', 11)
        except:
            pdf.set_font("helvetica", '', 11)

        pdf.add_page()
        pdf.write_html(full_html)
        pdf.output(fpath)
        return fname, fpath
    except Exception as e:
        logger.error(f"Render Error: {e}")
        raise
