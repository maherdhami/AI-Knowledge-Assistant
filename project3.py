import os
import streamlit as st
import tempfile
from dotenv import load_dotenv
load_dotenv()

st.set_page_config(page_title="AI Assistant", page_icon="🤖", layout="wide")

langapi=os.getenv("LANGCHAIN_API_KEY")
langproject=os.getenv("LANGCHAIN_PROJECT")
langtrace=os.getenv("LANGCHAIN_TRACING_V2")
hftoken=os.getenv("HF_TOKEN")
if not hftoken:
    try:
        hftoken = st.secrets.get("HF_TOKEN")
    except Exception:
        pass
if hftoken:
    os.environ["HF_TOKEN"] = hftoken

from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders import WebBaseLoader

from langchain_text_splitters import RecursiveCharacterTextSplitter
ts=RecursiveCharacterTextSplitter(chunk_size=100, chunk_overlap=20)

from langchain_huggingface import HuggingFaceEmbeddings

@st.cache_resource
def get_embeddings():
    return HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

hf = get_embeddings()

from langchain_chroma import Chroma

from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder
prompt=ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """Act like ChatGPT and Claude Pro.
Answer the user's questions clearly, accurately, and politely.
If context is provided below, use it to answer the question. If no context is provided or if context is empty, answer normally using your own general knowledge.

Context:
{t}"""
        ),
        MessagesPlaceholder(variable_name="history"),
        ("human","{input}")
    ]
)

from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

store={}

def get_session_history(session_id:str)->BaseChatMessageHistory:
    if session_id not in store:
        store[session_id]=ChatMessageHistory()
    return store[session_id]

from langchain_core.messages import trim_messages
from langchain_groq import ChatGroq
from langchain_ollama import ChatOllama

if "messages" not in st.session_state:
    st.session_state.messages=[]

if "session_id" not in st.session_state:
    st.session_state.session_id="user1"

if "retriever" not in st.session_state:
    st.session_state.retriever=None

# Retrieve default Groq API Key from environment or Streamlit secrets
default_groq_key = os.getenv("GROQ_API_KEY", "")
if not default_groq_key:
    try:
        default_groq_key = st.secrets.get("GROQ_API_KEY", "")
    except Exception:
        default_groq_key = ""

st.title("🤖 AI Assistant")

with st.sidebar:
    st.header("⚙️ Model Configuration")
    model_provider = st.selectbox(
        "LLM Provider",
        ["Groq (Cloud - Recommended)", "Ollama (Local only)"],
        index=0,
        help="Use Groq for Streamlit Cloud deployment. Ollama only works locally on your own PC."
    )

    if model_provider.startswith("Groq"):
        user_groq_key = st.text_input(
            "Groq API Key",
            value=default_groq_key,
            type="password",
            help="Get your free key at https://console.groq.com"
        )
        selected_model_name = st.selectbox(
            "Model",
            ["llama-3.3-70b-versatile", "llama-3.1-8b-instant", "mixtral-8x7b-32768"],
            index=0
        )
        if user_groq_key:
            model = ChatGroq(model=selected_model_name, api_key=user_groq_key)
        else:
            model = None
            st.warning("⚠️ Please provide a Groq API Key.")
    else:
        ollama_model_name = st.text_input("Ollama Model", value="llama3:8b")
        model = ChatOllama(model=ollama_model_name)

    st.divider()
    st.header("📚 Knowledge Base")
    uploaded_files=st.file_uploader("Upload Documents", accept_multiple_files=True, type=["pdf"])
    website_url=st.text_input("Website URL")

    if st.button("Process Documents"):
        if not uploaded_files and not website_url:
            st.warning("Please upload at least one PDF file or enter a website URL.")
        else:
            all_docs=[]
            # User Website
            if website_url:
                try:
                    with st.spinner("Loading website content..."):
                        web_loader=WebBaseLoader(website_url)
                        all_docs.extend(web_loader.load())
                except Exception as e:
                    st.error(f"Website Error: {e}")
            # PDF Uploads
            if uploaded_files:
                with st.spinner("Loading uploaded PDFs..."):
                    for file in uploaded_files:
                        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                            tmp_file.write(file.getbuffer())
                            tmp_path = tmp_file.name
                        try:
                            loader = PyPDFLoader(tmp_path)
                            all_docs.extend(loader.load())
                        finally:
                            if os.path.exists(tmp_path):
                                os.remove(tmp_path)

            if all_docs:
                with st.spinner("Indexing documents into vector store..."):
                    textsplit=ts.split_documents(all_docs)
                    db=Chroma.from_documents(textsplit,hf)
                    st.session_state.retriever=db.as_retriever()
                    st.success("Knowledge Base Created Successfully!")
            else:
                st.warning("No document content could be extracted.")

    st.divider()

    # Status display
    if st.session_state.retriever:
        st.success("📚 Mode: Knowledge Base Active (RAG)")
        if st.button("Clear Knowledge Base"):
            st.session_state.retriever = None
            st.rerun()
    else:
        st.info("🤖 Mode: Direct LLM (No documents loaded)")

    if st.button("Clear Chat"):
        st.session_state.messages = []
        if st.session_state.session_id in store:
            store[st.session_state.session_id] = ChatMessageHistory()
        st.rerun()

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# USER INPUT

user_prompt=st.chat_input("Ask Anything...")
if user_prompt:
    if model is None:
        st.error("Please provide a valid Groq API Key in the sidebar to chat.")
    else:
        st.session_state.messages.append(
            {
                "role":"user",
                "content":user_prompt
            }
        )
        with st.chat_message("user"):
            st.markdown(user_prompt)

        history=get_session_history(st.session_state.session_id)
        try:
            trim=trim_messages(strategy="last", max_tokens=10, token_counter=len, include_system=True)
            history.messages=trim.invoke(history.messages)
        except Exception:
            pass
        
        if st.session_state.retriever:
            t=(st.session_state.retriever.invoke(user_prompt))
            t="\n\n".join([doc.page_content for doc in t])
        else:
            t=""
            
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    chain=prompt|model
                    chain_with_history=RunnableWithMessageHistory(
                        chain,
                        get_session_history,
                        input_messages_key="input",
                        history_messages_key="history"
                    )
                    response=chain_with_history.invoke(
                        {
                            "input":user_prompt,
                            "t":t
                        },
                        config={"configurable":{"session_id":st.session_state.session_id}}
                    )
                    answer=response.content
                    st.markdown(answer)
                    st.session_state.messages.append(
                        {
                            "role":"assistant",
                            "content":answer
                        }
                    )
                except Exception as e:
                    err_msg = str(e)
                    if "ConnectError" in type(e).__name__ or "ConnectError" in err_msg or "11434" in err_msg:
                        st.error("❌ **Connection Error**: Could not connect to local Ollama server (http://localhost:11434).")
                        st.info("💡 **If you are running on Streamlit Cloud**, Ollama cannot run in the cloud. Please switch the **LLM Provider** in the sidebar to **Groq (Cloud - Recommended)**.")
                    else:
                        st.error(f"Error generating response: {e}")