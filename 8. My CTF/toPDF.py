import fitz  # PyMuPDF

def add_attachment_to_pdf(pdf_path: str, attachment_path: str, output_pdf_path: str) -> None:
    # פתיחת קובץ ה-PDF
    doc = fitz.open(pdf_path)

    # הוספת הקובץ המצורף
    doc.attachFile(attachment_path)

    # שמירת הקובץ עם הקובץ המצורף
    doc.save(output_pdf_path)

if __name__ == "__main__":
    pdf_path = "mission.pdf"  # קובץ ה-PDF המקורי
    attachment_path = "client.exe"  # הקובץ שנרצה להוסיף
    output_pdf_path = "mission_with_attachment.pdf"  # קובץ ה-PDF החדש עם הקובץ המצורף

    add_attachment_to_pdf(pdf_path, attachment_path, output_pdf_path)
    print(f"Attachment added to PDF and saved as '{output_pdf_path}'")
