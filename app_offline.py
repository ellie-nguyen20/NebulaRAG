#!/usr/bin/env python3
"""
NebulaRAG Web Interface - Offline Demo Version
A demo version that works without API calls for testing the UI
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
    from nebularag.utils.file_utils import read_text_files
    from nebularag.utils.text_processing import split_text
except ImportError as e:
    st.error(f"Import error: {e}")
    st.stop()

# Page configuration
st.set_page_config(
    page_title="NebulaRAG - AI Document Assistant (Demo)",
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
    
    .demo-notice {
        background-color: #fff3cd;
        border: 1px solid #ffeaa7;
        border-radius: 5px;
        padding: 1rem;
        margin: 1rem 0;
        color: #856404;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'documents_loaded' not in st.session_state:
    st.session_state.documents_loaded = False
if 'documents_count' not in st.session_state:
    st.session_state.documents_count = 0
if 'document_chunks' not in st.session_state:
    st.session_state.document_chunks = []

def load_documents_offline(docs_path: str, chunk_size: int = 800, chunk_overlap: int = 120) -> bool:
    """Load documents offline for demo purposes."""
    try:
        with st.spinner("🔄 Loading documents offline..."):
            # Read documents
            docs = read_text_files(docs_path)
            
            if not docs:
                st.error("❌ No documents found in the specified directory!")
                return False
            
            # Split documents into chunks
            all_chunks = []
            for doc in docs:
                chunks = split_text(doc, chunk_size=chunk_size, chunk_overlap=chunk_overlap)
                all_chunks.extend(chunks)
            
            # Store in session state
            st.session_state.documents_loaded = True
            st.session_state.documents_count = len(docs)
            st.session_state.document_chunks = all_chunks
            
            st.success(f"✅ Successfully loaded {len(docs)} documents and created {len(all_chunks)} chunks!")
            return True
            
    except Exception as e:
        st.error(f"❌ Error loading documents: {str(e)}")
        return False

def search_documents_offline(question: str, top_k: int = 3) -> List[str]:
    """Simple offline search by keyword matching."""
    if not st.session_state.document_chunks:
        return []
    
    question_lower = question.lower()
    question_words = question_lower.split()
    
    # Simple keyword matching
    scored_chunks = []
    for chunk in st.session_state.document_chunks:
        chunk_lower = chunk.lower()
        score = sum(1 for word in question_words if word in chunk_lower)
        if score > 0:
            scored_chunks.append((score, chunk))
    
    # Sort by score and return top-k
    scored_chunks.sort(key=lambda x: x[0], reverse=True)
    return [chunk for _, chunk in scored_chunks[:top_k]]

def generate_demo_answer(question: str, relevant_chunks: List[str]) -> str:
    """Generate a demo answer based on relevant chunks."""
    if not relevant_chunks:
        return "I couldn't find relevant information in the documents to answer your question. Please try rephrasing your question or check if the documents contain the information you're looking for."
    
    # Simple answer generation for demo
    if "7 testing principles" in question.lower() or "seven testing principles" in question.lower():
        return """
Based on the ISTQB documentation, here are the 7 fundamental testing principles:

1. **Testing shows the presence, not the absence of defects** - Testing can show that defects are present in the test object, but cannot prove that there are no defects.

2. **Exhaustive testing is impossible** - Testing everything is not feasible except in trivial cases. Rather than attempting to test exhaustively, test techniques, test case prioritization, and risk-based testing should be used to focus test efforts.

3. **Early testing saves time and money** - Defects that are removed early in the process will not cause subsequent defects in derived work products.

4. **Defects cluster together** - A small number of system components usually contain most of the defects discovered or are responsible for most of the operational failures.

5. **Tests wear out** - If the same tests are repeated many times, they become increasingly ineffective in detecting new defects.

6. **Testing is context dependent** - There is no single universally applicable approach to testing. Testing is done differently in different contexts.

7. **Absence-of-defects fallacy** - It is a fallacy to expect that software verification will ensure the success of a system.

*Note: This is a demo response. The actual RAG system would provide more detailed and accurate answers based on the full document content.*
        """
    
    # Generic response for other questions
    return f"""
Based on the documents, here's what I found related to your question:

{relevant_chunks[0][:500]}...

*Note: This is a demo response. The actual RAG system would provide more comprehensive answers using AI embeddings and reranking.*
    """

# Main UI
def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🤖 NebulaRAG - AI Document Assistant (Demo Mode)</h1>
        <p>Demo version - Works offline without API calls</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Demo notice
    st.markdown("""
    <div class="demo-notice">
        <strong>🚨 Demo Mode:</strong> This is an offline demo version. It uses simple keyword matching instead of AI embeddings. 
        The actual RAG system requires API access which is currently rate-limited.
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
        st.subheader("🔧 Parameters")
        chunk_size = st.slider("Chunk Size", 200, 2000, 800, 50)
        chunk_overlap = st.slider("Chunk Overlap", 50, 500, 120, 10)
        top_k = st.slider("Top-K Results", 1, 10, 3, 1)
        
        # Initialize button
        if st.button("🚀 Load Documents (Offline)", type="primary"):
            if load_documents_offline(docs_path, chunk_size, chunk_overlap):
                st.session_state.messages = []  # Clear previous messages
        
        # Status
        st.subheader("📊 Status")
        if st.session_state.documents_loaded:
            st.markdown(f'<p class="status-success">✅ Documents Loaded</p>', unsafe_allow_html=True)
            st.markdown(f'<p class="status-info">📚 {st.session_state.documents_count} documents loaded</p>', unsafe_allow_html=True)
            st.markdown(f'<p class="status-info">📄 {len(st.session_state.document_chunks)} chunks created</p>', unsafe_allow_html=True)
        else:
            st.markdown(f'<p class="status-error">❌ Documents Not Loaded</p>', unsafe_allow_html=True)
        
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
                    for i, source in enumerate(message["sources"][:3]):
                        st.text(f"Source {i+1}: {source[:200]}...")
    
    # Chat input
    if prompt := st.chat_input("Ask a question about your documents..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Generate and display assistant response
        if st.session_state.documents_loaded:
            with st.chat_message("assistant"):
                with st.spinner("🤔 Searching documents..."):
                    relevant_chunks = search_documents_offline(prompt, top_k)
                    response_content = generate_demo_answer(prompt, relevant_chunks)
                
                st.markdown(response_content)
                
                # Show sources
                if relevant_chunks:
                    with st.expander("📚 Sources"):
                        for i, chunk in enumerate(relevant_chunks[:3]):
                            st.text(f"Source {i+1}: {chunk[:200]}...")
            
            # Add assistant message to chat history
            st.session_state.messages.append({
                "role": "assistant", 
                "content": response_content,
                "sources": relevant_chunks
            })
        else:
            with st.chat_message("assistant"):
                st.error("❌ Documents not loaded. Please load documents in the sidebar first.")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 1rem;">
        <p>🚀 Powered by NebulaRAG | Demo Mode | Built with Streamlit</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
