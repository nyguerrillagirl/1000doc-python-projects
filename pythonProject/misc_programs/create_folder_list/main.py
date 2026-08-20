# I created this script to help me get an entire list of filenames converted into a list
import os
import re


def natural_key(s):
    return [int(text) if text.isdigit() else text.lower()
            for text in re.split(r'(\d+)', s)]


def create_list(file_path):
    files = [f for f in os.listdir(file_path)
            if os.path.isfile(os.path.join(file_path, f))]
    return sorted(files, key=natural_key)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    filePath = r"C:\Users\lorra\OneDrive\Documents\74_2026_C\EBOOKS\COMMODORE_64_BOOKS"
    files = create_list(filePath)
    cleaned_files = [f.replace("_", " ").removesuffix(".pdf") for f in files]
    for f in cleaned_files:
        print(f)


