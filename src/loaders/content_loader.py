"""
Content loaders for different source types.
"""

from typing import List, Dict, Any
import requests
from langchain_community.document_loaders import WebBaseLoader, PyPDFLoader, TextLoader
from langchain_core.documents import Document


def load_content(state: Any) -> Dict[str, Any]:
    """
    Load content based on the input type.
    
    Args:
        state: The current state containing input_type and content
        
    Returns:
        Updated state with loaded documents
    """
    # Access attributes using dot notation for Pydantic models
    input_type = state.input_type
    content = state.content
    
    documents = []
    
    try:
        if input_type == "url":
            # Load content from a web URL
            loader = WebBaseLoader(content)
            documents = loader.load()
        elif input_type == "pdf":
            # Load content from a PDF file
            loader = PyPDFLoader(content)
            documents = loader.load()
        elif input_type == "textfile":
            # Load content from a text file
            loader = TextLoader(content)
            documents = loader.load()
        elif input_type == "text":
            # Wrap direct text in a Document
            documents = [Document(page_content=content)]
        else:
            raise ValueError(f"Unsupported input type: {input_type}")
    except Exception as e:
        raise Exception(f"Failed to load content: {str(e)}")
    
    # Return updated state
    return {"documents": documents}