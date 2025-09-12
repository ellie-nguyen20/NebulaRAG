# NebulaRAG Setup Guide

## Step 1: Install Dependencies

```bash
# Install dependencies
pip3 install -r requirements.txt

# Install package in development mode
pip3 install -e .
```

## Step 2: Configure Environment Variables

Create `.env` file in the root directory with the following content:

```bash
# NebulaBlock API Configuration
NEBULABLOCK_BASE_URL=https://dev-llm-proxy.nebulablock.com/v1
NEBULABLOCK_API_KEY=sk-your-api-key-here

# Optional API Endpoints (defaults shown)
NEBULABLOCK_EMBEDDINGS_PATH=/embeddings
NEBULABLOCK_RERANK_PATH=/rerank
NEBULABLOCK_CHAT_PATH=/chat/completions

# Model Configuration (defaults shown)
NEBULABLOCK_EMBEDDING_MODEL=Qwen/Qwen3-Embedding-8B
NEBULABLOCK_RERANKER_MODEL=BAAI/bge-reranker-v2-m3
NEBULABLOCK_CHAT_MODEL=Mistral-Small-24B-Instruct-2501

# RAG Pipeline Configuration (optional)
RAG_CHUNK_SIZE=800
RAG_CHUNK_OVERLAP=120
RAG_TOP_K=12
RAG_RERANK_K=6
HTTP_TIMEOUT=60.0
```

**Note**: Replace `sk-your-api-key-here` with your actual API key.

## Step 3: Test API Connection

```bash
python3 scripts/test_nebula.py
```

## Step 4: Run Basic Example

```bash
# Using CLI
nebularag --docs docs --question "What is this document about?"

# Or using Python module
python3 -m nebularag.cli.main --docs docs --question "What is this document about?"
```

## Step 5: Run Example Script

```bash
python3 examples/basic_usage.py
```

## Troubleshooting

1. **ModuleNotFoundError**: Make sure you've installed the package with `pip3 install -e .`
2. **API Key Error**: Check `NEBULABLOCK_API_KEY` in `.env` file
3. **Connection Error**: Check `NEBULABLOCK_BASE_URL` and internet connection
4. **Empty Results**: Make sure `docs/` directory contains `.txt` or `.md` files
