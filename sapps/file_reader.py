import os
import mimetypes
import json
import csv
import configparser
import xml.etree.ElementTree as ET
from PyPDF2 import PdfReader
from docx import Document
import openpyxl
import yaml
from bs4 import BeautifulSoup

def is_binary_file(file_path):
    """
    Determines if a file is likely binary by reading the first 1024 bytes.
    """
    with open(file_path, 'rb') as file:
        chunk = file.read(1024)
        return b'\x00' in chunk  # If there are null bytes, it's likely binary

def read_plain_text(file_path):
    """Reads plain text files (e.g., .txt, .py, etc.)."""
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
        content = file.read()
    return content

def read_pdf(file_path):
    """Reads PDFs using PyPDF2."""
    content = ""
    reader = PdfReader(file_path)
    for page in reader.pages:
        content += page.extract_text() or ""
    return content

def read_word_doc(file_path):
    """Reads .docx files using python-docx."""
    doc = Document(file_path)
    content = '\n'.join([para.text for para in doc.paragraphs])
    return content

def read_excel(file_path):
    """Reads Excel files using openpyxl."""
    wb = openpyxl.load_workbook(file_path)
    sheet = wb.active
    content = ""
    for row in sheet.iter_rows(values_only=True):
        content += ' '.join([str(cell) for cell in row if cell is not None]) + '\n'
    return content

def read_csv(file_path):
    """Reads CSV files using the csv module."""
    content = ""
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            content += ', '.join(row) + '\n'
    return content

def read_json(file_path):
    """Reads JSON files using the json module."""
    with open(file_path, 'r') as file:
        content = json.dumps(json.load(file), indent=4)
    return content

def read_html(file_path):
    """Reads HTML files using BeautifulSoup."""
    with open(file_path, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')
    return soup.get_text()

def read_xml(file_path):
    """Reads XML files using xml.etree.ElementTree."""
    tree = ET.parse(file_path)
    root = tree.getroot()
    return ET.tostring(root, encoding='unicode')

def read_yaml(file_path):
    """Reads YAML files using PyYAML."""
    with open(file_path, 'r') as file:
        content = yaml.safe_load(file)
    return yaml.dump(content)

def read_ini(file_path):
    """Reads INI configuration files using configparser."""
    config = configparser.ConfigParser()
    config.read(file_path)
    content = ""
    for section in config.sections():
        content += f"[{section}]\n"
        for key, value in config.items(section):
            content += f"{key} = {value}\n"
    return content

def read_file(file_path):
    """
    Attempts to read the file based on its type.
    Calls appropriate file-reading functions for different formats.
    """
    try:
        if os.path.exists(file_path):
            if is_binary_file(file_path):
                print(f"The file at {file_path} appears to be binary and is not human-readable.")
                return
            
            file_type, _ = mimetypes.guess_type(file_path)

            if file_type and 'text' in file_type:
                content = read_plain_text(file_path)
            elif file_type == 'application/pdf':
                content = read_pdf(file_path)
            elif file_type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
                content = read_word_doc(file_path)
            elif file_type == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet':
                content = read_excel(file_path)
            elif file_type == 'text/csv':
                content = read_csv(file_path)
            elif file_type == 'application/json':
                content = read_json(file_path)
            elif file_type == 'text/html':
                content = read_html(file_path)
            elif file_type == 'application/xml' or file_type == 'text/xml':
                content = read_xml(file_path)
            elif file_type == 'application/x-yaml' or file_type == 'text/yaml':
                content = read_yaml(file_path)
            elif file_type == 'text/ini':
                content = read_ini(file_path)
            else:
                print(f"Unsupported file type: {file_type}")
                return
            
            print(f"\n--- Content of {file_path} ---\n")
            print(content)
            print("\n-------------------------------\n")
        else:
            print(f"The file at {file_path} does not exist.")
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")

def read_directory(directory_path):
    """
    Iterates through all the files in the directory and subdirectories,
    calling read_file() on each human-readable file.
    """
    try:
        if os.path.exists(directory_path):
            for root, dirs, files in os.walk(directory_path):
                for file_name in files:
                    file_path = os.path.join(root, file_name)
                    print(f"Reading {file_path}")
                    read_file(file_path)
        else:
            print(f"The directory {directory_path} does not exist.")
    except Exception as e:
        print(f"An error occurred while reading the directory: {e}")

if __name__ == "__main__":
    print("Select an option:")
    print("1. View file contents")
    print("2. View directory contents")
    user_input = input("Enter: ")

    if user_input == "1":
        file_path = input("Enter the file path: ")
        read_file(file_path)
    elif user_input == "2":
        directory_path = input("Enter the directory path: ")
        read_directory(directory_path)
    else:
        print("Invalid option. Please choose either 1 or 2.")
