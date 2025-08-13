"""
Text splitting utility for dividing large documents into chunks.
"""

from typing import List, Dict, Any
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document


def split_text(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Split documents into chunks based on configured size and overlap.
    
    Args:
        state: The current state containing documents, chunk_size, and chunk_overlap
        
    Returns:
        Updated state with text chunks
    """
    documents = state["documents"]
    chunk_size = state["chunk_size"]
    chunk_overlap = state["chunk_overlap"]
    
    # Initialize text splitter
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
    )
    
    # Split documents into chunks
    chunks = text_splitter.split_documents(documents)
    
    # Update state with chunks
    state["chunks"] = chunks
    return state