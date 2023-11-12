from sqlalchemy import create_engine, Column, Integer, String, LargeBinary, URL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
import os
import pyautogui
import time
from docx import Document
import psycopg2
import rdfreader


urll = URL.create(
        drivername="postgresql",
        username="smarthack",
        password="12345",
        host="123.45.67.890",
        port="12345",
        database="smarthack"
    )

engine = create_engine(url)

Base = declarative_base()


class Tender_documents(Base):
    __tablename__ = 'tender_documents'

    id = Column(Integer, primary_key=True)
    doc_name = Column(String)
    down_link = Column(String)
    doc_content = Column(LargeBinary)

    tender_id = Column(String)

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

id = None
doc_name = ''
down_link = ''
tender_id = ''

def read_pdf_and_create_batches(pdf_path, batch_size=2000):
    # Check if the file exists
    if not os.path.exists(pdf_path):
        print(f"The file {pdf_path} does not exist.")
        return

    # Open the PDF file
    with open(pdf_path, 'rb') as pdf_file:
        # Create a PDF reader object
        pdf_reader = pdfreader.PdfFileReader(pdf_file)

        # Initialize variables
        total_words = 0
        current_batch = []
        batch_number = 1

        # Iterate through each page of the PDF
        for page_num in range(pdf_reader.numPages):
            # Get the text from the current page
            page = pdf_reader.getPage(page_num)
            text = page.extractText()

            # Split the text into words
            words = text.split()

            # Check if adding the words from the current page exceeds the batch size
            if total_words + len(words) <= batch_size:
                current_batch.extend(words)
                total_words += len(words)
            else:
                # Save the current batch to a file
                save_batch(current_batch, batch_number)

                # Reset variables for the next batch
                current_batch = words
                total_words = len(words)
                batch_number += 1

        # Save the last batch if there is any remaining text
        if current_batch:
            save_batch(current_batch, batch_number)

def save_batch(words, batch_number):
    # Create a new file for the batch
    batch_filename = f'batch_{batch_number}.txt'
    with open(batch_filename, 'w', encoding='utf-8') as batch_file:
        batch_file.write(' '.join(words))

    print(f'Batch {batch_number} saved to {batch_filename}')


def retrieve_blob_and_save_to_file(record_id, file_path):
    record = session.query(Tender_documents).filter_by(id=record_id).first()
    if record:
        global id, doc_name, down_link, tender_id
        id = record.id
        doc_name = record.doc_name
        down_link = record.down_link
        blob_data = record.doc_content
        tender_id = record.tender_id

        with open(file_path + '\\' + doc_name, 'wb') as file:
            file.write(blob_data)
        print(f"Blob data saved to {file_path}")

        if 'p7m' in doc_name:
            pass
        elif 'p7s' in doc_name:
            pass
        elif 'pdf' in doc_name:
            read_pdf_and_create_batches(file_path + '\\' + doc_name)
        elif 'doc' in doc_name:
            pass
    else:
        print(f"No record found with ID {record_id}")


def rename_file_replace_spaces(filename):
    old_file_path = r"C:\Users\Stefan\Desktop\Facultate\GitHubProjects\SH\cast_p7s" + "\\" + filename

    # Replace spaces with underscores in the filename
    new_filename = filename.replace(" ", "_")
    print(new_filename)

    # Construct the new file path
    new_file_path = r"C:\Users\Stefan\Desktop\Facultate\GitHubProjects\SH\cast_p7s" + "\\" + new_filename
    print(new_file_path)

    # Rename the file
    os.rename(old_file_path, new_file_path)
    print(f"File successfully renamed from '{old_file_path}' to '{new_file_path}'.")
    return new_file_path


def open_file_explorer(path):
    # Open Start menu
    pyautogui.hotkey('winleft')
    time.sleep(1)  # Wait for the Start menu to open

    # Type the path
    pyautogui.write(path)
    time.sleep(1)  # Wait for typing to complete

    # Press Enter to open File Explorer
    pyautogui.press('enter')
    time.sleep(2)

    # Maximize the window
    pyautogui.hotkey('winleft', 'up')
    time.sleep(3)  # Wait for the window to maximize

    # Move the mouse to specific coordinates (replace with your desired coordinates)
    target_x, target_y = 500, 155  # Adjust these coordinates based on your needs
    pyautogui.moveTo(target_x, target_y, duration=1)  # Move the mouse to the specified position over 1 second

    # Right-click at the current mouse position
    pyautogui.rightClick()
    time.sleep(1)

    # Move down two times
    pyautogui.press('down')
    time.sleep(0.5)  # Adjust the sleep duration based on your system's performance
    pyautogui.press('down')
    time.sleep(0.5)

    # Press Enter to open File Explorer
    pyautogui.press('enter')
    time.sleep(2)

    # Move the mouse to specific coordinates (replace with your desired coordinates)
    target_x, target_y = 700, 750  # Adjust these coordinates based on your needs
    pyautogui.moveTo(target_x, target_y, duration=1)  # Move the mouse to the specified position over 1 second

    # Right-click at the current mouse position
    pyautogui.leftClick()
    time.sleep(1)


def read_docx(filename):
    doc = Document(filename)
    content = ""
    for paragraph in doc.paragraphs:
        content += paragraph.text + "\n"
    return content


def split_into_batches(text, batch_size):
    batches = []
    words = text.split()
    current_batch = ""
    current_word_count = 0

    for word in words:
        if current_word_count + len(word) + 1 <= batch_size:
            current_batch += word + " "
            current_word_count += len(word) + 1
        else:
            batches.append(current_batch.strip())
            current_batch = word + " "
            current_word_count = len(word) + 1

    if current_batch:
        batches.append(current_batch.strip())

    return batches


def main(new_file_path):
    filename = new_file_path
    batch_size = 2000

    content = read_docx(filename)
    batches = split_into_batches(content, batch_size)

    for i, batch in enumerate(batches):
        print(f"Batch {i + 1}:\n{batch}\n")

    # Optionally, you can store the batches in a list
    # batches_list = [batch for batch in batches]


for record_id in range(299):
    # Usage example:
    record_id = 250  # Replace with the actual ID of the record you want to retrieve
    file_path = r'/cast_p7s'  # Replace with the desired local file path
    filename = retrieve_blob_and_save_to_file(record_id, file_path)

# RENAME
filename = "Model_acord-cadru_LD_Medicamente_PN_Oncologie.doc.p7m"
filename = "Model acord-cadru LD Medicamente PN Oncologie.doc.p7m"
new_file_path = rename_file_replace_spaces(filename)

# CONVERSION_PATH
target_path = r'/cast_p7s'
open_file_explorer(target_path)

# REMOVE OLD FILE
os.remove(new_file_path)

# SEPARATE FILE IN BATCHES
new_file_path = "Model_acord-cadru_LD_Medicamente_PN_Oncologie.doc.p7m"
print(new_file_path[:-4])
main(new_file_path[:-4])


