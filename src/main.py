#!/usr/bin/env python3
"""
Main entry point for the LangGraph Content Summarizer.
This script handles command-line arguments and orchestrates the summarization process.
"""

import argparse
import os
import sys
from typing import Optional

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def main():
    parser = argparse.ArgumentParser(
        description="Summarize content from various sources using LangGraph and LLMs via OpenRouter API"
    )
    
    # Define mutually exclusive input group
    input_group = parser.add_mutually_exclusive_group(required=True)
    
    input_group.add_argument(
        "--url",
        type=str,
        help="URL of the web page to summarize"
    )
    
    input_group.add_argument(
        "--pdf",
        type=str,
        help="Path to the PDF file to summarize"
    )
    
    input_group.add_argument(
        "--textfile",
        type=str,
        help="Path to the text file to summarize"
    )
    
    input_group.add_argument(
        "--text",
        type=str,
        help="Direct text content to summarize"
    )
    
    # Optional arguments
    parser.add_argument(
        "--chunk-size",
        type=int,
        default=None,
        help="Override chunk size (default: use CHUNK_SIZE env var or 1000)"
    )
    
    parser.add_argument(
        "--chunk-overlap",
        type=int,
        default=None,
        help="Override chunk overlap (default: use CHUNK_OVERLAP env var or 100)"
    )
    
    args = parser.parse_args()
    
    # Validate environment variables
    api_key = os.getenv("OPENROUTER_API_KEY")
    base_url = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")
    model = os.getenv("LLM_MODEL", "meta-llama/llama-3.1-8b-instruct:free")
    
    if not api_key:
        print("Error: OPENROUTER_API_KEY environment variable is required", file=sys.stderr)
        print("Please set it in your .env file or environment", file=sys.stderr)
        sys.exit(1)
    
    # Determine input type and content
    input_type = None
    content = None
    
    if args.url:
        input_type = "url"
        content = args.url
    elif args.pdf:
        input_type = "pdf"
        content = args.pdf
        # Validate file exists
        if not os.path.exists(content):
            print(f"Error: PDF file '{content}' not found", file=sys.stderr)
            sys.exit(1)
    elif args.textfile:
        input_type = "textfile"
        content = args.textfile
        # Validate file exists
        if not os.path.exists(content):
            print(f"Error: Text file '{content}' not found", file=sys.stderr)
            sys.exit(1)
    elif args.text:
        input_type = "text"
        content = args.text
    
    # Get chunking configuration
    chunk_size = args.chunk_size or int(os.getenv("CHUNK_SIZE", "1000"))
    chunk_overlap = args.chunk_overlap or int(os.getenv("CHUNK_OVERLAP", "100"))
    
    # Import here to avoid issues with env vars
    try:
        from src.pipeline import summarize_content
        summary = summarize_content(
            input_type=input_type,
            content=content,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )
        print(summary)
    except Exception as e:
        print(f"Error during summarization: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()