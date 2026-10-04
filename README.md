# 🤖 AI Knowledge Assistant

An AI-powered Knowledge Assistant built using **LangChain**, **Streamlit**, **Ollama**, **ChromaDB**, and **HuggingFace Embeddings**.

The application allows users to upload documents, process websites, build a local knowledge base, and chat with AI using Retrieval-Augmented Generation (RAG) — all without requiring any API key.

---

## 🚀 Features

- 📄 Upload PDF Documents
- 🌐 Process Website URLs
- 🧠 Retrieval-Augmented Generation (RAG)
- 🔍 Semantic Search using Vector Embeddings
- 💾 ChromaDB Vector Database
- 🤖 Multiple Ollama Model Support
- 💬 Conversational Chat Interface
- 📝 Chat Memory
- 🔒 Runs Completely Locally
- 🔑 No API Key Required

---

## 🛠️ Technologies Used

- Python
- Streamlit
- LangChain
- Ollama
- ChromaDB
- HuggingFace Embeddings
- BeautifulSoup
- Requests

---

## 📂 Project Structure

```text
AI-Knowledge-Assistant/
│
├── project3.py
├── requirements.txt
├── README.md
├── .gitignore
└── project3.ipynb
```

---

## ⚙️ System Requirements

### Software Required

- Python 3.10 or higher
- Git
- Ollama

### Download Links

Python:
https://www.python.org/downloads/

Git:
https://git-scm.com/downloads

Ollama:
https://ollama.com/download

---

## 📥 Clone the Repository

```bash
git clone https://github.com/maherdhami/AI-Knowledge-Assistant.git

cd AI-Knowledge-Assistant
```

---

## 🐍 Create Virtual Environment

### Windows

```bash
python -m venv venv

venv\Scripts\activate
```

### Linux / Mac

```bash
python3 -m venv venv

source venv/bin/activate
```

---

## 📦 Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🤖 Install Ollama Model

Pull at least one model before running the application.

Recommended:

```bash
ollama pull gemma3:latest
```

Optional Models:

```bash
ollama pull llama3:8b

ollama pull gemma:2b

ollama pull glm-4.7-flash:latest
```

Verify installed models:

```bash
ollama list
```

Example Output:

```text
NAME
gemma3:latest
llama3:8b
gemma:2b
glm-4.7-flash:latest
```

---

## ▶️ Start Ollama

Open a terminal and run:

```bash
ollama serve
```

Keep this terminal running.

---

## ▶️ Run the Application

Open another terminal.

Activate virtual environment:

### Windows

```bash
venv\Scripts\activate
```

### Linux / Mac

```bash
source venv/bin/activate
```

Run Streamlit:

```bash
streamlit run project3.py
```

---

## 🌐 Open the Application

Open your browser and visit:

```text
http://localhost:8501
```

---

## 📚 How to Use

### Step 1: Select AI Model

Choose any installed Ollama model from the sidebar.

Recommended:

```text
gemma3:latest
```

---

### Step 2: Upload Documents

Upload one or more PDF documents.

---

### Step 3: Process Documents

Click:

```text
Process Documents
```

The application will:

- Extract document content
- Split text into chunks
- Generate embeddings
- Store vectors in ChromaDB
- Create a searchable knowledge base

---

### Step 4: Ask Questions

Example Queries:

```text
Summarize this document.
```

```text
What are the key findings?
```

```text
Explain chapter 3.
```

```text
List important points.
```

---

### Step 5: Website Knowledge Base

Enter a website URL:

```text
https://en.wikipedia.org/wiki/Artificial_intelligence
```

Click:

```text
Process Documents
```

The website content becomes part of the knowledge base.

---

## 🔒 Privacy

- Runs entirely on local machine
- No OpenAI API required
- No Groq API required
- No Gemini API required
- User data remains local
- Uploaded files are not sent to external services

---

## 🎯 Quick Start

```bash
git clone https://github.com/maherdhami/AI-Knowledge-Assistant.git

cd AI-Knowledge-Assistant

python -m venv venv

venv\Scripts\activate

pip install -r requirements.txt

ollama pull gemma3:latest

ollama serve
```

Open a second terminal:

```bash
cd AI-Knowledge-Assistant

venv\Scripts\activate

streamlit run project3.py
```

Open:

```text
http://localhost:8501
```

---

## 📖 Academic Purpose

This project demonstrates:

- Retrieval-Augmented Generation (RAG)
- Vector Databases
- Local Large Language Models (LLMs)
- Semantic Search
- LangChain Framework
- Streamlit Application Development
- Document Question Answering Systems

---

## 👨‍💻 Author

### Maher Dhami

GitHub:
https://github.com/maherdhami

LinkedIn:
https://www.linkedin.com/in/maher-dhami-a15197225/

---

## 📄 License

This project is developed for educational and academic learning purposes.

Feel free to use, modify, and learn from the code.
