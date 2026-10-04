# 🤖 AI Knowledge Assistant

An intelligent Retrieval-Augmented Generation (RAG) application built using **LangChain**, **Ollama**, **ChromaDB**, **HuggingFace Embeddings**, and **Streamlit**. The assistant allows users to upload PDFs, ingest website content, and chat with their own knowledge base through a conversational AI interface.

### 🌐 Live Demo

**AI Knowledge Assistant:**
https://ai-knowledge-assistant-7.streamlit.app/

---

# 🚀 Features

* 💬 ChatGPT-style conversational interface
* 📄 Upload and chat with PDF documents
* 🌐 Extract and query website content using URLs
* 🧠 Retrieval-Augmented Generation (RAG)
* 🔍 Semantic search powered by vector embeddings
* 🗂️ ChromaDB vector database integration
* 🤗 HuggingFace Embeddings
* 🦙 Local LLM inference using Ollama
* 📝 Context-aware conversation memory
* ✂️ Automatic chat history trimming
* ⚡ Fast and lightweight Streamlit UI

---

# 🛠️ Tech Stack

## Frontend

* Streamlit

## AI & LLM

* Ollama
* Llama 3 (8B)

## Framework

* LangChain

## Embeddings

* sentence-transformers/all-MiniLM-L6-v2

## Vector Database

* ChromaDB

## Document Processing

* PyPDFLoader
* WebBaseLoader

## Memory Management

* RunnableWithMessageHistory
* ChatMessageHistory

---

# 📂 Project Structure

```text
AI-Knowledge-Assistant/
│
├── app.py
├── README.md
│
├── data/
├── chroma_db/
│
├── assets/
│   ├── screenshot1.png
│   └── screenshot2.png
│
└── utils/
```

---

# ⚙️ Installation

## 1. Clone Repository

```bash
git clone https://github.com/maherdhami/AI-Knowledge-Assistant.git
cd AI-Knowledge-Assistant
```

## 2. Create Virtual Environment

```bash
python -m venv venv
```

### Windows

```bash
venv\Scripts\activate
```

### Linux / macOS

```bash
source venv/bin/activate
```

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

## 4. Install Ollama

Download and install Ollama:

https://ollama.com

Pull the Llama 3 model:

```bash
ollama pull llama3:8b
```

## 5. Configure Environment Variables

Create a `.env` file in the project root:

```env
LANGCHAIN_API_KEY=your_langsmith_key
LANGCHAIN_PROJECT=AI-Knowledge-Assistant
LANGCHAIN_TRACING_V2=true
HF_TOKEN=your_huggingface_token
```

---

# ▶️ Running the Application

```bash
streamlit run app.py
```

Application will be available at:

```text
http://localhost:8501
```

---

# 🧠 How It Works

## Step 1: Knowledge Ingestion

Users can provide:

* PDF Documents
* Website URLs

## Step 2: Document Processing

The system:

1. Loads documents
2. Splits them into chunks
3. Generates embeddings using HuggingFace

## Step 3: Vector Storage

Embeddings are stored inside:

```text
ChromaDB
```

## Step 4: Retrieval & Generation

When a user asks a question:

```text
User Query
      │
      ▼
Retriever
      │
      ▼
Relevant Context
      │
      ▼
Prompt Construction
      │
      ▼
Llama 3
      │
      ▼
AI Response
```

## Step 5: Conversational Memory

Chat history is maintained using LangChain memory components, enabling context-aware multi-turn conversations.

---

# 🔍 RAG Architecture

```text
PDFs / Websites
        │
        ▼
Document Loaders
        │
        ▼
Text Splitter
        │
        ▼
HuggingFace Embeddings
        │
        ▼
ChromaDB
        │
        ▼
Retriever
        │
        ▼
Prompt Template
        │
        ▼
Llama 3 (Ollama)
        │
        ▼
Final Response
```

---

# 📸 Application Screenshots

## Home Screen

```text
assets/screenshot1.png
```

## Chat Interface

```text
assets/screenshot2.png
```

---

# 📦 Requirements

```txt
streamlit
langchain
langchain-community
langchain-core
langchain-text-splitters
langchain-huggingface
langchain-chroma
langchain-ollama
chromadb
sentence-transformers
pypdf
beautifulsoup4
python-dotenv
```

---

# 🎯 Skills Demonstrated

* Retrieval-Augmented Generation (RAG)
* Generative AI Applications
* LangChain Framework
* LLM Integration
* Prompt Engineering
* Semantic Search
* Vector Databases
* Embedding Models
* Conversational AI
* Memory Management
* Streamlit Development
* Local AI Deployment
* Document Question Answering Systems

---

# 🔮 Future Enhancements

* Real-time streaming responses
* Multiple LLM support
* Chat export functionality
* Persistent vector storage
* LangGraph-based memory
* User authentication
* Multi-user architecture
* Source citations
* Hybrid search (Keyword + Vector)
* DOCX and image support
* Cloud deployment options

---

# 👨‍💻 Author

**Maher Dhami**

GitHub: https://github.com/maherdhami

LinkedIn: https://www.linkedin.com/in/maher-dhami-a15197225/

---

# ⭐ Support

If you found this project valuable:

* ⭐ Star the repository
* 🍴 Fork the repository
* 🚀 Share it with others

---

# 📜 License

This project is licensed under the **MIT License**.
