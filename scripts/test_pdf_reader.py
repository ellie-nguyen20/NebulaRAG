"""
Test script for PDF reading functionality.
Usage: python scripts/test_pdf_reader.py [path_to_pdf_file]
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from nebularag.utils.file_utils import extract_text_from_pdf, read_text_files


def test_single_pdf(pdf_path: str):
    """Test reading a single PDF file."""
    print(f"\n{'='*60}")
    print(f"Testing PDF: {pdf_path}")
    print(f"{'='*60}\n")
    
    try:
        path = Path(pdf_path)
        if not path.exists():
            print(f"❌ File not found: {pdf_path}")
            return False
        
        if not path.name.lower().endswith('.pdf'):
            print(f"❌ Not a PDF file: {pdf_path}")
            return False
        
        # Extract text
        print("📖 Extracting text from PDF...")
        text = extract_text_from_pdf(path)
        
        # Display results
        print(f"✅ Success!")
        print(f"\n📊 Statistics:")
        print(f"   - Total characters: {len(text):,}")
        print(f"   - Total words: {len(text.split()):,}")
        print(f"   - Total lines: {len(text.splitlines()):,}")
        
        # Show preview
        print(f"\n📄 Preview (first 500 characters):")
        print("-" * 60)
        print(text[:500])
        if len(text) > 500:
            print("\n... (truncated)")
        print("-" * 60)
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def test_directory(dir_path: str):
    """Test reading all files (including PDFs) from a directory."""
    print(f"\n{'='*60}")
    print(f"Testing directory: {dir_path}")
    print(f"{'='*60}\n")
    
    try:
        print("📚 Loading all files (txt, md, pdf)...")
        documents = read_text_files(dir_path)
        
        print(f"\n✅ Success!")
        print(f"📊 Loaded {len(documents)} document(s)")
        
        total_chars = sum(len(doc) for doc in documents)
        print(f"   - Total characters: {total_chars:,}")
        print(f"   - Average doc size: {total_chars // len(documents):,} characters")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def main():
    """Main test function."""
    print("\n" + "="*60)
    print("  PDF Reader Test Script")
    print("="*60)
    
    # Check if PyPDF2 is installed
    try:
        from PyPDF2 import PdfReader
        print("\n✅ PyPDF2 is installed")
    except ImportError:
        print("\n❌ PyPDF2 is NOT installed")
        print("   Install it with: pip install PyPDF2>=3.0.0")
        return
    
    # Test based on arguments
    if len(sys.argv) > 1:
        test_path = sys.argv[1]
        path = Path(test_path)
        
        if path.is_file():
            test_single_pdf(test_path)
        elif path.is_dir():
            test_directory(test_path)
        else:
            print(f"\n❌ Invalid path: {test_path}")
    else:
        # Test with docs directory if no argument provided
        docs_dir = Path(__file__).parent.parent / "docs"
        if docs_dir.exists():
            test_directory(str(docs_dir))
        else:
            print("\nℹ️  Usage:")
            print(f"   python {Path(__file__).name} <path_to_pdf_or_directory>")
            print("\nExample:")
            print(f"   python {Path(__file__).name} docs/istqb_foundation.pdf")
            print(f"   python {Path(__file__).name} docs/")


if __name__ == "__main__":
    main()

