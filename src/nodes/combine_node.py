"""
Summary combination node for merging multiple summaries into a cohesive final summary.
"""

import os
from typing import List, Dict, Any
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate


def combine_summaries(state: Any) -> Dict[str, Any]:
    """
    Combine multiple summaries into a single coherent summary.
    
    Args:
        state: The current state containing summaries to combine
        
    Returns:
        Updated state with final summary
    """
    # Access attributes using dot notation for Pydantic models
    summaries = state.summaries
    
    # If there's only one summary, return it as is
    if len(summaries) <= 1:
        return {"final_summary": summaries[0] if summaries else ""}
    
    # Initialize LLM with low temperature for consistent, factual summaries
    llm = ChatOpenAI(
        model=os.getenv("LLM_MODEL", "meta-llama/llama-3.1-8b-instruct:free"),
        openai_api_key=os.getenv("OPENROUTER_API_KEY"),
        openai_api_base=os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1"),
        temperature=0.0  # Low temperature for factual consistency
    )
    
    # Create improved prompt template for combining summaries
    summaries_text = "\n\n".join([f"- {summary}" for summary in summaries])
    
    prompt_template = PromptTemplate.from_template(
        "You are a skilled editor tasked with combining multiple summaries into a single, coherent, and comprehensive summary.\n\n"
        "Individual summaries:\n{summaries}\n\n"
        "Please synthesize these summaries into one well-structured summary that captures all essential information. "
        "Remove redundancies, maintain logical flow, and ensure the result reads as a unified piece of text rather than a list of separate points.\n\n"
        "Combined Summary:"
    )
    
    # Format prompt with summaries
    prompt = prompt_template.format(summaries=summaries_text)
    
    # Get combined summary from LLM
    response = llm.invoke(prompt)
    final_summary = response.content.strip()
    
    # Return updated state
    return {"final_summary": final_summary}