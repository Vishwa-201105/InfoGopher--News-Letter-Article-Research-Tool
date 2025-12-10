# 🔎 InfoGopher: AI-Powered News Research Tool

InfoGopher is a Streamlit application designed to perform **Retrieval-Augmented Generation (RAG)** on web articles. It allows users to input multiple news URLs, index their content using **Gemini Embeddings**, and then ask complex, contextual questions based *only* on the indexed articles. It features a persistent, multi-session chat history with dynamic, automatic chat naming.

## ✨ Features

* **Article Indexing:** Fetches content from multiple URLs (using Selenium) and indexes it into a persistent ChromaDB vector store.
* **Gemini RAG Pipeline:** Uses the **`gemini-2.5-flash`** model for generating contextual answers and the **`text-embedding-004`** model for creating embeddings.
* **Persistent Chat History:** Saves conversation history across sessions and allows switching between different chats in the sidebar.
* **Dynamic Chat Naming:** Automatically names new chat sessions based on the user's first question for easy organization.
* **Source Citation:** Links the answer back to the specific source URLs used from the indexed articles.
* **Robust Persistence:** Employs a unique directory naming strategy to manage ChromaDB persistence, effectively preventing common "readonly database" errors in Streamlit environments.

## 🛠️ Prerequisites

Before running the application, ensure you have the following installed:

1.  **Python 3.9+**
2.  **A Gemini API Key**

## Image sample of website:
<img width="1433" height="667" alt="Screenshot 2025-12-09 at 11 32 49 PM" src="https://github.com/user-attachments/assets/cbab4a17-3cb6-4360-9f94-6bb44bd276d5" />

## Limitations:
1. **Web Scraping Reliability:** The data loading relies on the pure-Python UnstructuredURLLoader, which struggles with highly dynamic, JavaScript-rendered websites (like those with infinite scrolling or content loaded post-click). The system may fail to capture all content from such sources.

2. **Context Window Size & Specificity:** The current RAG pipeline uses a fixed context window and retrieval count, which can sometimes lead to over-contextualization (irrelevant data retrieved) or under-contextualization (key details missed) for very long articles or highly specific queries.

3. **Cost/Rate Limits:** While deployment issues were solved, the application's cost is tied directly to the Gemini API usage. High query volume can quickly exceed free-tier quotas, necessitating migration to a paid tier for reliable, scaled production use.

## Future Scope:
1. **Advanced Web Scraping Agent:** Integrate a dedicated, robust scraping service (e.g., using a Headless Browser like Playwright/Selenium via a proxy service or a specialized API) to handle JavaScript rendering and bypass common anti-scraping techniques (IP blocks, CAPTCHAs).

2. **Modular Architecture and Agents:** Refactor the current single-chain architecture into a modular design. Introduce LangChain Agents to dynamically select the best action—either querying the vector store or using a separate tool (like Google Search) for general knowledge—to improve query accuracy and efficiency.

3. **Multi-Modal and Multi-Source Support:** Extend the ingestion pipeline to handle non-text inputs like PDFs and image metadata. Introduce a feature allowing the user to filter search results by source URL or date within the ChromaDB retriever for more precise answers.


## 🚀 Setup and Installation

### 1. Clone the Repository

```bash
git clone <https://github.com/Vishwa-201105/InfoGopher--News-Letter-Article-Research-Tool>
cd news-research-tool-project
