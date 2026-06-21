import os
from dotenv import load_dotenv
load_dotenv()

langapi=os.getenv("LANGCHAIN_API_KEY")
langproject=os.getenv("LANGCHAIN_PROJECT")
langtrace=os.getenv("LANGCHAIN_TRACING_V2")
hftoken=os.getenv("HF_TOKEN")

from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders import WebBaseLoader

from langchain_text_splitters import RecursiveCharacterTextSplitter
ts=RecursiveCharacterTextSplitter(chunk_size=100, chunk_overlap=20)

from langchain_huggingface import HuggingFaceEmbeddings
hf=HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

from langchain_chroma import Chroma

from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder
prompt=ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
            Act like ChatGPT and Claude Pro.
            Answer using the provided context if relevant.
            Context:
            {t}
            """
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

from langchain_ollama import ChatOllama
from langchain_core.messages import trim_messages

model=ChatOllama(model="llama3:8b")
chain=prompt|model
chain=RunnableWithMessageHistory(chain, get_session_history, input_messages_key="input", history_messages_key="history")
trim=trim_messages(strategy="last", max_tokens=200, token_counter=model, include_system=True)

# STREAMLIT

import streamlit as st

st.set_page_config(page_title="AI Assistant", page_icon="🤖", layout="wide")
if "messages" not in st.session_state:
    st.session_state.messages=[]

if "session_id" not in st.session_state:
    st.session_state.session_id="user1"

if "retriever" not in st.session_state:
    st.session_state.retriever=None

st.title("AI Assistant")
with st.sidebar:
    st.header("Knowledge Base")
    uploaded_files=st.file_uploader("Upload Documents", accept_multiple_files=True, type=["pdf"])
    website_url=st.text_input("Website URL")

    if st.button("Process Documents"):

        all_docs=[]
        # Default Website
        webl=WebBaseLoader("https://huggingface.co/")
        all_docs.extend(webl.load())
        # User Website
        if website_url:
            try:
                web_loader=WebBaseLoader(website_url)
                all_docs.extend(web_loader.load())
            except Exception as e:
                st.error(f"Website Error: {e}")
        # PDF Uploads
        if uploaded_files:
            for file in uploaded_files:
                with open(file.name,"wb") as f:
                    f.write(file.getbuffer())
                loader=PyPDFLoader(file.name)
                all_docs.extend(loader.load())

        textsplit=ts.split_documents(all_docs)
        texts=[doc.page_content for doc in textsplit]
        embeddoc=hf.embed_documents(texts)
        db=Chroma.from_documents(textsplit,hf)

        st.session_state.retriever=(db.as_retriever())
        st.success("Knowledge Base Created")

    st.divider()
    if st.button("Clear Chat"):
        st.session_state.messages=[]
        store[st.session_state.session_id]=ChatMessageHistory()
        st.rerun()

# DISPLAY CHAT HISTORY

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# USER INPUT

user_prompt=st.chat_input("Ask Anything...")

if user_prompt:

    st.session_state.messages.append(
        {
            "role":"user",
            "content":user_prompt
        }
    )

    with st.chat_message("user"):
        st.markdown(user_prompt)

    history=get_session_history(st.session_state.session_id)

    history.messages=trim.invoke(history.messages)

    if st.session_state.retriever:
        docs=(st.session_state.retriever.invoke(user_prompt))
        t="\n\n".join(
            [
                doc.page_content
                for doc in docs
            ]
        )
        
    else:
        t=""

    response=chain.invoke(
        {
            "input":user_prompt,
            "t":t
        },
        config={"configurable":{"session_id":st.session_state.session_id}}
    )
    
    answer=response.content
    st.session_state.messages.append({"role":"assistant","content":answer})
    with st.chat_message("assistant"):
        st.markdown(answer)