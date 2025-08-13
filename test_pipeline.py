#!/usr/bin/env python3
"""
Simple test script to verify the summarization pipeline works correctly.
"""

import os
import sys
from dotenv import load_dotenv

# Add src to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Load environment variables
load_dotenv()

def test_direct_text():
    """Test summarization with direct text input"""
    print("Testing direct text summarization...")
    
    # Import after adding src to path
    from pipeline import summarize_content
    
    sample_text = """
    Artificial intelligence (AI) is a branch of computer science that aims to create 
    software or machines that exhibit human-like intelligence. This can include 
    learning from experience, understanding natural language, solving problems, 
    and recognizing patterns. AI has numerous applications in fields such as 
    healthcare, finance, transportation, and entertainment. Machine learning, 
    a subset of AI, uses statistical techniques to enable machines to improve 
    at tasks with experience. Deep learning, a further subset of machine learning, 
    is based on artificial neural networks and is particularly effective for 
    image and speech recognition.
    """
    
    try:
        summary = summarize_content(
            input_type="text",
            content=sample_text,
            chunk_size=500,
            chunk_overlap=50
        )
        print("Summary:")
        print(summary)
        print("\nTest completed successfully!")
        return True
    except Exception as e:
        print(f"Error during test: {str(e)}")
        return False

if __name__ == "__main__":
    # Check if API key is set
    if not os.getenv("OPENROUTER_API_KEY"):
        print("Error: OPENROUTER_API_KEY environment variable is not set")
        print("Please set it in your .env file to run the test")
        sys.exit(1)
    
    success = test_direct_text()
    if not success:
        sys.exit(1)