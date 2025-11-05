#!/usr/bin/env python3
"""
NebulaRAG Web Interface - ChatGPT-like UI
A beautiful web interface for the RAG system using Streamlit
"""

import streamlit as st
import os
import sys
from pathlib import Path
import time
from typing import List, Dict, Any

# Add current directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

try:
    from nebularag.clients.nebula_client import NebulaBlockClient
    from nebularag.core.rag_pipeline import RAGPipeline
    from nebularag.utils.file_utils import read_text_files
    from nebularag.config.settings import get_settings
except ImportError as e:
    st.error(f"Import error: {e}")
    st.stop()

# Page configuration
st.set_page_config(
    page_title="NebulaRAG - AI Document Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for ChatGPT-like styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 1rem 0;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    
    .chat-message {
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        border-left: 4px solid #667eea;
    }
    
    .user-message {
        background-color: #f0f2f6;
        border-left-color: #667eea;
    }
    
    .assistant-message {
        background-color: #ffffff;
        border-left-color: #764ba2;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .status-success {
        color: #28a745;
        font-weight: bold;
    }
    
    .status-error {
        color: #dc3545;
        font-weight: bold;
    }
    
    .status-info {
        color: #17a2b8;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'rag_pipeline' not in st.session_state:
    st.session_state.rag_pipeline = None
if 'documents_loaded' not in st.session_state:
    st.session_state.documents_loaded = False
if 'documents_count' not in st.session_state:
    st.session_state.documents_count = 0

def initialize_rag_pipeline(docs_path: str, chunk_size: int = 800, chunk_overlap: int = 120, 
                          top_k: int = 12, rerank_k: int = 6) -> bool:
    """Initialize the RAG pipeline with documents."""
    try:
        with st.spinner("🔄 Initializing RAG pipeline..."):
            # Initialize client
            client = NebulaBlockClient()
            
            # Create RAG pipeline
            rag = RAGPipeline(client, chunk_size=chunk_size, top_k=top_k, rerank_k=rerank_k)
            
            # Read documents
            docs = read_text_files(docs_path)
            
            if not docs:
                st.error("❌ No documents found in the specified directory!")
                return False
            
            # Index documents
            num_chunks = rag.index_texts(docs)
            
            # Store in session state
            st.session_state.rag_pipeline = rag
            st.session_state.documents_loaded = True
            st.session_state.documents_count = len(docs)
            
            st.success(f"✅ Successfully loaded {len(docs)} documents and indexed {num_chunks} chunks!")
            return True
            
    except Exception as e:
        st.error(f"❌ Error initializing RAG pipeline: {str(e)}")
        return False

def ask_question(question: str) -> Dict[str, Any]:
    """Ask a question to the RAG pipeline."""
    try:
        if not st.session_state.rag_pipeline:
            return {"error": "RAG pipeline not initialized"}
        
        with st.spinner("🤔 Thinking..."):
            result = st.session_state.rag_pipeline.answer(question)
            return result
            
    except Exception as e:
        return {"error": str(e)}

# Main UI
def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🤖 NebulaRAG - AI Document Assistant</h1>
        <p>Ask questions about your documents using advanced RAG technology</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar for configuration
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # Documents path
        docs_path = st.text_input(
            "📁 Documents Path", 
            value="docs",
            help="Path to directory containing your documents (txt, md, pdf)"
        )
        
        # RAG parameters
        st.subheader("🔧 RAG Parameters")
        chunk_size = st.slider("Chunk Size", 200, 2000, 800, 50)
        chunk_overlap = st.slider("Chunk Overlap", 50, 500, 120, 10)
        top_k = st.slider("Top-K Retrieval", 5, 30, 12, 1)
        rerank_k = st.slider("Rerank-K", 3, 15, 6, 1)
        
        # Initialize button
        if st.button("🚀 Initialize RAG Pipeline", type="primary"):
            if initialize_rag_pipeline(docs_path, chunk_size, chunk_overlap, top_k, rerank_k):
                st.session_state.messages = []  # Clear previous messages
        
        # Status
        st.subheader("📊 Status")
        if st.session_state.documents_loaded:
            st.markdown(f'<p class="status-success">✅ Pipeline Ready</p>', unsafe_allow_html=True)
            st.markdown(f'<p class="status-info">📚 {st.session_state.documents_count} documents loaded</p>', unsafe_allow_html=True)
        else:
            st.markdown(f'<p class="status-error">❌ Pipeline Not Ready</p>', unsafe_allow_html=True)
        
        # Clear chat button
        if st.button("🗑️ Clear Chat"):
            st.session_state.messages = []
            st.rerun()
    
    # Main chat interface
    st.header("💬 Let's ask anything!")
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            
            # Show sources if available
            if message["role"] == "assistant" and "sources" in message:
                with st.expander("📚 Sources"):
                    for i, source in enumerate(message["sources"][:3]):  # Show top 3 sources
                        st.text(f"Source {i+1}: {source[:200]}...")
    
    # Chat input
    if prompt := st.chat_input("Ask a question about your documents..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Generate and display assistant response
        if st.session_state.rag_pipeline:
            with st.chat_message("assistant"):
                with st.spinner("🤔 Thinking..."):
                    result = ask_question(prompt)
                
                if "error" in result:
                    st.error(f"❌ Error: {result['error']}")
                    response_content = f"Sorry, I encountered an error: {result['error']}"
                else:
                    response_content = result.get("answer", "No answer generated")
                    st.markdown(response_content)
                    
                    # Show sources
                    if "sources" in result and result["sources"]:
                        with st.expander("📚 Sources"):
                            for i, source in enumerate(result["sources"][:3]):
                                st.text(f"Source {i+1}: {source[:200]}...")
            
            # Add assistant message to chat history
            st.session_state.messages.append({
                "role": "assistant", 
                "content": response_content,
                "sources": result.get("sources", [])
            })
        else:
            with st.chat_message("assistant"):
                st.error("❌ RAG pipeline not initialized. Please initialize it in the sidebar first.")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 1rem;">
        <p>🚀 Powered by NebulaRAG | Built with Streamlit</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
