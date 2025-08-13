"""
Summarization node for processing text chunks.
"""

import os
from typing import List, Dict, Any
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain_core.documents import Document


def summarize_chunks(state: Any) -> Dict[str, Any]:
    """
    Summarize text chunks using an LLM.
    
    Args:
        state: The current state containing chunks to summarize
        
    Returns:
        Updated state with chunk summaries
    """
    # Access attributes using dot notation for Pydantic models
    chunks = state.chunks
    
    # Initialize LLM with low temperature for consistent, factual summaries
    llm = ChatOpenAI(
        model=os.getenv("LLM_MODEL", "meta-llama/llama-3.1-8b-instruct:free"),
        openai_api_key=os.getenv("OPENROUTER_API_KEY"),
        openai_api_base=os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1"),
        temperature=0.0  # Low temperature for factual consistency
    )
    
    # Create improved prompt template for summarization - explicitly requesting concise summaries
    prompt_template = PromptTemplate.from_template(
        "You are a precise summarization assistant. Your task is to create a very concise, accurate summary of the provided text while preserving key information and main points.\n\n"
        "Text to summarize:\n{chunk_text}\n\n"
        "Please provide a clear, factual summary in exactly 1-2 sentences. Focus only on the most essential information. Keep it as brief as possible while maintaining clarity.\n\n"
        "Concise Summary:"
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
    
    # Return updated state
    return {"summaries": summaries}