import fitz
import pytesseract
from PIL import Image
import os
from app.models.document import Document
from app.utils.vector_store import VectorStore
from app.utils.text_processor import TextProcessor

class DocumentService:
    def __init__(self):
        self.vector_store = VectorStore()
        self.text_processor = TextProcessor()

    def process_document(self, file):
        try:
            temp_path = os.path.join('temp', file.filename)
            os.makedirs('temp', exist_ok=True)
            file.save(temp_path)

            doc = fitz.open(temp_path)
            text = ""
            needs_ocr = False

            for page in doc:
                page_text = page.get_text()
                if not page_text.strip():
                    needs_ocr = True
                    pix = page.get_pixmap()
                    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                    page_text = pytesseract.image_to_string(img)
                text += page_text + '\n'

            if text.strip():
                processed_text = self.text_processor.preprocess(text)
                document = Document(
                    content=processed_text,
                    metadata={
                        'filename': file.filename,
                        'ocr_used': needs_ocr
                    }
                )
                success = self.vector_store.add_document(document)
                return success, f"Document processed successfully{'with OCR' if needs_ocr else ''}"
            return False, "No text content extracted from document"

        except Exception as e:
            return False, f"Error processing document: {str(e)}"
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)