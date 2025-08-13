"""
Summarization node for processing text chunks.
"""

import os
from typing import List, Dict, Any
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain_core.documents import Document


def summarize_chunks(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Summarize text chunks using an LLM.
    
    Args:
        state: The current state containing chunks to summarize
        
    Returns:
        Updated state with chunk summaries
    """
    chunks = state["chunks"]
    
    # Initialize LLM
    llm = ChatOpenAI(
        model=os.getenv("LLM_MODEL", "meta-llama/llama-3.1-8b-instruct:free"),
        openai_api_key=os.getenv("OPENROUTER_API_KEY"),
        openai_api_base=os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1"),
        temperature=0.0
    )
    
    # Create prompt template for summarization
    prompt_template = PromptTemplate.from_template(
        "Please provide a concise summary of the following text:\n\n{chunk_text}\n\nSummary:"
    )
    
    summaries = []
    
    # Process each chunk
    for chunk in chunks:
        # Format prompt with chunk content
        prompt = prompt_template.format(chunk_text=chunk.page_content)
        
        # Get summary from LLM
        response = llm.invoke(prompt)
        summary = response.content.strip()
        summaries.append(summary)
    
    # Update state with summaries
    state["summaries"] = summaries
    return state