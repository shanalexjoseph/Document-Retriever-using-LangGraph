import fitz  # PyMuPDF
import re

def extract_fields(file_path):
    doc = fitz.open(file_path)
    text = "\n".join(page.get_text() for page in doc)
    national_id_match = re.search(r"National ID\\s*[:\\-]?\\s*(\\d{10})", text, re.IGNORECASE)
    action_match = re.search(r"Action\\s*[:\\-]?\\s*(.*?)(?:\\n|$)", text, re.IGNORECASE)

    return {
        "ocr_text": text,
        "national_id": national_id_match.group(1) if national_id_match else None,
        "action": action_match.group(1).strip().lower().replace(" ", "_") if action_match else None
    }
