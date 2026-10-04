import os
import tempfile
import streamlit as st

# ---------------------------------------------------------
# STREAMLIT CONFIGURATION
# ---------------------------------------------------------

st.set_page_config(
    page_title="AI Assistant",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 AI Assistant")

# ---------------------------------------------------------
# DOCUMENT LOADERS
# ---------------------------------------------------------

from langchain_community.document_loaders import (
    PyPDFLoader,
    WebBaseLoader
)

# ---------------------------------------------------------
# TEXT SPLITTER
# ---------------------------------------------------------

from langchain_text_splitters import RecursiveCharacterTextSplitter

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=100
)

# ---------------------------------------------------------
# LOCAL EMBEDDING MODEL
# No API key required
# ---------------------------------------------------------

from langchain_huggingface import HuggingFaceEmbeddings


@st.cache_resource
def get_embeddings():
    return HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )


embeddings = get_embeddings()

# ---------------------------------------------------------
# CHROMA VECTOR DATABASE
# ---------------------------------------------------------

from langchain_chroma import Chroma

# ---------------------------------------------------------
# LOCAL LLM USING OLLAMA
# No API key required
# ---------------------------------------------------------

from langchain_ollama import ChatOllama


@st.cache_resource
def get_model(model_name):
    return ChatOllama(
        model=model_name,
        temperature=0.3
    )


# ---------------------------------------------------------
# PROMPT
# ---------------------------------------------------------

from langchain_core.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder
)

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are a helpful AI assistant.

Answer the user's questions clearly, accurately and politely.

If document context is provided, use that context to answer the question.

If the context does not contain the answer, you may answer using your
general knowledge.

Do not make up information from the documents.

Context:

{context}
"""
        ),

        MessagesPlaceholder(variable_name="history"),

        (
            "human",
            "{input}"
        )
    ]
)

# ---------------------------------------------------------
# CHAT HISTORY
# ---------------------------------------------------------

from langchain_community.chat_message_histories import ChatMessageHistory

from langchain_core.chat_history import BaseChatMessageHistory

from langchain_core.runnables.history import RunnableWithMessageHistory


store = {}


def get_session_history(session_id: str) -> BaseChatMessageHistory:

    if session_id not in store:

        store[session_id] = ChatMessageHistory()

    return store[session_id]


# ---------------------------------------------------------
# STREAMLIT SESSION STATE
# ---------------------------------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []


if "session_id" not in st.session_state:
    st.session_state.session_id = "user1"


if "retriever" not in st.session_state:
    st.session_state.retriever = None


if "vector_db" not in st.session_state:
    st.session_state.vector_db = None


# ---------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------

with st.sidebar:

    st.header("⚙️ Model Configuration")

    # Models installed locally using Ollama
    available_models = [
    "gemma3:latest",
    "llama3:8b",
    "gemma:2b",
    "glm-4.7-flash:latest"
]

    selected_model = st.selectbox(
        "Select Local Model",
        available_models
    )

    model = get_model(selected_model)

    st.caption("✅ Running locally using Ollama")
    st.caption("🔑 No API Key Required")

    st.divider()

    # -----------------------------------------------------
    # KNOWLEDGE BASE
    # -----------------------------------------------------

    st.header("📚 Knowledge Base")

    uploaded_files = st.file_uploader(
        "Upload PDF Documents",
        accept_multiple_files=True,
        type=["pdf"]
    )

    website_url = st.text_input(
        "Website URL"
    )

    if st.button("Process Documents"):

        if not uploaded_files and not website_url:

            st.warning(
                "Please upload at least one PDF or enter a website URL."
            )

        else:

            all_documents = []

            # -------------------------------------------------
            # WEBSITE
            # -------------------------------------------------

            if website_url:

                try:

                    with st.spinner(
                        "Loading website content..."
                    ):

                        web_loader = WebBaseLoader(
                            website_url
                        )

                        website_documents = (
                            web_loader.load()
                        )

                        all_documents.extend(
                            website_documents
                        )

                except Exception as e:

                    st.error(
                        f"Website loading error: {e}"
                    )

            # -------------------------------------------------
            # PDF DOCUMENTS
            # -------------------------------------------------

            if uploaded_files:

                with st.spinner(
                    "Loading PDF documents..."
                ):

                    for uploaded_file in uploaded_files:

                        tmp_path = None

                        try:

                            with tempfile.NamedTemporaryFile(
                                delete=False,
                                suffix=".pdf"
                            ) as tmp_file:

                                tmp_file.write(
                                    uploaded_file.getbuffer()
                                )

                                tmp_path = tmp_file.name

                            loader = PyPDFLoader(
                                tmp_path
                            )

                            pdf_documents = (
                                loader.load()
                            )

                            all_documents.extend(
                                pdf_documents
                            )

                        except Exception as e:

                            st.error(
                                f"PDF Error: {e}"
                            )

                        finally:

                            if (
                                tmp_path
                                and
                                os.path.exists(tmp_path)
                            ):

                                os.remove(tmp_path)

            # -------------------------------------------------
            # CREATE VECTOR DATABASE
            # -------------------------------------------------

            if all_documents:

                with st.spinner(
                    "Creating vector database..."
                ):

                    document_chunks = (
                        text_splitter.split_documents(
                            all_documents
                        )
                    )

                    vector_db = (
                        Chroma.from_documents(
                            documents=document_chunks,
                            embedding=embeddings
                        )
                    )

                    st.session_state.vector_db = (
                        vector_db
                    )

                    st.session_state.retriever = (
                        vector_db.as_retriever(
                            search_kwargs={
                                "k": 4
                            }
                        )
                    )

                st.success(
                    "✅ Knowledge Base Created Successfully!"
                )

                st.write(
                    f"Documents loaded: "
                    f"{len(all_documents)}"
                )

                st.write(
                    f"Chunks created: "
                    f"{len(document_chunks)}"
                )

            else:

                st.warning(
                    "No document content could be extracted."
                )

    # -----------------------------------------------------
    # KNOWLEDGE BASE STATUS
    # -----------------------------------------------------

    st.divider()

    if st.session_state.retriever is not None:

        st.success(
            "📚 Mode: RAG Active"
        )

        if st.button(
            "Clear Knowledge Base"
        ):

            st.session_state.retriever = None

            st.session_state.vector_db = None

            st.rerun()

    else:

        st.info(
            "🤖 Mode: Direct Local LLM"
        )

    # -----------------------------------------------------
    # CLEAR CHAT
    # -----------------------------------------------------

    if st.button("Clear Chat"):

        st.session_state.messages = []

        session_id = (
            st.session_state.session_id
        )

        if session_id in store:

            store[session_id] = (
                ChatMessageHistory()
            )

        st.rerun()


# ---------------------------------------------------------
# DISPLAY EXISTING CHAT
# ---------------------------------------------------------

for message in st.session_state.messages:

    with st.chat_message(
        message["role"]
    ):

        st.markdown(
            message["content"]
        )


# ---------------------------------------------------------
# USER INPUT
# ---------------------------------------------------------

user_input = st.chat_input(
    "Ask Anything..."
)


if user_input:

    # -----------------------------------------------------
    # DISPLAY USER MESSAGE
    # -----------------------------------------------------

    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )

    with st.chat_message("user"):

        st.markdown(
            user_input
        )

    # -----------------------------------------------------
    # RETRIEVE DOCUMENT CONTEXT
    # -----------------------------------------------------

    context = ""

    if st.session_state.retriever is not None:

        try:

            retrieved_documents = (
                st.session_state.retriever.invoke(
                    user_input
                )
            )

            context = "\n\n".join(
                [
                    document.page_content
                    for document
                    in retrieved_documents
                ]
            )

        except Exception as e:

            st.warning(
                f"Retrieval Error: {e}"
            )

            context = ""

    # -----------------------------------------------------
    # CREATE LANGCHAIN
    # -----------------------------------------------------

    chain = prompt | model

    chain_with_history = (
        RunnableWithMessageHistory(
            chain,
            get_session_history,
            input_messages_key="input",
            history_messages_key="history"
        )
    )

    # -----------------------------------------------------
    # GENERATE RESPONSE
    # -----------------------------------------------------

    with st.chat_message(
        "assistant"
    ):

        with st.spinner(
            "Thinking..."
        ):

            try:

                response = (
                    chain_with_history.invoke(
                        {
                            "input": user_input,
                            "context": context
                        },
                        config={
                            "configurable": {
                                "session_id":
                                st.session_state.session_id
                            }
                        }
                    )
                )

                answer = response.content

                st.markdown(
                    answer
                )

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": answer
                    }
                )

            except Exception as e:

                st.error(
                    f"""
Error generating response.

Make sure Ollama is running and the selected model is installed.

Error: {e}
"""
                )