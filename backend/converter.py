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
os.makedirs(PDF_DIR, exist_ok=True)

UNICODE_FONT_URL = "https://github.com/reingart/pyfpdf/raw/master/unifont/DejaVuSans.ttf"
FONT_PATH = os.path.join(BASE_DIR, 'DejaVuSans.ttf')

def download_unicode_font():
    if not os.path.exists(FONT_PATH):
        import requests
        try:
            r = requests.get(UNICODE_FONT_URL, timeout=15)
            r.raise_for_status()
            with open(FONT_PATH, 'wb') as f: f.write(r.content)
            logger.info("Unicode font downloaded.")
        except Exception as e:
            logger.error(f"Failed to download font: {e}")

def generate_pdf(md_text):
    """Logique centrale de génération PDF."""
    try:
        html_content = markdown.markdown(md_text, extensions=['tables', 'fenced_code'])
        pdf = HTMLPDF()
        download_unicode_font()
        
        fname = f"doc_{uuid.uuid4().hex[:8]}.pdf"
        fpath = os.path.join(PDF_DIR, fname)
        
        if os.path.exists(FONT_PATH):
            pdf.add_font('DejaVu', '', FONT_PATH, uni=True)
            pdf.set_font('DejaVu', '', 11)
            face = "DejaVu"
        else:
            pdf.set_font("helvetica", '', 11)
            face = "helvetica"

        full_html = f'<font face="{face}" size="11">{html_content}</font>'
        pdf.add_page()
        pdf.write_html(full_html)
        pdf.output(fpath)
        return fname, fpath
    except Exception as e:
        logger.error(f"Render Error: {e}")
        raise
