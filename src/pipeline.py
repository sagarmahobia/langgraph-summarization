"""
LangGraph pipeline for content summarization.
This module defines the workflow graph and manages the state transitions between nodes.
"""

import asyncio
from typing import List, Dict, Any, Optional
from langgraph.graph import StateGraph, END
from pydantic import BaseModel, Field

from src.loaders import load_content
from src.utils.text_splitter import split_text
from src.nodes.summarize_node import summarize_chunks
from src.nodes.combine_node import combine_summaries


class State(BaseModel):
    """State model for the LangGraph pipeline"""
    input_type: str
    content: str
    chunk_size: int
    chunk_overlap: int
    documents: List[Any] = Field(default_factory=list)
    chunks: List[Any] = Field(default_factory=list)
    summaries: List[str] = Field(default_factory=list)
    final_summary: str = ""


def route_after_summarizing(state: State) -> str:
    """Route after chunk summarization"""
    # If we have multiple summaries, combine them
    if len(state.summaries) > 1:
        return "combiner"
    else:
        # If we have only one summary, it's our final summary
        return "output"


def create_workflow():
    """Create and configure the LangGraph workflow"""
    # Define a LangGraph state machine
    workflow = StateGraph(State)
    
    # Add nodes
    workflow.add_node("loader", load_content)
    workflow.add_node("splitter", split_text)
    workflow.add_node("summarizer", summarize_chunks)
    workflow.add_node("combiner", combine_summaries)
    workflow.add_node("output", lambda state: {"final_summary": state.get("final_summary", "")})
    
    # Add edges - simplified using direct string values
    workflow.add_edge("loader", "splitter")
    workflow.add_edge("splitter", "summarizer")
    
    workflow.add_conditional_edges(
        "summarizer",
        route_after_summarizing,
        {
            "combiner": "combiner",
            "output": "output"
        }
    )
    
    workflow.add_edge("combiner", "output")
    workflow.add_edge("output", END)
    
    # Set entry point
    workflow.set_entry_point("loader")
    
    return workflow


async def summarize_content(
    input_type: str,
    content: str,
    chunk_size: int = 1000,
    chunk_overlap: int = 100
) -> str:
    """
    Summarize content using the LangGraph pipeline.
    
    Args:
        input_type: Type of input ('url', 'pdf', 'textfile', 'text')
        content: The actual content (URL, file path, or text)
        chunk_size: Size of text chunks
        chunk_overlap: Overlap between chunks
        
    Returns:
        The final summary as a string
    """
    # Create the workflow
    workflow = create_workflow()
    app = workflow.compile()
    
    # Initialize state
    initial_state = State(
        input_type=input_type,
        content=content,
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
    
    # Run the workflow
    final_state = await app.ainvoke(initial_state.dict())
    
    return final_state["final_summary"]