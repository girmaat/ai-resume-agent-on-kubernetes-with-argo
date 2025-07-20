# ------------------------------------------------------------------------------
# Purpose: Test that me/summary.txt and me/gi.pdf can be loaded and parsed.
#
# How to Run:
#   python tests/4.test_resume_loading.py
#
# Expected Output:
#   summary.txt loaded with a text preview
#   gi.pdf loaded with number of pages and sample extracted text
# ------------------------------------------------------------------------------

def test_summary_and_pdf():
    import os
    from pypdf import PdfReader

    summary_path = "me/summary.txt"
    pdf_path = "me/gi.pdf"

    if not os.path.exists(summary_path):
        print("ERROR: summary.txt is missing")
        return
    if not os.path.exists(pdf_path):
        print("ERROR: gi.pdf is missing")
        return

    summary = open(summary_path, encoding="utf-8").read()
    print("summary.txt loaded:", summary[:60], "...")

    reader = PdfReader(pdf_path)
    pages = [p.extract_text() for p in reader.pages if p.extract_text()]
    print("gi.pdf loaded with", len(pages), "pages")
    print("Sample text:", pages[0][:60] if pages else "No text extracted")

if __name__ == "__main__":
    test_summary_and_pdf()
