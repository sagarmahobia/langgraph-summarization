# Architecture Overview

This document outlines the high-level architecture of the LangGraph Content Summarizer.

## Core Components

1.  **Input Handler:**
    *   **Purpose:** Determines the type of input source (URL, PDF, Text File, Direct Text).
    *   **Logic:** Routes the input to the appropriate loader based on its type.

2.  **Abstract Loader:**
    *   **Purpose:** Provides a unified interface for loading content from diverse sources.
    *   **Implementations:**
        *   `WebLoader`: Fetches and parses HTML content from a URL.
        *   `PDFLoader`: Extracts text from PDF documents.
        *   `TextFileLoader`: Reads plain text files.
        *   `DirectTextLoader`: Wraps raw text input into a document format.
    *   **Output:** Produces a standardized `Document` object (or list of `Document` objects) containing the text and potentially metadata.

3.  **Text Splitter:**
    *   **Purpose:** Segments large documents into smaller chunks to fit within the LLM's context window.
    *   **Configuration:** Chunk size and overlap are configurable (e.g., via environment variables).
    *   **Output:** A list of `Document` chunks.

4.  **LLM Manager:**
    *   **Purpose:** Manages the connection and interaction with the LLM via the OpenRouter API.
    *   **Configuration:** Reads `OPENROUTER_API_KEY`, `OPENROUTER_BASE_URL`, and `LLM_MODEL` from environment variables.
    *   **Wrapper:** Utilizes a LangChain LLM wrapper (e.g., `ChatOpenAI`) configured for OpenRouter compatibility.

5.  **Summarization Nodes (LangGraph):**
    *   **`Summarize_Chunks_Node`:**
        *   **Input:** List of `Document` chunks.
        *   **Process:** Iterates through chunks, sends each to the LLM via the `LLM Manager` with a summarization prompt.
        *   **Output:** List of individual chunk summaries.
    *   **`Combine_Summaries_Node`:**
        *   **Input:** List of chunk summaries.
        *   **Process:** If multiple summaries exist, sends them to the LLM via the `LLM Manager` with a prompt to combine them into a single, coherent summary.
        *   **Output:** Final combined summary.
    *   **`Output_Node`:**
        *   **Input:** Final summary string.
        *   **Process:** Returns the summary to the caller or handles further output (e.g., printing, saving to file).

6.  **LangGraph Orchestrator:**
    *   **Purpose:** Defines the workflow graph, managing the state and transitions between the `Input Handler`, `Abstract Loader`, `Text Splitter`, `Summarization Nodes`, and `Output_Node`.
    *   **State:** Maintains the `Document` objects, list of summaries, and the final summary as it flows through the pipeline.

## Data Flow

1.  **Input:** User provides source type and identifier.
2.  **Routing:** `Input Handler` directs to the correct loader.
3.  **Loading:** `Abstract Loader` fetches and parses content into `Document`(s).
4.  **Chunking:** `Text Splitter` processes `Document`(s) into manageable chunks.
5.  **Chunk Summarization:** `Summarize_Chunks_Node` uses `LLM Manager` to summarize each chunk.
6.  **Summary Combination:** `Combine_Summaries_Node` uses `LLM Manager` to merge chunk summaries (if necessary).
7.  **Output:** `Output_Node` delivers the final summary.

## Diagram (Conceptual)

```
+-----------------+
|  Input Handler  |
+-----------------+
          |
          v
+------------------+       +------------------+
| Abstract Loader  |------>|  Text Splitter   |
+------------------+       +------------------+
                                    |
                                    v
+------------------+       +---------------------------+
|  LLM Manager     |<------| Summarize Chunks Node     |
+------------------+       +---------------------------+
          ^                            |
          |                            v
          |              +---------------------------+
          |              | Combine Summaries Node    |
          |              +---------------------------+
          |                            |
          |                            v
          |              +------------------+
          +------------->|   Output Node    |
                         +------------------+

                                |
                                v
                         +-------------+
                         |    User     |
                         +-------------+
```

## Technologies

*   **Python:** Primary programming language.
*   **LangGraph:** Core framework for defining and executing the workflow graph.
*   **LangChain:** Provides `Document` abstractions, text splitters, and LLM wrappers.
*   **Loaders:** `langchain_community.document_loaders` (Web, PDF, Text).
*   **OpenRouter API:** Interface for accessing various LLMs.