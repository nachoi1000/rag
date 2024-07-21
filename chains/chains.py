from langchain.chains import create_history_aware_retriever
from langchain_core.prompts import MessagesPlaceholder, ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain

def retriever_chain(vectorstore):
    """This function recieves a vectordatabase and returns a chain which will be used as a retriever_chain"""
    
    prompt = ChatPromptTemplate.from_messages([
    MessagesPlaceholder(variable_name="chat_history"),
    ("user", "{input}"),
    ("user", "Given the above conversation, generate a search query to look up in order to get information relevant to the conversation")
    ])

    retriever = vectorstore.as_retriever()
    
    llm = ChatOpenAI()
    
    retriever_chain = create_history_aware_retriever(llm, retriever, prompt)
    return retriever_chain


def main_chain(vectorstore):
    """This function recieves a vectorstore and returns a chain which will be used as a conversational_retrieval_chain"""
    
    prompt = ChatPromptTemplate.from_messages([
    ("system", "Answer ONLY with the facts listed in the list of sources below. If there isn't enough information below, say you don't know. Do not generate answers that don't use the sources below. Answer the user's questions based on the below context:\n\n{context}"),
    MessagesPlaceholder(variable_name="chat_history"),
    ("user", "{input}")
    ])
    
    llm = ChatOpenAI()
    
    document_chain = create_stuff_documents_chain(llm, prompt)
    
    conversational_retrieval_chain = create_retrieval_chain(retriever_chain(vectorstore=vectorstore), document_chain)
    return conversational_retrieval_chain