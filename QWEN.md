# LangGraph Pipeline Plan for Content Summarization

## Objective
Create a flexible LangGraph pipeline capable of summarizing content from various sources (web URL, PDF, text file, direct text query) using an LLM accessed via the OpenRouter API. The LLM model, API key, and base URL are configured via environment variables.

## Pipeline Stages

1.  **Abstract Content Loading:**
    *   Input: Content source type (URL, PDF path, Text file path, Direct Text) and the corresponding identifier (e.g., the actual URL or file path).
    *   Action: Route to a specific loader based on the type:
        *   **URL:** Use `WebLoader` (e.g., from `langchain_community.document_loaders`) to fetch and parse the web page.
        *   **PDF File:** Use `PyPDFLoader` or similar to extract text from the PDF.
        *   **Text File:** Use `TextLoader` to read the file's content.
        *   **Direct Text:** Directly wrap the text into a `Document` object.
    *   Output: A standardized `Document` object (or list of `Document` objects) containing the extracted text and relevant metadata, regardless of the source type.

2.  **Chunk Text (if necessary):**
    *   Input: `Document` object(s) from the abstract loader.
    *   Action: Use a text splitter (e.g., from `langchain.text_splitter`) to divide potentially large text content into smaller, manageable chunks suitable for the LLM's context window. Overlapping chunks can improve coherence.
    *   Output: List of `Document` objects representing the text chunks.

3.  **Summarize Chunks:**
    *   Input: List of `Document` chunks (or a single `Document` if no splitting occurred).
    *   Action:
        1.  Initialize an LLM wrapper using LangChain's OpenAI-compatible interface.
        2.  Configure the LLM wrapper using environment variables:
            *   `OPENROUTER_API_KEY`: The API key for OpenRouter.
            *   `OPENROUTER_BASE_URL`: The base URL for the OpenRouter API (e.g., `https://openrouter.ai/api/v1`).
            *   `LLM_MODEL`: The specific model identifier to use (e.g., `meta-llama/llama-3.1-8b-instruct:free`).
        3.  For each chunk, call the configured LLM with a prompt instructing it to summarize the provided text concisely. This can be done using a `LLMChain` or direct LLM invocation.
    *   Output: List of chunk summaries (strings).

4.  **Combine Summaries (if multiple chunks):**
    *   Input: List of chunk summaries.
    *   Action:
        1.  Use the same LLM wrapper configured in the 'Summarize Chunks' stage.
        2.  If there were multiple chunks, combine their summaries. This involves another LLM call with a prompt asking it to synthesize the list of summaries into a single, coherent final summary.
    *   Output: Final combined summary (string).

5.  **Output Summary:**
    *   Input: Final summary string.
    *   Action: Return the summary to the user or pass it to the next component in a larger system.

## Tools & Libraries

*   **LangGraph:** Core framework for building the state machine/graph.
*   **Document Loaders:** `WebLoader`, `PyPDFLoader`, `TextLoader` from `langchain_community.document_loaders`.
*   **Text Splitting:** Utilities from `langchain.text_splitter`.
*   **LLM Integration:** LangChain's `ChatOpenAI` or equivalent OpenAI-compatible LLM wrapper.
*   **Environment Variables:** For `OPENROUTER_API_KEY`, `OPENROUTER_BASE_URL`, and `LLM_MODEL`.
*   **LangChain:** For LLM integration, chains, and utilities.
*   **Python:** Core language for implementation.
*   **uv:** Package manager for Python dependencies.

## Considerations

*   **Error Handling:** Handle errors from different loaders (network, file I/O), parsing errors, LLM call failures (including API quota issues), and missing environment variables gracefully.
*   **Async/Await:** Consider using asynchronous operations for LLM calls and potentially loaders if supported, to improve performance.
*   **State Management:** Use LangGraph's state management to pass `Document` objects and summaries between nodes.
*   **Prompt Engineering:** Carefully design prompts for the LLM to ensure good quality summaries at both the chunk and combination stages.
*   **Configurability:** Allow configuration for chunk size, overlap, and summary length via parameters or environment variables, while keeping the core LLM configuration in env vars.