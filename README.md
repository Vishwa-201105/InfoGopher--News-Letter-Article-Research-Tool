# 📰 InfoGopher — AI-Powered News Research Assistant

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python"/>
  <img src="https://img.shields.io/badge/LangChain-RAG-green?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/Google-Gemini-orange?style=for-the-badge&logo=google"/>
  <img src="https://img.shields.io/badge/ChromaDB-Vector%20Database-purple?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/Streamlit-Web%20App-red?style=for-the-badge&logo=streamlit"/>
</p>

---

## 📌 Overview

**InfoGopher** is an AI-powered research assistant that enables users to analyze multiple online news articles using **Retrieval-Augmented Generation (RAG)**.

Instead of searching manually through lengthy articles, users simply provide article URLs and ask questions in natural language. The application retrieves only the most relevant information from indexed articles and generates context-aware answers using Google's **Gemini** models.

Built with **LangChain**, **ChromaDB**, **Gemini**, and **Streamlit**, InfoGopher demonstrates an end-to-end implementation of a modern RAG pipeline.

---

## ✨ Features

- 🔗 Index multiple news article URLs
- 🤖 Retrieval-Augmented Generation (RAG)
- 🧠 Gemini 2.5 Flash for contextual question answering
- 📚 ChromaDB vector database for semantic retrieval
- 🔍 Google Gemini Embeddings for document indexing
- 💬 Persistent multi-session chat history
- 🏷 Automatic chat title generation
- 📄 Source citation for every response
- ⚡ Fast semantic search over indexed documents
- 🎨 Interactive Streamlit interface

---

## 🛠️ Tech Stack

| Category | Technologies |
|-----------|--------------|
| Language | Python |
| LLM | Google Gemini 2.5 Flash |
| Embeddings | Gemini text-embedding-004 |
| Framework | LangChain |
| Vector Database | ChromaDB |
| Frontend | Streamlit |
| Web Scraping | Selenium |
| Document Loading | UnstructuredURLLoader |
| Environment | dotenv |

---

## 🏗️ System Architecture

```
User URLs
      │
      ▼
Article Loader
      │
      ▼
Text Processing
      │
      ▼
Gemini Embeddings
      │
      ▼
ChromaDB Vector Store
      │
      ▼
User Question
      │
      ▼
Similarity Search
      │
      ▼
Relevant Chunks
      │
      ▼
Gemini 2.5 Flash
      │
      ▼
AI Response + Source References
```

---

## 🚀 Key Features Explained

### 🔍 Article Indexing

Users can provide multiple news article URLs.

The application:

- Extracts webpage content
- Cleans and processes text
- Generates semantic embeddings
- Stores vectors inside ChromaDB

---

### 💡 Intelligent Question Answering

Rather than relying on general LLM knowledge, InfoGopher retrieves only the relevant document chunks before generating a response.

This significantly reduces hallucinations while improving factual accuracy.

---

### 💬 Persistent Chat Sessions

Each conversation is automatically saved.

Features include:

- Multiple chat sessions
- Automatic chat naming
- Session switching
- Conversation persistence

---

### 📚 Source Attribution

Every generated answer includes the source article(s) used for retrieval, allowing users to verify information easily.

---

## 📂 Project Structure

```
InfoGopher/
│
├── app.py
├── requirements.txt
├── chroma_db/
├── chat_history/
├── utils/
├── assets/
├── .env
└── README.md
```

*(Adjust the structure if your repository differs.)*

---

## 📸 Application Preview

### Home Page

<img width="1433" alt="InfoGopher Screenshot" src="https://github.com/user-attachments/assets/cbab4a17-3cb6-4360-9f94-6bb44bd276d5"/>

---

## ⚙️ Installation

### Clone Repository

```bash
git clone https://github.com/Vishwa-201105/InfoGopher--News-Letter-Article-Research-Tool.git

cd InfoGopher--News-Letter-Article-Research-Tool
```

### Create Virtual Environment

```bash
python -m venv venv
```

Activate:

Windows

```bash
venv\Scripts\activate
```

Mac/Linux

```bash
source venv/bin/activate
```

---

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

### Configure Environment Variables

Create a `.env` file.

```env
GOOGLE_API_KEY=YOUR_GEMINI_API_KEY
```

---

### Run the Application

```bash
streamlit run app.py
```

---

## 📖 How It Works

1. Enter one or more news article URLs.
2. The articles are scraped and processed.
3. Text is converted into vector embeddings.
4. Embeddings are stored in ChromaDB.
5. Ask any question about the indexed articles.
6. Relevant document chunks are retrieved.
7. Gemini generates an answer grounded in the retrieved context.

---

## 🎯 Example Questions

- Summarize all uploaded articles.
- Compare viewpoints across different news sources.
- What caused the stock market decline?
- Which company announced the acquisition?
- What are the major takeaways?
- What statistics are mentioned?

---

## ⚠️ Current Limitations

- Dynamic websites with heavy JavaScript rendering may not always scrape successfully.
- Performance depends on the quality of retrieved document chunks.
- Free Gemini API quotas may limit large-scale usage.
- Extremely long documents may require chunking optimizations.

---

## 🚀 Future Improvements

- 🌐 Support PDF and DOCX ingestion
- 🎥 Support YouTube transcript analysis
- 🖼 Multi-modal RAG with image understanding
- 🌍 Web search agent integration
- 🧠 Multi-agent research workflow using LangGraph
- ☁ Deploy with Docker and cloud databases
- 📊 Conversation analytics dashboard
- 🔐 User authentication and cloud chat history

---

## 🤝 Contributing

Contributions are welcome.

1. Fork the repository.
2. Create a feature branch.
3. Commit your changes.
4. Open a Pull Request.

---

## 👨‍💻 Author

**Vishwa S**

GitHub: https://github.com/Vishwa-201105

---

## ⭐ Show Your Support

If you found this project useful, consider giving it a **⭐ Star** on GitHub.

---

## 📄 License

This project is intended for educational, research, and portfolio purposes.

Feel free to fork and build upon it with proper attribution.
