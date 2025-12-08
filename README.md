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

## 🚀 Setup and Installation

### 1. Clone the Repository

```bash
git clone <your-repository-url>
cd news-research-tool-project
