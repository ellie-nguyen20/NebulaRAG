# NebulaRAG

A minimal, dependency-light RAG (Retrieval-Augmented Generation) pipeline designed to work with NebulaBlock's Inference API. This project demonstrates how to build a complete RAG system with document indexing, semantic search, reranking, and answer generation.

## 🚀 Features

- **Lightweight**: Minimal dependencies, no heavy ML frameworks
- **PDF Support**: Read and process PDF documents directly
- **Configurable**: Environment-based configuration for all endpoints and models
- **OpenAI-Compatible**: Works with OpenAI-compatible APIs
- **Complete Pipeline**: Document splitting → embedding → retrieval → reranking → generation
- **CLI Interface**: Easy-to-use command-line interface
- **In-Memory Store**: Fast vector similarity search with cosine similarity

## 📋 Requirements

- Python 3.8+
- NebulaBlock API access
- Internet connection for API calls

## 🛠️ Installation

### Option 1: Development Installation (Recommended)

```bash
# Clone the repository
git clone <repository-url>
cd rag-example

# Install in development mode
pip install -e .
```

### Option 2: Direct Usage

```bash
# Clone the repository
git clone <repository-url>
cd rag-example

# Install dependencies
pip install -r requirements.txt

# Run directly
python -m nebularag.cli.main --help
```

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the project root with the following variables:

```bash
# Required
NEBULABLOCK_BASE_URL=https://dev-llm-proxy.nebulablock.com/v1
NEBULABLOCK_API_KEY=sk-your-api-key-here

# Optional (defaults shown)
NEBULABLOCK_EMBEDDINGS_PATH=/embeddings
NEBULABLOCK_RERANK_PATH=/rerank
NEBULABLOCK_CHAT_PATH=/chat/completions
NEBULABLOCK_EMBEDDING_MODEL=Qwen/Qwen3-Embedding-8B
NEBULABLOCK_RERANKER_MODEL=BAAI/bge-reranker-v2-m3
NEBULABLOCK_CHAT_MODEL=Mistral-Small-24B-Instruct-2501
```

### Default Models

- **Embedding**: Qwen/Qwen3-Embedding-8B
- **Reranker**: BAAI/bge-reranker-v2-m3  
- **Chat**: Mistral-Small-24B-Instruct-2501

## 📁 Project Structure

```
rag-example/
├── nebularag/            # Main package
│   ├── cli/              # Command-line interface
│   ├── clients/          # External API clients
│   ├── config/           # Configuration management
│   ├── core/             # Core RAG components
│   └── utils/            # Utility functions
├── scripts/              # Utility scripts
│   └── test_nebula.py    # API testing script
├── docs/                 # Sample documents
│   └── sample.md         # Example markdown file
├── setup.py              # Package configuration
├── requirements.txt      # Python dependencies
├── .env.example          # Environment template
└── README.md             # This file
```

## 🚀 Usage

### Basic Usage

1. **Prepare your documents**: Place `.txt`, `.md`, or `.pdf` files in a directory (e.g., `docs/`)
   - ✅ Supported formats: `.txt`, `.md`, `.pdf`
   - 📚 Perfect for studying with PDF textbooks or documentation

2. **Set up environment**: Copy `.env.example` to `.env` and fill in your API credentials

3. **Run the RAG pipeline**:
   ```bash
   nebularag --docs docs --question "What does the guide say about X?"
   ```

### Using with PDF Files (e.g., ISTQB Study Materials)

```bash
# Example: Study ISTQB Foundation Level
# 1. Place your ISTQB PDF in the docs folder
# 2. Ask questions about the content
nebularag --docs docs --question "What are the 7 testing principles in ISTQB?"
nebularag --docs docs --question "Explain black box testing techniques"
nebularag --docs docs --question "What is the difference between verification and validation?"
```

### Advanced Usage

```bash
# Custom chunk size and overlap
nebularag \
  --docs docs \
  --question "Your question here" \
  --chunk-size 1000 \
  --chunk-overlap 150 \
  --top-k 15 \
  --rerank-k 8
```

### CLI Options

| Option | Description | Default |
|--------|-------------|---------|
| `--docs` | Path to documents directory | Required |
| `--question` | Question to ask | Required |
| `--chunk-size` | Size of text chunks | 800 |
| `--chunk-overlap` | Overlap between chunks | 120 |
| `--top-k` | Number of candidates to retrieve | 12 |
| `--rerank-k` | Number of candidates after reranking | 6 |

### Testing the API

Test your NebulaBlock API connection:

```bash
python scripts/test_nebula.py
```

## 🔧 How It Works

### RAG Pipeline Flow

1. **Document Processing**: 
   - Reads `.txt`, `.md`, and `.pdf` files from the specified directory
   - Extracts text from PDFs using PyPDF2
   - Splits documents into overlapping chunks (default: 800 chars, 120 overlap)

2. **Indexing**:
   - Generates embeddings for each chunk using the embedding model
   - Stores embeddings in an in-memory vector store with cosine similarity

3. **Retrieval**:
   - Embeds the user question
   - Retrieves top-K most similar chunks by cosine similarity

4. **Reranking**:
   - Sends retrieved candidates to the reranker model
   - Reranks based on relevance to the question
   - Selects top rerank-K candidates

5. **Generation**:
   - Combines reranked chunks as context
   - Sends context + question to the chat model
   - Returns the generated answer with source citations

### API Compatibility

The client assumes OpenAI/Cohere-like JSON structures but keeps endpoints configurable:

- **Embeddings**: `POST /embeddings` with `{"model": "...", "input": [...]}`
- **Reranking**: `POST /rerank` with `{"model": "...", "query": "...", "documents": [...]}`
- **Chat**: `POST /chat/completions` with `{"model": "...", "messages": [...]}`

## 🧪 Examples

### Example 1: Basic Question Answering

```bash
# With sample documents
nebularag \
  --docs docs \
  --question "What is the main topic of the documentation?"
```

### Example 2: Using OpenAI SDK (Alternative)

If you prefer the official OpenAI client:

```python
from openai import OpenAI
import os

client = OpenAI(
    base_url=os.environ["NEBULABLOCK_BASE_URL"],
    api_key=os.environ["NEBULABLOCK_API_KEY"]
)

# Embedding
response = client.embeddings.create(
    model=os.environ["NEBULABLOCK_EMBEDDING_MODEL"],
    input=["hello world"]
)

# Chat
response = client.chat.completions.create(
    model=os.environ["NEBULABLOCK_CHAT_MODEL"],
    messages=[{"role": "user", "content": "Hi"}]
)
```

## 🛠️ Development

### Running Tests

```bash
# Test API connectivity
python scripts/test_nebula.py

# Test imports
python -c "from rag_example import NebulaBlockClient, RAGPipeline; print('Import successful!')"
```

### Adding New Features

1. **New Vector Store**: Implement the interface in `store.py`
2. **New Splitters**: Add functions to `splitter.py`
3. **New Clients**: Extend `nebula_client.py` or create new client classes

## 📝 Notes

- This is a reference implementation for learning and prototyping
- For production use, consider:
  - Persistent vector databases (Pinecone, Weaviate, etc.)
  - Semantic chunking strategies
  - Caching mechanisms
  - Error handling and retries
  - Rate limiting
- The reranker endpoint assumes Cohere-like structure
- All API calls are synchronous; async support can be added for better performance

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Troubleshooting

### Common Issues

1. **ModuleNotFoundError**: Make sure you've installed the package with `pip install -e .`
2. **API Key Error**: Verify your `NEBULABLOCK_API_KEY` is set correctly
3. **Connection Error**: Check your `NEBULABLOCK_BASE_URL` and internet connection
4. **Empty Results**: Ensure your documents directory contains `.txt`, `.md`, or `.pdf` files
5. **PDF Not Loading**: If you see "PyPDF2 not installed", run `pip install PyPDF2>=3.0.0`

### Getting Help

- Check the [Issues](https://github.com/your-repo/issues) page
- Review the API documentation for NebulaBlock
- Test your API connection with `python scripts/test_nebula.py`