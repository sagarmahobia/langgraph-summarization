"""
Summary combination node for merging multiple summaries into a cohesive final summary.
"""

import os
from typing import List, Dict, Any
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate


def combine_summaries(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Combine multiple summaries into a single coherent summary.
    
    Args:
        state: The current state containing summaries to combine
        
    Returns:
        Updated state with final summary
    """
    summaries = state["summaries"]
    
    # If there's only one summary, return it as is
    if len(summaries) <= 1:
        state["final_summary"] = summaries[0] if summaries else ""
        return state
    
    # Initialize LLM
    llm = ChatOpenAI(
        model=os.getenv("LLM_MODEL", "meta-llama/llama-3.1-8b-instruct:free"),
        openai_api_key=os.getenv("OPENROUTER_API_KEY"),
        openai_api_base=os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1"),
        temperature=0.0
    )
    
    # Create prompt template for combining summaries
    summaries_text = "\n\n".join([f"- {summary}" for summary in summaries])
    
    prompt_template = PromptTemplate.from_template(
        "Please combine the following summaries into a single coherent summary:\n\n{summaries}\n\nFinal Summary:"
    )
    
    # Format prompt with summaries
    prompt = prompt_template.format(summaries=summaries_text)
    
    # Get combined summary from LLM
    response = llm.invoke(prompt)
    final_summary = response.content.strip()
    
    # Update state with final summary
    state["final_summary"] = final_summary
    return state