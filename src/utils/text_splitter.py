"""
Text splitting utility for dividing large documents into chunks.
"""

from typing import List, Dict, Any
from langchain_text_splitters import SentenceTransformersTokenTextSplitter
from langchain_core.documents import Document


def split_text(state: Any) -> Dict[str, Any]:
    """
    Split documents into chunks based on configured size and overlap.
    
    Args:
        state: The current state containing documents, chunk_size, and chunk_overlap
        
    Returns:
        Updated state with text chunks
    """
    # Access attributes using dot notation for Pydantic models
    documents = state.documents
    chunk_size = state.chunk_size
    chunk_overlap = state.chunk_overlap
    
    # Initialize sentence-based text splitter
    text_splitter = SentenceTransformersTokenTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )
    
    # Split documents into chunks
    chunks = text_splitter.split_documents(documents)
    
    # Return updated state
    return {"chunks": chunks}