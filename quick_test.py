#!/usr/bin/env python3
"""
Quick test script for NebulaRAG
Run this to test the basic functionality
"""

import os
import sys
from pathlib import Path

# Add the current directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

def test_imports():
    """Test if all modules can be imported"""
    print("Testing imports...")
    try:
        from nebularag.core import RAGPipeline, InMemoryVectorStore
        from nebularag.clients import NebulaBlockClient
        from nebularag.utils import read_text_files, split_text
        from nebularag.config import get_settings
        print("✓ All imports successful!")
        return True
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False

def test_text_processing():
    """Test text processing utilities"""
    print("\nTesting text processing...")
    try:
        from nebularag.utils.text_processing import split_text, clean_text
        
        # Test text splitting
        sample_text = "This is a sample document. It has multiple sentences. Each sentence should be split properly."
        chunks = split_text(sample_text, chunk_size=30, chunk_overlap=5)
        print(f"✓ Text splitting works: {len(chunks)} chunks created")
        
        # Test text cleaning
        dirty_text = "  This   has   extra   spaces  \n\n  "
        clean = clean_text(dirty_text)
        print(f"✓ Text cleaning works: '{clean}'")
        return True
    except Exception as e:
        print(f"✗ Text processing error: {e}")
        return False

def test_vector_store():
    """Test vector store functionality"""
    print("\nTesting vector store...")
    try:
        from nebularag.core.vector_store import InMemoryVectorStore, cosine_similarity
        
        # Test cosine similarity
        vec1 = [1, 0, 0]
        vec2 = [0, 1, 0]
        similarity = cosine_similarity(vec1, vec2)
        print(f"✓ Cosine similarity works: {similarity}")
        
        # Test vector store
        store = InMemoryVectorStore()
        texts = ["hello world", "goodbye world"]
        embeddings = [[1, 0], [0, 1]]
        store.add(texts, embeddings)
        print(f"✓ Vector store works: {store.size()} vectors stored")
        return True
    except Exception as e:
        print(f"✗ Vector store error: {e}")
        return False

def test_file_utils():
    """Test file utilities"""
    print("\nTesting file utilities...")
    try:
        from nebularag.utils.file_utils import read_text_files
        
        # Check if docs directory exists
        docs_dir = Path(__file__).parent / "docs"
        if docs_dir.exists():
            docs = read_text_files(str(docs_dir))
            print(f"✓ File reading works: {len(docs)} documents found")
        else:
            print("⚠ Docs directory not found, skipping file test")
        return True
    except Exception as e:
        print(f"✗ File utilities error: {e}")
        return False

def test_config():
    """Test configuration"""
    print("\nTesting configuration...")
    try:
        from nebularag.config import get_settings
        
        # Test settings loading
        settings = get_settings()
        print(f"✓ Configuration loaded")
        print(f"  - Base URL: {settings.nebula_base_url}")
        print(f"  - Embedding Model: {settings.embedding_model}")
        print(f"  - Chunk Size: {settings.default_chunk_size}")
        return True
    except Exception as e:
        print(f"✗ Configuration error: {e}")
        return False

def main():
    """Run all tests"""
    print("NebulaRAG Quick Test")
    print("=" * 40)
    
    tests = [
        test_imports,
        test_text_processing,
        test_vector_store,
        test_file_utils,
        test_config,
    ]
    
    results = []
    for test in tests:
        results.append(test())
    
    print("\n" + "=" * 40)
    print("Test Summary:")
    passed = sum(results)
    total = len(results)
    print(f"Passed: {passed}/{total}")
    
    if passed == total:
        print("✓ All tests passed! You can now use NebulaRAG.")
        print("\nNext steps:")
        print("1. Set up your .env file with API credentials")
        print("2. Run: python3 scripts/test_nebula.py")
        print("3. Run: nebularag --docs docs --question 'Your question'")
    else:
        print("✗ Some tests failed. Please check the errors above.")
    
    return 0 if passed == total else 1

if __name__ == "__main__":
    sys.exit(main())
