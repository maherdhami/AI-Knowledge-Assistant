# AI-Knowledge-Assistant
A Streamlit-based AI Knowledge Assistant powered by LangChain, Ollama, ChromaDB and HuggingFace Embeddings. Upload PDFs, scrape websites and chat with your knowledge base using Retrieval-Augmented Generation (RAG).

# AI Knowledge Assistant 🤖

A Streamlit-based AI Knowledge Assistant powered by LangChain, Ollama, ChromaDB, and HuggingFace Embeddings. Upload PDFs, scrape websites, and chat with your knowledge base using Retrieval-Augmented Generation (RAG).

---

## 🚀 Features

- 💬 ChatGPT-like conversational interface
- 📄 Upload and query PDF documents
- 🌐 Ingest website content using URLs
- 🧠 Retrieval-Augmented Generation (RAG)
- 🔍 Semantic search with vector embeddings
- 🗂️ ChromaDB vector database
- 🤗 HuggingFace Embeddings
- 🦙 Local LLM inference using Ollama
- 📝 Conversation memory with LangChain
- ✂️ Automatic chat history trimming
- ⚡ Fast and lightweight Streamlit UI

---

## 🛠️ Tech Stack

### Frontend
- Streamlit

### LLM
- Ollama
- Llama 3 (8B)

### Framework
- LangChain

### Embeddings
- sentence-transformers/all-MiniLM-L6-v2

### Vector Database
- ChromaDB

### Document Loaders
- PyPDFLoader
- WebBaseLoader

### Memory
- RunnableWithMessageHistory
- ChatMessageHistory

---

## 📂 Project Structure

```text
AI-Knowledge-Assistant/
│
├── app.py
├── requirements.txt
├── README.md
├── .env
├── .env.example
│
├── data/
│
├── chroma_db/
│
├── assets/
│   ├── screenshot1.png
│   ├── screenshot2.png
│
└── utils/
```

---

## ⚙️ Installation

### 1. Clone Repository

```bash
git clone https://github.com/yourusername/AI-Knowledge-Assistant.git
cd AI-Knowledge-Assistant
```

### 2. Create Virtual Environment

```bash
python -m venv venv
```

### Windows

```bash
venv\Scripts\activate
```

### Linux / Mac

```bash
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Install Ollama

Download Ollama:

https://ollama.com

Pull Llama 3 model:

```bash
ollama pull llama3:8b
```

### 5. Configure Environment Variables

Create a `.env` file:

```env
LANGCHAIN_API_KEY=your_langsmith_key
LANGCHAIN_PROJECT=AI-Knowledge-Assistant
LANGCHAIN_TRACING_V2=true
HF_TOKEN=your_huggingface_token
```

---

## ▶️ Run Application

```bash
streamlit run app.py
```

Application will start at:

```text
http://localhost:8501
```

---

## 🧠 How It Works

### Step 1: Upload Knowledge Sources

Users can upload:

- PDF Documents
- Website URLs

### Step 2: Document Processing

Documents are:

- Loaded
- Split into chunks
- Embedded using HuggingFace Embeddings

### Step 3: Vector Storage

Embeddings are stored in:

```text
ChromaDB
```

### Step 4: Retrieval

When a user asks a question:

```text
Question
    ↓
Retriever
    ↓
Relevant Chunks
    ↓
Prompt
    ↓
LLM
    ↓
Final Answer
```

### Step 5: Memory

Conversation history is stored using:

```python
RunnableWithMessageHistory
```

allowing context-aware conversations.

---

## 🔍 RAG Architecture

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
Embeddings
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
Answer
```

---

## 📸 Screenshots

### Home Screen

Add screenshot here:

```text
assets/screenshot1.png
```

### Chat Interface

Add screenshot here:

```text
assets/screenshot2.png
```

---

## 📦 Requirements

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

## 🎯 Skills Demonstrated

This project demonstrates:

- Generative AI
- Retrieval-Augmented Generation (RAG)
- LangChain
- LLM Integration
- Prompt Engineering
- Semantic Search
- Embeddings
- Vector Databases
- Conversational Memory
- Streamlit Development
- Local AI Deployment
- Document Question Answering

---

## 🔮 Future Improvements

- Streaming responses
- Multiple LLM support
- Chat export
- Persistent Chroma database
- LangGraph memory
- Authentication system
- Multi-user support
- Source citations
- Hybrid search
- Image and DOCX support
- Cloud deployment

---

## 👨‍💻 Author

**Maher Dhami**

- GitHub: https://github.com/maherdhami
- LinkedIn: https://www.linkedin.com/in/maher-dhami-a15197225/

---

## ⭐ Support

If you found this project useful:

- Star the repository ⭐
- Fork the repository 🍴
- Share it with others 🚀

---

## 📜 License

This project is licensed under the MIT License.

---

### Repository Name

```text
AI-Knowledge-Assistant
```

### GitHub Description

```text
A Streamlit-based AI Knowledge Assistant powered by LangChain, Ollama, ChromaDB and HuggingFace Embeddings. Upload PDFs, scrape websites and chat with your knowledge base using Retrieval-Augmented Generation (RAG).
```

### GitHub Topics

```text
ai
llm
rag
langchain
streamlit
ollama
chromadb
huggingface
vector-database
retrieval-augmented-generation
chatbot
pdf-chat
document-qa
python
genai
```
