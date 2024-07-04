import os
from openai import OpenAI
from pypdf import PdfReader

api_key = input("Enter your OpenAI API key: ")
client = OpenAI(api_key=api_key)
level1 = ["Unknown", "Journals", "IAEA"]
level2 = ["TechnicalReportSeries", "Standards", "SpecificSafetyRequirements", "SpecificSafetyGuide", "SafetyStandardsSeries", "SafetySeries", "SafetyReportsSeries", "SafetyGuide", "SafetyFundamentals", "PracticalRadMan", "PeerDiscussionRegPractices", "NuclearSecuritySeries", "InternNuclearVerifSeries", "INSAGSeries", "Info", "IAEA-TechnicalReport", "IAEA-TechnicalGuidelines", "IAEA-TECDOCSeries", "IAEA-SafetyStandards", "IAEA-NuclearEnergySeries", "IAEA-EBP-WWER", "Glossary", "GeneralSafetyRequirements"]

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

def extract_text_from_pdf(file_path):
    with open(file_path, 'rb') as file:
        pdf_reader = PdfReader(file)
        num_pages = len(pdf_reader.pages)
        text = ""
        for page_num in range(num_pages):
            page = pdf_reader.pages[page_num]
            text += page.extract_text()
    return text

def generate_answer(location, text):
    question = f"Can you look at this text and decide in which of these two folders {location} it should belong? Answer only in one word."
    
    max_context_length = 4096 - len(question) - 30
    truncated_text = text[:max_context_length]
    
    prompt = f"{truncated_text}\n\nQuestion: {question}\nAnswer:"
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content.strip()

def organize_file(category, file_path):
    if category == level1[1]:
        upload_directory = f"./{level1[1]}"
    elif category == level1[2]:
        upload_directory = f"./{level1[2]}"
    else:
        upload_directory = f"./{level1[0]}"
    
    file_name = os.path.basename(file_path)
    new_file_path = os.path.join(upload_directory, file_name)
    os.rename(file_path, new_file_path)

def main():
    create_default_folders()
    
    file_path = input("Enter the path to the PDF file: ")
    text = extract_text_from_pdf(file_path)
    location = level1
    answer = generate_answer(location, text)
    
    print(f"Category: {answer}")
    organize_file(answer, file_path)

if __name__ == "__main__":
    main()

