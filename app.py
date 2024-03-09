import streamlit as st 
import PyPDF2
import io
import openai
import docx2txt
import pyperclip

st.title("Document Reading App")

openai.api_key = st.sidebar.text_input("Enter your OpenAI API kEY", type= "password")

#Defining a function to extract text from a PDF file 
def extract_text_from_pdf(file):
    #creatinda bytesio object
    pdf_file_obj = io.BytesIO(file.read())
    #Createing a pdf reader object
    pdf_reader = PyPDF2.PdfReader(pdf_file_obj)
    #an empty string to stopre the ectracted text
    text = ''
    #looping through each page
    for page_num in range (len(pdf_reader.pages)):
        pages = pdf_reader.pages[page_num]
        text += pages.extract_text()
    #returning the extrcated text 
    return text 

#Defining a function to extract text from a Word file 
def extract_text_from_docx(file):
    #creatinda bytesio object
    docx_file_obj = io.BytesIO(file.read())
    #Createing a pdf reader object
    text = docx2txt.PdfReader(docx_file_obj)
    return text

#Defining a function to extract text from a text file 
def extract_text_from_txt(file):
    text = file.read().decode('utf-8')
    return text 

##Defining a function to extract text from a file based on its typr
def extract_text_from_file(file):
    #checking the type of uploaded file 
    if file.type == 'application/pdf':
        text = extract_text_from_pdf(file)
    elif file.type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
        text = extract_text_from_docx(file)
    elif file.type == 'text/plain':
        text = extract_text_from_txt(file)
    else:
        st.error("Unsupported file type!")
        text = None
    return text 

#Defining function to generate question using openai gpt-3
# def get_questions_from_gpt(text):
#     #Selction first 4096 characters 
#     prompt = text[:4096]
#     #generating a question 
#     response = openai.completions.create(engine="text-davinci-003", prompt=prompt, temperature=0.5, max_tokens=30)
#     return response.choices[0].text.strip()

def get_answers_from_gpt(text, question):
    #Selction first 4096 characters as well as question 
    prompt1 = text[:4096] + "\nQuestion:" + question + "\nAnswer"
    response = openai.completions.create(model="gpt-3.5-turbo-instruct", prompt=prompt1, temperature=0.6, max_tokens=2000)
    return response.choices[0].text.strip()

def main():
    st.title("Ask Questions from uploaded document")
    #creating an uploaded file
    uploaded_file = st.file_uploader("Choose a file", type={"pdf", "docx","txt"})
    #checking if file has been uploaded
    if uploaded_file is not None:
        text = extract_text_from_file(uploaded_file)
        
        if text is not None:
            #generating qustion from gpt function 
            # question = get_questions_from_gpt(text)
            # st.write("Questions: " + question)
            
            user_question = st.text_input("Ask a Question about your document!")
            if user_question:
                #generating an asnwer 
                answer = get_answers_from_gpt(text, user_question)
                st.write("Answer: " + answer)
                
                #Creatinf a button to copy the answer 
                if st.button("Copy Aswer Text"):
                    pyperclip.copy(answer)
                    st.success("Answer text copied to clipboard")
                    
if __name__ == "__main__":
    main()
            