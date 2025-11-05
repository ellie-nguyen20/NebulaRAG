"""File handling utilities."""

import os
import sys
from pathlib import Path
from typing import List, Tuple

try:
    from PyPDF2 import PdfReader
    PDF_SUPPORT = True
except ImportError:
    PDF_SUPPORT = False
    print("Warning: PyPDF2 not installed. PDF support disabled.", file=sys.stderr)


def validate_directory(dir_path: str) -> Path:
    """
    Validate that a directory exists and is accessible.
    
    Args:
        dir_path: Path to the directory to validate
        
    Returns:
        Path object for the validated directory
        
    Raises:
        FileNotFoundError: If the directory doesn't exist
        ValueError: If the path is not a directory
        PermissionError: If the directory is not accessible
    """
    dir_path = Path(dir_path)
    
    if not dir_path.exists():
        raise FileNotFoundError(f"Directory not found: {dir_path}")
    
    if not dir_path.is_dir():
        raise ValueError(f"Path is not a directory: {dir_path}")
    
    if not os.access(dir_path, os.R_OK):
        raise PermissionError(f"Directory is not readable: {dir_path}")
    
    return dir_path


def extract_text_from_pdf(file_path: Path) -> str:
    """
    Extract text from a PDF file.
    
    Args:
        file_path: Path to the PDF file
        
    Returns:
        Extracted text as a string
        
    Raises:
        ImportError: If PyPDF2 is not installed
        Exception: If PDF cannot be read
    """
    if not PDF_SUPPORT:
        raise ImportError("PyPDF2 is required for PDF support. Install it with: pip install PyPDF2")
    
    try:
        reader = PdfReader(str(file_path))
        text_parts = []
        
        for page_num, page in enumerate(reader.pages, 1):
            try:
                text = page.extract_text()
                if text.strip():
                    text_parts.append(text.strip())
            except Exception as e:
                print(f"Warning: Could not extract text from page {page_num} of {file_path}: {e}", file=sys.stderr)
                continue
        
        return "\n\n".join(text_parts)
    except Exception as e:
        raise Exception(f"Error reading PDF {file_path}: {e}")


def read_text_files(dir_path: str, exts: Tuple[str, ...] = (".txt", ".md", ".pdf")) -> List[str]:
    """
    Read all text files from a directory and its subdirectories.
    Supports .txt, .md, and .pdf files.
    
    Args:
        dir_path: Path to the directory containing text files
        exts: Tuple of file extensions to include (case-insensitive)
        
    Returns:
        List of file contents as strings
        
    Raises:
        FileNotFoundError: If the directory doesn't exist
        ValueError: If no readable files are found
    """
    dir_path = validate_directory(dir_path)
    
    out: List[str] = []
    for file_path in dir_path.rglob("*"):
        if file_path.is_file() and any(file_path.name.lower().endswith(ext) for ext in exts):
            try:
                # Handle PDF files
                if file_path.name.lower().endswith(".pdf"):
                    if not PDF_SUPPORT:
                        print(f"Warning: Skipping PDF {file_path} - PyPDF2 not installed", file=sys.stderr)
                        continue
                    content = extract_text_from_pdf(file_path)
                # Handle text files
                else:
                    with open(file_path, "r", encoding="utf-8") as fh:
                        content = fh.read().strip()
                
                if content:  # Only add non-empty files
                    out.append(content)
                    print(f"✓ Loaded: {file_path.name} ({len(content)} characters)")
            except (UnicodeDecodeError, PermissionError, OSError) as e:
                print(f"Warning: Could not read {file_path}: {e}", file=sys.stderr)
                continue
            except Exception as e:
                print(f"Warning: Error processing {file_path}: {e}", file=sys.stderr)
                continue
    
    if not out:
        raise ValueError(f"No readable text files found in {dir_path}")
    
    return out


def get_file_info(file_path: str) -> dict:
    """
    Get information about a file.
    
    Args:
        file_path: Path to the file
        
    Returns:
        Dictionary with file information
    """
    path = Path(file_path)
    stat = path.stat()
    
    return {
        "name": path.name,
        "size": stat.st_size,
        "modified": stat.st_mtime,
        "extension": path.suffix,
        "is_file": path.is_file(),
        "is_dir": path.is_dir(),
    }
