import os
import streamlit as st
import time
from dotenv import load_dotenv
import shutil
from typing import Optional, Any
import datetime

# --- LangChain/ChromaDB Imports ---
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.document_loaders import SeleniumURLLoader
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter  # Corrected class name
from langchain_core.prompts import PromptTemplate
from langchain_core.documents import Document

# --- ChromaDB Client Import (for persistence) ---
import chromadb

# --- CONSTANTS ---
# Base path for storing the indexed articles (the actual index uses a timestamped subfolder)
CHROMA_BASE_PATH = "chroma_index_storage"
CHROMA_COLLECTION_NAME = "default_collection"

# --- UI CONFIGURATION ---
st.set_page_config(
    page_title="InfoGopher: News Research Tool",
    page_icon="🔎",
    layout="wide"
)

# --- LLM PROMPT FOR NAMING ---
NAME_PROMPT = PromptTemplate(
    template="""
    Analyze the following user question and generate a very short, concise, professional title (maximum 5 words) for a chat conversation based on its content.

    QUESTION: {question}

    TITLE:
    """,
    input_variables=["question"]
)


# --- SESSION CALLBACKS (CHAT MANAGEMENT) ---
def switch_conversation(conv_id):
    """Callback to switch the current active conversation."""
    st.session_state["current_conv_id"] = conv_id
    st.session_state["question_input"] = ""


def delete_conversation(conv_id):
    """Callback to delete a conversation page."""
    if conv_id in st.session_state["conversations"]:
        del st.session_state["conversations"][conv_id]

        if st.session_state["current_conv_id"] == conv_id:
            if st.session_state["conversations"]:
                st.session_state["current_conv_id"] = list(st.session_state["conversations"].keys())[0]
            else:
                new_chat()
        st.rerun()


def new_chat():
    """Callback to create and switch to a new conversation."""
    base_id = "New Chat"
    num = 1
    new_id = base_id
    while new_id in st.session_state["conversations"]:
        num += 1
        new_id = f"{base_id} {num}"

    st.session_state["conversations"][new_id] = {
        "qa_history": [],
        "question_history": []
    }
    st.session_state["current_conv_id"] = new_id
    st.session_state["question_input"] = ""
    st.rerun()


# --- SESSION STATE INITIALIZATION ---
if "conversations" not in st.session_state:
    st.session_state["conversations"] = {}
if "current_conv_id" not in st.session_state:
    st.session_state["current_conv_id"] = None
if "question_input" not in st.session_state:
    st.session_state["question_input"] = ""
# Stores the path to the currently loaded/active Chroma index
if "active_chroma_path" not in st.session_state:
    st.session_state["active_chroma_path"] = None

if not st.session_state["conversations"]:
    new_chat()

current_conv_id = st.session_state["current_conv_id"]
current_conv = st.session_state["conversations"][current_conv_id]

# Load environment variables (GEMINI_API_KEY)
load_dotenv()

# --- CRITICAL ENVIRONMENT VARIABLE FIX ---
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if GEMINI_API_KEY:
    os.environ["GOOGLE_API_KEY"] = GEMINI_API_KEY
else:
    st.error("GEMINI_API_KEY not found. Please ensure it is set in your .env file.")
    st.stop()


# --- CACHED FUNCTIONS ---

@st.cache_resource(show_spinner=False)
def get_embeddings() -> GoogleGenerativeAIEmbeddings:
    return GoogleGenerativeAIEmbeddings(
        model="text-embedding-004",
        task_type="retrieval_document"
    )


@st.cache_resource(show_spinner=False)
def get_llm() -> ChatGoogleGenerativeAI:
    return ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0.2
    )


@st.cache_resource(show_spinner=False)
def get_vectorstore() -> Optional[Chroma]:
    """Loads the single, active Chroma collection based on session state."""
    active_path = st.session_state.get("active_chroma_path")

    if active_path and os.path.exists(active_path):
        try:
            client = chromadb.PersistentClient(path=active_path)

            return Chroma(
                client=client,
                collection_name=CHROMA_COLLECTION_NAME,
                embedding_function=get_embeddings()
            )
        except Exception as e:
            st.warning(f"Failed to load vector store from '{active_path}'. Error: {e}")
            return None
    return None


RAG_PROMPT = PromptTemplate(
    template="""
    You are an expert news research assistant. Use ONLY the following context to answer the user's question concisely. 
    If you don't know the answer, just say that you don't know based on the context provided.

    CONTEXT:
    {context}

    QUESTION: {question}

    Answer:
    """,
    input_variables=["context", "question"]
)

# Initialize models and embeddings once
embeddings = get_embeddings()
llm = get_llm()

# --- STREAMLIT UI ---

st.title(f"🔎 InfoGopher: {current_conv_id}")
st.caption("Leveraging Gemini Embeddings and LLMs for contextual news summarization.")
st.markdown("---")

## 📚 Session Management and Inputs

with st.sidebar:
    st.header("📚 Chat Sessions")

    st.button("➕ Start New Chat", on_click=lambda: new_chat(), use_container_width=True, type="primary")
    st.markdown("---")

    # List all saved conversations
    for conv_id in st.session_state["conversations"]:
        is_current = conv_id == current_conv_id

        col_name, col_delete = st.columns([0.8, 0.2])

        with col_name:
            style = "primary" if is_current else "secondary"
            st.button(
                f"{'▶️' if is_current else ''} {conv_id}",
                key=f"switch_{conv_id}",
                on_click=lambda id=conv_id: switch_conversation(id),
                use_container_width=True,
                type=style
            )

        # CORRECTED LOGIC: Show delete button for ANY chat as long as there is more than one chat session total.
        if len(st.session_state["conversations"]) > 1:
            with col_delete:
                st.button(
                    "🗑️",
                    key=f"delete_{conv_id}",
                    on_click=lambda id=conv_id: delete_conversation(id),
                    use_container_width=True,
                    type="secondary"
                )

    st.markdown("---")
    st.header("🔗 Article Indexing")

    articles_input = st.text_area(
        "Enter News Article URLs (one per line):",
        height=200,
        key="url_input",
        placeholder="e.g., https://www.bbc.com/news/article1\nhttps://www.cnn.com/article2"
    )
    process_url_clicked = st.button("Fetch and Index Articles 💾", use_container_width=True)
    st.markdown("---")

# 2. Main Content Area

# --- KB STATUS CHECK ---
if st.session_state.get("active_chroma_path"):
    st.info(
        f"✅ Indexed articles are active and ready for querying from: `{os.path.basename(st.session_state['active_chroma_path'])}`.")
else:
    st.warning("⚠️ Article index not yet created. Please index articles using the sidebar.")

st.markdown("---")

# The question input
question = st.text_input(
    "Ask a question about the indexed articles:",
    key="question_input",
    placeholder="e.g., What was the main topic of the BBC article?"
)
answer_button = st.button("Answer Question 💡", use_container_width=True)
st.markdown("<br>", unsafe_allow_html=True)

# ==============================================================================
# CORE LOGIC: PROCESS URLS (INDEX CREATION) - FIX FOR READONLY DATABASE
# ==============================================================================
main_placeholder = st.empty()

if process_url_clicked:
    urls = [url.strip() for url in articles_input.split('\n') if url.strip()]

    if not urls:
        main_placeholder.error("🛑 Please enter at least one URL.")
    else:

        # --- FIX: Create a unique, new directory for the index to avoid file locks ---
        # This prevents the "readonly database" error by creating a fresh space.
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        CHROMA_NEW_PATH = os.path.join(CHROMA_BASE_PATH, f"index_{timestamp}")

        # 1. Clear the old, *cached* connection first to release file handles
        get_vectorstore.clear()

        # 2. Delete the *previous* active path to clean up disk space (if it exists)
        previous_path = st.session_state.get("active_chroma_path")
        if previous_path and os.path.exists(previous_path):
            main_placeholder.warning(f"⚠️ Clearing old index at {previous_path}...")
            shutil.rmtree(previous_path)
            time.sleep(0.5)

            # 3. Create the new index in the unique path
        with st.spinner("⏳ Fetching and Loading Data from URLs (using Selenium)..."):
            loader = SeleniumURLLoader(urls=urls)
            data = loader.load()

        if not data:
            main_placeholder.error("❌ Data loading failed. Check URLs or connection.")
            st.stop()

        else:
            main_placeholder.success("✅ Data Loading Complete!")

            with st.spinner("⏳ Splitting Documents and Creating Embeddings..."):
                # Use the correctly named class
                text_splitter = RecursiveCharacterTextSplitter(
                    separators=['\n\n', '\n', '.', ','],
                    chunk_size=1000
                )
                docs = text_splitter.split_documents(data)

                if not docs:
                    main_placeholder.error("❌ Text splitting failed! No usable text chunks were found.")
                    st.stop()

                # --- CHROMADB CREATION (Writing to the unique, new path) ---
                vectorstore_chroma = Chroma.from_documents(
                    documents=docs,
                    embedding=embeddings,
                    persist_directory=CHROMA_NEW_PATH,
                    collection_name=CHROMA_COLLECTION_NAME
                )
                vectorstore_chroma.persist()

            main_placeholder.success("✅ Embeddings Built and ChromaDB persisted successfully!")

            # 4. Update the session state with the new, active path
            st.session_state["active_chroma_path"] = CHROMA_NEW_PATH

            main_placeholder.success(f"💾 Article index saved and ready!")
            st.rerun()

        # ==============================================================================
# CORE LOGIC: ANSWER QUESTION (RAG PIPELINE)
# ==============================================================================
progress_container = st.empty()

if answer_button and question:

    if not st.session_state.get("active_chroma_path"):
        st.error("Please index articles using the sidebar first.")
        st.stop()

    with progress_container.container():
        st.info(f"🔎 Searching indexed articles and Generating Answer...")

    vectorstore = get_vectorstore()

    if vectorstore:
        try:
            # Check if this is the first question in a generic-named chat
            is_new_chat = current_conv_id.startswith("New Chat") and not current_conv["qa_history"]

            # 1. RAG EXECUTION...
            retriever = vectorstore.as_retriever(search_kwargs={"k": 4})
            docs_used = retriever.invoke(question)
            context = "\n\n".join([d.page_content for d in docs_used])
            final_prompt = RAG_PROMPT.format(context=context, question=question)

            with st.spinner("🧠 Analyzing context and invoking Gemini..."):
                result = llm.invoke(final_prompt).content

            progress_container.empty()

            # 2. DYNAMIC CHAT NAMING LOGIC
            if is_new_chat:
                with st.spinner("🏷️ Generating dynamic chat title..."):
                    title_prompt = NAME_PROMPT.format(question=question)
                    new_title = llm.invoke(title_prompt).content.strip().replace('"', '')

                    if not new_title or new_title in st.session_state["conversations"]:
                        new_title = f"Untitled - {question[:20]}..."

                    # Rename the conversation
                    st.session_state["conversations"][new_title] = st.session_state["conversations"].pop(
                        current_conv_id)
                    st.session_state["current_conv_id"] = new_title
                    st.rerun()

                    # 3. Package and Append Results to CURRENT SESSION
            sources = set(d.metadata.get("source") for d in docs_used if d.metadata.get("source"))

            qa_pair = {
                "question": question,
                "answer": result.strip(),
                "sources": list(sources)
            }
            current_conv = st.session_state["conversations"][st.session_state["current_conv_id"]]
            current_conv["qa_history"].append(qa_pair)

            if not current_conv["question_history"] or current_conv["question_history"][-1] != question:
                current_conv["question_history"].append(question)

            st.rerun()

        except Exception as e:
            with progress_container.container():
                st.error(f"❌ An error occurred during query execution: {e}")
    else:
        with progress_container.container():
            st.warning("⚠️ Could not load the article index. Please try indexing articles again.")

# --- CHAT HISTORY DISPLAY ---
st.markdown("## 💬 Conversation History")
if current_conv["qa_history"]:
    for qa_pair in current_conv["qa_history"]:
        with st.container(border=True):
            st.markdown(f"**❓ Question:** {qa_pair['question']}")
            st.success(qa_pair['answer'])

            st.markdown("###### 🔗 Sources")
            if qa_pair['sources']:
                for i, source in enumerate(qa_pair['sources']):
                    domain_name = source.split('//')[-1].split('/')[0]
                    st.markdown(f"**{i + 1}.** [{domain_name}... ]({source})")

            else:
                st.write("No specific sources found in the retrieved documents.")
        st.markdown("---")
else:
    st.info(f"Ask your first question in **{st.session_state['current_conv_id']}** above!")