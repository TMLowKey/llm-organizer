import os
from openai import OpenAI
from pypdf import PdfReader
import streamlit as st

api_key = st.text_input("Enter your OpenAI API key:")
client = OpenAI(api_key=api_key)
level1 = ["Unknown","Journals", "IAEA"]
level2 = ["TerchnicalReportSeries", "Standards", "SpecificSafetyRequirements", "SpecificSafetyGuide", "SafetyStandardsSeries", "SafetySeries", "SafetyReportsSeries", "SafetyGuide", "SafetyFundamentals", "PracticalRadMan", "PeerDicussionRegPracticies", "NuclearSecuritySeries", "InternNuclearVerifSeries", "INSAGSeries", "Info", "IAEA-TechnicalReport", "IAEA-TechnicalGuidelines", "IAEA-TECDOCSeries", "IAEA-SafetyStandards", "IAEA-NuclearEnergySeries", "IAEA-EBP-WWER", "Glossary", "GeneralSafetyRequirements"]

def create_default_folders():
    for item in level1:
        try:
            path = f"./{item}"
            os.mkdir(path)
            print(f"Folder '{path}' created successfully!")
        except FileExistsError:
            pass
    for item in level2:
        try:
            path = f"./IAEA/{item}"
            os.mkdir(path)
            print(f"Folder '{path}' created successfully!")
        except FileExistsError:
            pass

def extract_text_from_pdf(file):         
    pdf_reader = PdfReader(file)  
    num_pages = len(pdf_reader.pages)    
    text = ""                            
    for page_num in range(num_pages):    
        page = pdf_reader.pages[page_num]
        text += page.extract_text()      
    return text                          

# Define a function to generate answers to user questions using the ChatGPT API
def generate_answer(location, text):

    question = f"Can you look on this text and decide in which of those two folders {location} it should belong. Answer only in one word."

    max_context_length = 4096 - len(question) - 30
    truncated_text = text[:max_context_length]

    prompt = f"{truncated_text}\n\nQuestion: {question}\nAnswer:"
    response = client.chat.completions.create(model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt}
    ])
    return response.choices[0].message.content.strip()

def organize_file(category, file):
    if category == level1[1]:
        upload_directory = f"./{level1[1]}"
    elif category == level1[2]:
        upload_directory = f"./{level1[2]}"
    else:
        upload_directory = f"./{level1[0]}"

    file_path = os.path.join(upload_directory, file.name)

    with open(file_path, "wb") as f:
        f.write(file.getbuffer())


def handle_file_upload():
    file = st.file_uploader("Upload a PDF file", type=["pdf"])
    if file is not None:
        # Extract text from the saved PDF file
        text = extract_text_from_pdf(file)
        location = level1
        answer = generate_answer(location, text)

        if st.button("Submit"):
            answer = generate_answer(location, text)
            st.write(answer)
            organize_file(answer, file)

# Define a main function to run the program
def main():
    create_default_folders()
    handle_file_upload()

if __name__ == "__main__":
    main()
