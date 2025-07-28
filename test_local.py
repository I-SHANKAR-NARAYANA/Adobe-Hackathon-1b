import os
import json
import sys
from main import PDFOutlineExtractor, PersonaDocumentAnalyzer

def test_round_1a(folder_path):
    """Test Round 1A - PDF Outline Extraction for all PDFs in a folder"""
    print("Testing Round 1A - PDF Outline Extraction")

    extractor = PDFOutlineExtractor()

    if not os.path.isdir(folder_path):
        print(f"Provided path {folder_path} is not a directory.")
        return

    pdf_files = [f for f in os.listdir(folder_path) if f.lower().endswith('.pdf')]

    if not pdf_files:
        print("No PDF files found in the folder.")
        return

    for pdf_file in pdf_files:
        pdf_path = os.path.join(folder_path, pdf_file)
        print(f"Processing: {pdf_path}")
        result = extractor.extract_outline(pdf_path)

        output_filename = f"outline_{os.path.splitext(pdf_file)[0]}.json"
        output_path = os.path.join(folder_path, output_filename)
        with open(output_path, "w") as f:
            json.dump(result, f, indent=2)
        print(f"Saved: {output_path}")

def test_round_1b(folder_path):
    """Test Round 1B - Persona Analysis using input JSON files and PDFs"""
    print("Testing Round 1B - Persona Analysis")

    analyzer = PersonaDocumentAnalyzer()

    if not os.path.isdir(folder_path):
        print(f"Provided path {folder_path} is not a directory.")
        return

    json_files = [
        f for f in os.listdir(folder_path)
        if f.lower().endswith("input.json")
    ]

    if not json_files:
        print("No valid input JSON files found in the folder.")
        return

    for json_file in json_files:
        json_path = os.path.join(folder_path, json_file)
        print(f"Processing input: {json_path}")
        
        with open(json_path, "r") as f:
            data = json.load(f)

        documents_info = data.get("documents", [])
        persona = data.get("persona", {}).get("role", "")
        job = data.get("job_to_be_done", {}).get("task", "")

        pdfs_folder = os.path.join(folder_path, "PDFs")
        pdf_paths = []
        for doc in documents_info:
            pdf_file = doc.get("filename")
            pdf_path = os.path.join(pdfs_folder, pdf_file)
            if os.path.exists(pdf_path):
                pdf_paths.append(pdf_path)
            else:
                print(f"Warning: Missing PDF file {pdf_file}")

        if not pdf_paths:
            print(f"No valid PDFs found for input: {json_file}")
            continue

        result = analyzer.analyze_documents(pdf_paths, persona, job)

        output_file = json_file.replace("input.json", "output.json")
        output_path = os.path.join(folder_path, output_file)
        with open(output_path, "w") as f:
            json.dump(result, f, indent=2)
        print(f"Saved: {output_path}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python test_local.py [1a|1b] <folder_path>")
        sys.exit(1)

    mode = sys.argv[1]
    folder = sys.argv[2]

    if mode == "1a":
        test_round_1a(folder)
    elif mode == "1b":
        test_round_1b(folder)
    else:
        print("Invalid mode. Use '1a' or '1b'.")
