from .models import UploadedDocument
from .utils import extract_text


def run_ocr(document_id):
    doc = UploadedDocument.objects.get(pk=document_id)

    try:
        text = extract_text(doc.file.path)
        doc.extracted_text = text
        doc.status = 'done'
    except Exception as e:
        doc.status = 'error'
        doc.error_message = str(e)
    finally:
        doc.save()
        