#!/usr/bin/env python3
"""
Web server for the LangGraph Content Summarizer.
This script starts the Streamlit web interface for summarizing content from various sources.
"""

import os
import sys
import subprocess

# Add the src directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '.'))

def start_streamlit():
    """Start the Streamlit app"""
    # Get the directory of this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    app_path = os.path.join(script_dir, 'streamlit_app.py')
    
    # Start Streamlit app
    process = subprocess.Popen([
        sys.executable, '-m', 'streamlit', 'run', 
        app_path, '--server.port=8501', 
        '--server.headless=true',
        '--server.runOnSave=false'
    ])
    
    return process

def start_web_app():
    """Start the web application"""
    print("Starting Streamlit server...")
    streamlit_process = start_streamlit()
    
    print("Streamlit server started!")
    print("Access the app at: http://localhost:8501")
    
    # Wait for the process to complete
    streamlit_process.wait()

if __name__ == '__main__':
    start_web_app()