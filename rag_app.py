# To execute the app: streamlit run app.py
import os
from streamlit.web import bootstrap
import streamlit as st
import openai
from langchain_core.messages import HumanMessage, AIMessage
from chains.chains import main_chain
from indexing.vectorstore import generate_langchain_vectorstore, add_document_to_vectordatabase
from common.utils import generate_document, generate_document_from_uploaded_file
from dotenv import load_dotenv

load_dotenv()

def process_local_data():
    """This function processes all local documents inside the data folder, generates the vectorstore, and returns it"""
    directory_path = "./data"
    documentos = []

    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)

        try:
            documento = generate_document(file_path=file_path)
            if documento:
                documentos.append(documento)
        except Exception as e:
            pass  # Just pass on errors without printing them in the frontend

    if "vector_store" in st.session_state:
        st.session_state.vector_store = add_document_to_vectordatabase(documentos, st.session_state.vector_store)
    else:
        st.session_state.vector_store = generate_langchain_vectorstore(documents=documentos)

def process_uploaded_files(files):
    """This function processes the uploaded files and updates the vectorstore"""
    documentos = []

    for file in files:
        documento = generate_document_from_uploaded_file(file=file)
        if documento:
            documentos.append(documento)

    if "vector_store" in st.session_state:
        st.session_state.vector_store = add_document_to_vectordatabase(documentos, st.session_state.vector_store)
    else:
        st.session_state.vector_store = generate_langchain_vectorstore(documents=documentos)

# Initialize chat history if not in session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        AIMessage(content="Hello, I am a bot. How can I help you?"),
    ]

# Set page configuration
st.set_page_config(page_title="RAG ChatBot", page_icon=":robot_face:")

st.title("RAG Chatbot")

# Sidebar with buttons
with st.sidebar:
    st.subheader("Your documents")
    files = st.file_uploader("Upload your PDFs here and click on 'Process'", accept_multiple_files=True)
    if st.button("Process"):
        with st.spinner("Processing"):
            process_uploaded_files(files)
            st.write("Files processed and database updated.")

    if st.button("Use Local Data"):
        st.write("Procesando datos locales...")
        process_local_data()
        st.write("Datos locales procesados y base de datos generada.")

    if st.button("Reset Conversation"):
        st.session_state.chat_history = [
            AIMessage(content="Hello, I am a bot. How can I help you?"),
        ]
        st.write("Conversación reiniciada.")

# Function to get response
def get_response(query, chat_history):
    if "vector_store" in st.session_state:
        vector_store = st.session_state.vector_store
    else:
        vector_store = None  # Handle this case as needed
    
    chain = main_chain(vector_store)
    response = chain.invoke({
        "chat_history": chat_history,
        "input": query
    })
    return response['answer']

# Display conversation
for message in st.session_state.chat_history:
    if isinstance(message, HumanMessage):
        with st.chat_message("Human"):
            st.markdown(message.content)
    elif isinstance(message, AIMessage):
        with st.chat_message("AI"):
            st.markdown(message.content)

# User input
user_query = st.chat_input("Your message")
if user_query:
    st.session_state.chat_history.append(HumanMessage(content=user_query))

    with st.chat_message("Human"):
        st.markdown(user_query)

    with st.chat_message("AI"):
        ai_response = get_response(query=user_query, chat_history=st.session_state.chat_history)
        st.markdown(ai_response)

    st.session_state.chat_history.append(AIMessage(content=ai_response))