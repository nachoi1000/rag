from langchain.text_splitter import RecursiveCharacterTextSplitter

def generate_chunks(txt_files, chunk_size = 1000, chunk_overlap_size = 200):
    """This function receives a list of string and returns a a list of string's chunks based on chunk_size and chunk_overlap_size parameters"""
    
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = chunk_size,
        chunk_overlap = chunk_overlap_size)
        #separators = ["\n\n", "\n", "(?<=\. )", " ", ""])
    
    chunks = text_splitter.split_text(txt_files)
    chunks = [chunk.replace("\n"," ") for chunk in chunks]
    return chunks
