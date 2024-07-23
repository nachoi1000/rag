import shutil
import os
from langchain.vectorstores.chroma import Chroma
from langchain.embeddings import SentenceTransformerEmbeddings
import chromadb
from chromadb.utils import embedding_functions



def generate_vectordb(folder = "my_vectordb"): #Funtion to be used witouth LangchainChroma 
    """This functions generate a vectordb in the specified folder."""
    # Instantiate chromadb instance. Data is stored on disk (a folder named 'my_vectordb' will be created in the same folder as this file).
    chroma_client = chromadb.PersistentClient(path=folder)
    # Select the embedding model to use.
    # List of model names can be found here https://www.sbert.net/docs/pretrained_models.html
    sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-mpnet-base-v2")
    # Create the collection, aka vector database. Or, if database already exist, then use it. Specify the model that we want to use to do the embedding.
    collection = chroma_client.get_or_create_collection(name="my_collection", embedding_function=sentence_transformer_ef)
    return collection


def add_documents_vectordatabase(documentos, collection): #Funtion to be used witouth LangchainChroma 
    """This functions receives a document or list of documents and add them into a vector_database"""
    documents = []
    metadatas = []
    ids = []

    # Obtener el último ID de la colección
    ids_collection = collection.get()["ids"]
    if ids_collection:
        last_id = int(ids_collection[-1])
    else:
        last_id = 0

    # Contar a partir del último ID
    id_counter = last_id + 1

    # Asegurarse de que 'documentos' es una lista
    if not isinstance(documentos, list):
        documentos = [documentos]

    for document in documentos:
        for chunk in document.chunks:
            documents.append(chunk)
            metadatas.append({'file_name': document.file_name})
            ids.append(str(id_counter))
            id_counter += 1

    collection.add(documents=documents, metadatas=metadatas, ids=ids)



def generate_langchain_vectorstore(documents, embedding_model= SentenceTransformerEmbeddings(model_name="all-mpnet-base-v2") , directory = "vectorstore"):
    """This function receives a list of documents, and returns a vectorstore"""
    #if os.path.exists('vectorstore'):
    #    shutil.rmtree('vectorstore')

    texts = [chunk for doc in documents for chunk in doc.chunks]
    metadatas = [{'file_name': doc.file_name} for doc in documents for _ in doc.chunks]
    vector_store = Chroma.from_texts(texts=texts, embedding=embedding_model, metadatas=metadatas, persist_directory="vectorstore")
    return vector_store


def add_document_to_vectordatabase(documents, vector_store):
    """This function receives a list of documents and an existiing vector_store, and returns the vector_store addedd with the document information."""

    texts = [chunk for doc in documents for chunk in doc.chunks]
    metadatas = [{'file_name': doc.file_name} for doc in documents for _ in doc.chunks]
    vector_store.add_texts(texts=texts, metadatas=metadatas)
    return vector_store