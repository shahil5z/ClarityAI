# app.py

import os
import streamlit as st
from dotenv import load_dotenv
from src.document_processing.pdf_processor import PDFProcessor
from src.document_processing.docx_processor import DocxProcessor
from src.embedding.embedder import DocumentEmbedder
from src.retrieval.retriever import DocumentRetriever
from src.generation.answer_generator import AnswerGenerator
from src.translation.translator import DocumentTranslator
from src.utils.config import Config
from src.utils.logger import setup_logger
from src.ui.components import (
    render_chat_history, 
    render_document_manager, 
    render_feedback_system,
    render_export_options,
    render_analytics
)

# Load environment variables
load_dotenv()

# Initialize logger
logger = setup_logger()

def main():
    st.set_page_config(
        page_title="ClarityAI - Document Intelligence",
        page_icon="📄",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    st.title("📄 ClarityAI - Document Intelligence")
    st.markdown("Upload your documents (PDFs, Word) and ask questions about their content.")
    
    # Initialize session state variables
    if 'processed' not in st.session_state:
        st.session_state.processed = False
    if 'vector_store' not in st.session_state:
        st.session_state.vector_store = None
    if 'retriever' not in st.session_state:
        st.session_state.retriever = None
    if 'answer_generator' not in st.session_state:
        st.session_state.answer_generator = None
    if 'translator' not in st.session_state:
        st.session_state.translator = DocumentTranslator()
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'uploaded_files' not in st.session_state:
        st.session_state.uploaded_files = []
    if 'feedback' not in st.session_state:
        st.session_state.feedback = None
    if 'last_question' not in st.session_state:
        st.session_state.last_question = ""
    
    # Sidebar for settings and document management
    with st.sidebar:
        st.header("Settings")
        language = st.selectbox("Select Language", ["English", "German"])
        model_name = st.selectbox("Select Model", ["gpt-3.5-turbo", "gpt-4"])
        
        # Advanced settings
        with st.expander("Advanced Settings"):
            temperature = st.slider("Temperature", 0.0, 1.0, 0.1, 0.05)
            max_tokens = st.slider("Max Tokens", 100, 4000, 1000, 100)
            chunk_size = st.slider("Chunk Size", 200, 2000, 1000, 100)
            chunk_overlap = st.slider("Chunk Overlap", 0, 500, 200, 10)
        
        # Update config based on user input
        Config.TEMPERATURE = temperature
        Config.MAX_TOKENS = max_tokens
        Config.CHUNK_SIZE = chunk_size
        Config.CHUNK_OVERLAP = chunk_overlap
        
        # Document management
        render_document_manager(st.session_state.uploaded_files, remove_selected_files)
        
        # Clear conversation button
        if st.button("Clear Conversation", type="secondary"):
            st.session_state.chat_history = []
            st.success("Conversation cleared!")
        
        # Export options
        render_export_options(st.session_state.chat_history)
        
        # Analytics
        render_analytics(st.session_state.chat_history)
        
        st.markdown("### About")
        st.markdown("ClarityAI is an AI-powered document intelligence system that can parse, understand, and answer questions based on uploaded documents.")
    
    # File upload section
    uploaded_files = st.file_uploader(
        "Upload documents", 
        type=["pdf", "docx"], 
        accept_multiple_files=True,
        help="Upload one or more PDF or Word documents to process"
    )
    
    # Process button
    if uploaded_files and st.button("Process Documents"):
        with st.spinner("Processing documents..."):
            try:
                # Initialize components
                pdf_processor = PDFProcessor()
                docx_processor = DocxProcessor()
                embedder = DocumentEmbedder(model_name="all-MiniLM-L6-v2")
                
                # Process documents
                documents = []
                for file in uploaded_files:
                    # Save uploaded file temporarily
                    temp_path = os.path.join("temp", file.name)
                    os.makedirs("temp", exist_ok=True)
                    with open(temp_path, "wb") as f:
                        f.write(file.getbuffer())
                    
                    # Process based on file type
                    if file.name.endswith('.pdf'):
                        docs = pdf_processor.process_pdf(temp_path)
                    elif file.name.endswith('.docx'):
                        docs = docx_processor.process_docx(temp_path)
                    
                    documents.extend(docs)
                
                # Create embeddings and vector store
                vector_store = embedder.create_vector_store(documents)
                
                # Initialize retriever and answer generator
                retriever = DocumentRetriever(vector_store)
                answer_generator = AnswerGenerator(model_name=model_name)
                
                # Store in session state
                st.session_state.vector_store = vector_store
                st.session_state.retriever = retriever
                st.session_state.answer_generator = answer_generator
                st.session_state.uploaded_files = uploaded_files
                st.session_state.processed = True
                
                st.success(f"Successfully processed {len(uploaded_files)} documents!")
                
            except Exception as e:
                st.error(f"Error processing documents: {str(e)}")
                logger.error(f"Error processing documents: {str(e)}")
    
    # Chat history display
    if st.session_state.chat_history:
        st.subheader("Conversation History")
        render_chat_history(st.session_state.chat_history)
    
    # Question answering section
    if st.session_state.processed:
        st.subheader("Ask Questions About Your Documents")
        
        question = st.text_input(
            "Enter your question:",
            placeholder="What information are you looking for?",
            help="Ask a question about the content of your uploaded documents"
        )
        
        # Only generate answer if question is not empty and different from last question
        if question and question != st.session_state.last_question:
            with st.spinner("Generating answer..."):
                try:
                    # Update last question
                    st.session_state.last_question = question
                    
                    # Add user question to chat history
                    st.session_state.chat_history.append({"role": "user", "content": question})
                    
                    # Translate question if needed
                    if language == "German":
                        translated_question = st.session_state.translator.translate(question, "en")
                    else:
                        translated_question = question
                    
                    # Retrieve relevant documents
                    relevant_docs = st.session_state.retriever.get_relevant_documents(translated_question)
                    
                    # Generate answer
                    answer = st.session_state.answer_generator.generate_answer(
                        question=translated_question,
                        documents=relevant_docs
                    )
                    
                    # Translate answer if needed
                    if language == "German":
                        answer = st.session_state.translator.translate(answer, "de")
                    
                    # Add AI response to chat history
                    st.session_state.chat_history.append({
                        "role": "assistant", 
                        "content": answer,
                        "sources": relevant_docs
                    })
                    
                    # Rerun to update the chat history display
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"Error generating answer: {str(e)}")
                    logger.error(f"Error generating answer: {str(e)}")
    else:
        st.info("Please upload and process documents to begin asking questions.")

def remove_selected_files(selected_files):
    """Remove selected files from the session state."""
    if not selected_files:
        return
    
    # Remove files from session state
    remaining_files = [f for f in st.session_state.uploaded_files if f not in selected_files]
    st.session_state.uploaded_files = remaining_files
    
    # If no files remain, reset processing state
    if not remaining_files:
        st.session_state.processed = False
        st.session_state.vector_store = None
        st.session_state.retriever = None
        st.session_state.answer_generator = None

if __name__ == "__main__":
    main()