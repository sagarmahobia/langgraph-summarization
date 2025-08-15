# LangGraph Content Summarizer

This project implements a flexible content summarization pipeline using LangGraph. It can summarize text from various sources including web URLs, PDF files, text files, and direct text input. It leverages Large Language Models (LLMs) accessed through the OpenRouter API.

This project is a demonstration of "Vibe Coding" and showcases how AI tools can be effectively integrated into a developer's day-to-day workflow for planning, designing, and documenting software.

## Features

*   **Multi-source Input:** Summarize content from web pages, PDFs, text files, or direct text strings.
*   **LangGraph Pipeline:** Robust and configurable workflow management.
*   **LLM Integration:** Uses LLMs via the OpenRouter API.
*   **Configurable LLM:** Easily switch LLMs by changing environment variables.
*   **Intelligent Chunking:** Automatically splits large documents into manageable chunks for processing.
*   **Consistent Output:** Uses low temperature settings (0.0) for factual, consistent summaries.

## Prerequisites

*   Python 3.9 or higher
*   An OpenRouter API key (sign up at [https://openrouter.ai/](https://openrouter.ai/))
*   `uv` package manager (install from [https://github.com/astral-sh/uv](https://github.com/astral-sh/uv))

## Installation

1.  **Clone the repository:**

    ```bash
    git clone <repository-url>
    cd langgraph-content-summarizer
    ```

2.  **Create a virtual environment with `uv` (recommended):**

    ```bash
    uv venv
    source .venv/bin/activate  # On Windows: .venv\Scripts\activate
    ```

3.  **Install dependencies using `uv`:**

    ```bash
    uv pip install -r requirements.txt
    ```

## Configuration

The application requires the following environment variables to be set. Create a `.env` file in the project root directory and add your configuration:

```env
# OpenRouter API Configuration
OPENROUTER_API_KEY=your_openrouter_api_key_here
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
LLM_MODEL=meta-llama/llama-3.1-8b-instruct:free

# Optional: Configure chunking behavior
# For sentence transformers, smaller chunks work better for concise summaries
CHUNK_SIZE=150
CHUNK_OVERLAP=15
```

Replace `your_openrouter_api_key_here` with your actual OpenRouter API key.

## Usage

Once configured, you can run the summarizer through either the command-line interface or the web application:

### Command-Line Interface

```bash
# Activate virtual environment if not already active
source .venv/bin/activate

# Run with a URL
python src/main.py --url "https://example.com/article"

# Run with a PDF file
python src/main.py --pdf "path/to/document.pdf"

# Run with a text file
python src/main.py --textfile "path/to/document.txt"

# Run with direct text
python src/main.py --text "Your text to summarize"

# Additional options for chunking and summary length
python src/main.py --url "https://example.com/article" --chunk-size 200 --chunk-overlap 20 --max-summary-length 3
```

### Web Application

```bash
# Activate virtual environment if not already active
source .venv/bin/activate

# Run the web app
python src/web_app.py
```

The web application provides a user-friendly UI with:
- Dropdown for selecting content type (URL, PDF, Text file, Direct text)
- Appropriate input fields for each content type
- File uploaders for PDF and text files (max 1MB)
- Configuration options
- Real-time processing status and results

Access the web application at: http://localhost:8501

Note: The web application uses Streamlit and runs in your browser.

## Sample Files

The repository includes sample files for testing:
- `samples/healthcare_ai.txt` - A text file about AI in healthcare
- `samples/drylab.pdf` - A PDF file (about a company newsletter)

## Project Structure

```
src/
├── main.py              # Entry point for the application
├── pipeline.py          # LangGraph workflow definition
├── loaders/             # Content loading modules
│   └── __init__.py      # Content loader implementation
├── nodes/               # LangGraph nodes
│   ├── summarize_node.py # Chunk summarization node
│   └── combine_node.py   # Summary combination node
├── utils/               # Utility functions
│   └── text_splitter.py  # Text splitting utility
```

## Testing

A simple test script is included to verify the pipeline works correctly:

```bash
# Run the test (requires OPENROUTER_API_KEY to be set)
python test_pipeline.py
```

## Contributing

Contributions are welcome! Here's how you can contribute:

1.  **Fork the repository** on GitHub.
2.  **Create a new branch** for your feature or bug fix:
    ```bash
    git checkout -b feature/your-feature-name
    # or
    git checkout -b bugfix/your-bug-fix
    ```
3.  **Make your changes** and ensure they adhere to the project's style and conventions.
4.  **Add or update tests** if applicable.
5.  **Commit your changes:**
    ```bash
    git commit -m "Add a brief description of your changes"
    ```
6.  **Push to your fork:**
    ```bash
    git push origin feature/your-feature-name
    ```
7.  **Open a Pull Request** on the original repository.

Please ensure your code is well-documented and tested before submitting a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.