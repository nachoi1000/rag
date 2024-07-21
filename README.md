# RAG Chatbot
This project consists of a webapp retrieval augmented generation (RAG) chatbot

## Introduction
-----
The Rag Chatbot Webapp is a Python application that allows you to chat with multiple documents (PDF or TXT documents). You can ask questions about the document using natural language, and the application will provide ONLY relevant responses based on the content of the documents. It won't answer if the question does not have context to be responded. This app utilizes a language model to generate accurate answers to your queries. Please note that the app will respond based only on the document.

## How It Works
-----
The application follows these steps to provide responses to your questions:

1. Document Loading: The app reads multiple PDF or TXT documents and extracts their text content.

2. Text Chunking: The extracted text is divided into smaller chunks that can be processed effectively.

3. Embedding and Vectorstore: The application utilizes a large language model to generate vector representations (embeddings) of each text chunks for each document.

4. Similarity Matching: When you ask a question (generate an user prompt), the app compares it prompt with the vectors of each text chunks and retrieves the most semantically similar ones.

5. Response Generation: The selected chunks are passed to the language model as context in a prompt, the large language model will generates a response using the context or not depending on the original user prompt.

## Dependencies and Installation
----------------------------
To install the MultiPDF Chat App, please follow these steps:

1. Clone the repository to your local machine.
2. Python 3.10 or above version.
3. Generate a python virtual environment and install the required dependencies, feel free to follow these steps:
   ```
   python -m venv name_of_the_virtualenv
   change dir to your local machine repository and execute name_of_the_virtualenv/Scripts/activate
   pip install -r requirements.txt
   ```
 You can also execute the execute.ps1 or execute.sh to automatically generate the python virtual environment and open streamlit.

4. Obtain an API key from OpenAI and add it to an `.env` file in the project directory.
```commandline
OPENAI_API_KEY=your_secrit_api_key
```

## Usage
-----
To use the Rag Chatbot Webapp, follow these steps:

1. Ensure that you have installed the required dependencies, create `.env` and added the OpenAI API key in the file.

2. Run the `execute.ps1` or `execute.sh` file. Or activeate the virtual environment and Execute the following command:
   ```
   streamlit run main.py
   ```

3. The application will launch in your default web browser, displaying the user interface.

4. Load multiple documents into the app by following the provided instructions. Or Add your files in data folder.

5. Ask questions in natural language about your documents using the chat interface.
