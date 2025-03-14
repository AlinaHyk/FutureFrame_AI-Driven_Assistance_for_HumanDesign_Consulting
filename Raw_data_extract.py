import os
import pdfplumber
import docx  # requires `python-docx` to be installed
import textract
from bs4 import BeautifulSoup

def convert_doc(in_path, out_path):
    """
    Use textract to handle old .doc files.
    Requires `antiword` installed (on Linux) or `wps` (on Windows) if .doc is proprietary.
    """
    try:
        # textract returns bytes, so decode to UTF-8
        text_bytes = textract.process(in_path)
        text_str   = text_bytes.decode('utf-8', errors='replace')
        # Write in text mode (UTF-8)
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(text_str)
    except Exception as e:
        print(f"[DOC ERROR] {in_path}: {e}")

def convert_docx(in_path, out_path):
    text_lines = []
    try:
        d = docx.Document(in_path)
        for para in d.paragraphs:
            text_lines.append(para.text)
    except Exception as e:
        print(f"[DOCX ERROR] {in_path}: {e}")
    
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(text_lines))

def convert_pdf(in_path, out_path):
    text_lines = []
    try:
        with pdfplumber.open(in_path) as pdf:
            for page in pdf.pages:
                txt = page.extract_text() or ""
                text_lines.append(txt)
    except Exception as e:
        print(f"[PDF ERROR] {in_path}: {e}")
    
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(text_lines))

def convert_html(in_path, out_path):
    text = ""
    try:
        with open(in_path, "r", encoding="utf-8", errors="replace") as f:
            soup = BeautifulSoup(f.read(), "html.parser")
        text = soup.get_text(separator="\n")
    except Exception as e:
        print(f"[HTML ERROR] {in_path}: {e}")
    
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(text)

def process_folder(folder_name, out_root):
    """
    Look at each file in the given folder, convert to .txt,
    and store results in out_root/<folder_name>.
    """
    folder_path = os.path.abspath(folder_name)
    output_subfolder = os.path.join(out_root, os.path.basename(folder_path))
    os.makedirs(output_subfolder, exist_ok=True)

    # Go through all files in <folder_name>
    for file in os.listdir(folder_path):
        in_path = os.path.join(folder_path, file)
        
        # Skip directories
        if not os.path.isfile(in_path):
            continue
        
        base, ext = os.path.splitext(file)
        ext = ext.lower()

        # Construct output .txt path
        out_txt = os.path.join(output_subfolder, base + ".txt")

        # Convert based on extension
        if ext == ".doc":
            convert_doc(in_path, out_txt)
        elif ext == ".docx":
            convert_docx(in_path, out_txt)
        elif ext == ".pdf":
            convert_pdf(in_path, out_txt)
        elif ext in [".html", ".htm"]:
            convert_html(in_path, out_txt)
        else:
            print(f"Skipping: {in_path} (unsupported extension)")

def main():
    # Change this to your root folder that has subfolders like 'Doc', 'Docx', 'HTML', 'PDF'
    base_folder = "Books_Cleand_type"
    input_folders = [ "Docx", "HTML", "PDF"]  # subdirectories inside base_folder
    
    out_root = os.path.join(os.path.abspath("."), "Transcribed")
    os.makedirs(out_root, exist_ok=True)

    # Process each subfolder
    for folder in input_folders:
        full_path = os.path.join(base_folder, folder)
        if os.path.isdir(full_path):
            process_folder(full_path, out_root)
        else:
            print(f"Folder not found or not a directory: {full_path}")

    print("\nAll done\n")

if __name__ == "__main__":
    main()
