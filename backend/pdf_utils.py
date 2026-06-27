from pypdf import PdfReader

def extract_text_from_pdf(pdf_file):

    reader = PdfReader(pdf_file)

    text = ""

    for page in reader.pages:

        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    return text


if __name__ == "__main__":

    from gemini_utils import (
        generate_structure,
        json_to_mermaid
    )

    text = extract_text_from_pdf(
        "Sample.pdf"
    )

    print("TEXT EXTRACTED:\n")
    print(text[:1000])

    workflow = generate_structure(text)

    print("\nWORKFLOW:\n")
    print(workflow)

    print("\nMERMAID:\n")
    print(json_to_mermaid(workflow))