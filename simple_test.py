#!/usr/bin/env python3
"""
Simple test script for NebulaRAG
Tests basic functionality without complex imports
"""

import os
import sys
from pathlib import Path

# Add current directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

def test_imports():
    """Test if we can import the modules"""
    print("Testing imports...")
    try:
        from nebularag.clients.nebula_client import NebulaBlockClient
        from nebularag.core.rag_pipeline import RAGPipeline
        from nebularag.utils.file_utils import read_text_files
        print("✅ All imports successful!")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_api_connection():
    """Test API connection"""
    print("\nTesting API connection...")
    
    # Check if API key is set
    api_key = os.environ.get("NEBULABLOCK_API_KEY")
    if not api_key:
        print("❌ NEBULABLOCK_API_KEY not set")
        print("Please set your API key in .env file or environment")
        return False
    
    print(f"✅ API key found: {api_key[:10]}...{api_key[-4:]}")
    
    try:
        from nebularag.clients.nebula_client import NebulaBlockClient
        client = NebulaBlockClient()
        print("✅ Client initialized successfully")
        return True
    except Exception as e:
        print(f"❌ Client initialization failed: {e}")
        return False

def test_documents():
    """Test document reading"""
    print("\nTesting document reading...")
    try:
        from nebularag.utils.file_utils import read_text_files
        
        docs_dir = Path("docs")
        if not docs_dir.exists():
            print("❌ docs directory not found")
            return False
        
        docs = read_text_files(str(docs_dir))
        print(f"✅ Found {len(docs)} documents")
        
        for i, doc in enumerate(docs):
            print(f"  Document {i+1}: {len(doc)} characters")
        
        return True
    except Exception as e:
        print(f"❌ Document reading failed: {e}")
        return False

def test_basic_rag():
    """Test basic RAG functionality"""
    print("\nTesting basic RAG...")
    try:
        from nebularag.clients.nebula_client import NebulaBlockClient
        from nebularag.core.rag_pipeline import RAGPipeline
        from nebularag.utils.file_utils import read_text_files
        
        # Initialize client
        client = NebulaBlockClient()
        
        # Create RAG pipeline
        rag = RAGPipeline(client, chunk_size=400, top_k=5, rerank_k=3)
        
        # Read documents
        docs = read_text_files("docs")
        print(f"✅ Loaded {len(docs)} documents")
        
        # Index documents
        num_chunks = rag.index_texts(docs)
        print(f"✅ Indexed {num_chunks} chunks")
        
        # Ask a simple question
        question = "What is this document about?"
        print(f"Question: {question}")
        
        result = rag.answer(question)
        print(f"✅ Answer: {result['answer'][:100]}...")
        print(f"✅ Sources: {len(result['sources'])}")
        
        return True
    except Exception as e:
        print(f"❌ RAG test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 NEBULARAG SIMPLE TEST")
    print("=" * 50)
    
    tests = [
        test_imports,
        test_api_connection,
        test_documents,
        test_basic_rag,
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"❌ Test failed with exception: {e}")
            results.append(False)
    
    print("\n" + "=" * 50)
    print("TEST SUMMARY")
    print("=" * 50)
    
    passed = sum(results)
    total = len(results)
    
    print(f"Total tests: {total}")
    print(f"Passed: {passed}")
    print(f"Failed: {total - passed}")
    print(f"Success rate: {passed/total*100:.1f}%")
    
    if passed == total:
        print("🎉 All tests passed!")
        return 0
    else:
        print("❌ Some tests failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())
