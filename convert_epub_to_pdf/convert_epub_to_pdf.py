# Script: convert_epub_to_pdf
import sys
from pathlib import Path
import subprocess
import zipfile
import xml.etree.ElementTree as ET


def is_valid_epub(epub_path: Path) -> bool:
    # Must be a valid ZIP file
    if not zipfile.is_zipfile(epub_path):
        return False

    try:
        with zipfile.ZipFile(epub_path, 'r') as z:
            # Check mimetype
            if 'mimetype' not in z.namelist():
                return False

            mimetype = z.read('mimetype').decode('utf-8').strip()
            if mimetype != "application/epub+zip":
                return False

            # Check container.xml
            container_path = 'META-INF/container.xml'
            if container_path not in z.namelist():
                return False

            container_xml = z.read(container_path)
            root = ET.fromstring(container_xml)

            # Find the OPF file path
            ns = {'c': 'urn:oasis:names:tc:opendocument:xmlns:container'}
            rootfiles = root.findall('c:rootfiles/c:rootfile', ns)
            if not rootfiles:
                return False

            opf_path = rootfiles[0].attrib.get('full-path')
            if not opf_path or opf_path not in z.namelist():
                return False

            # Optional: try parsing the OPF file
            try:
                opf_xml = z.read(opf_path)
                ET.fromstring(opf_xml)  # basic well-formedness check
            except Exception:
                return False

            return True

    except Exception:
        return False


def resolve_folders(args):
    """
    Determine source and target folders based on number of arguments
    Rules:
        0 args -> use current user's Downloads folder for both
        1 args -> source = arg, target = same
        2 args -> source = arg1, target = arg2
    :param args: An array of arguments provided on the command line
    :return: source and target folders
    """
    if len(args) == 0:
        downloads = Path.home() / "Downloads"
        source = downloads
        target = downloads
    elif len(args) == 1:
        source = Path(args[0])
        target = source
    elif len(args) == 2:
        source = Path(args[0])
        target = Path(args[1])
    else:
        raise ValueError("Usage: convert_epub_to_pdf [source] [target]")

    return source, target


def do_epub_to_pdf_conversion(epub_path: Path, pdf_path: Path):
    subprocess.run([
        "ebook-convert",
        str(epub_path),
        str(pdf_path),
        "--paper-size", "a4",
        "--pdf-page-numbers",
        "--pdf-default-font-size", "12",
        "--pretty-print"
        ], check=True)


def do_batch_conversion(source_folder_path: Path, target_folder_path: Path):
    for epub_file in source_folder_path.glob("*.epub"):
        if not is_valid_epub(epub_file):
            print(f"INVALID EPUB - skipping: {epub_file.name}")
            continue

        pdf_file = target_folder_path / epub_file.with_suffix(".pdf").name
        print("Checking....", epub_file)
        if pdf_file.exists():
            print(f"Skipping {epub_file.name} - PDF file already exists.")
        else:
            print(f"converting {epub_file.name} -> {pdf_file.name}")
            try:
                do_epub_to_pdf_conversion(epub_file, pdf_file)
            except Exception as e:
                print(f"Error processing {epub_file}: {e}")


if __name__ == '__main__':
    # extract only the arguments from the command line
    args = sys.argv[1:]
    source_folder, target_folder = resolve_folders(args)
    do_batch_conversion(source_folder, target_folder)



