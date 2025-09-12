# 🧪 RAG Test Scenarios - 15 Test Cases

## 📋 **Overview**

This test suite is designed to comprehensively evaluate the performance and reliability of the NebulaRAG model.

## 🔍 **1. Basic Tests (4 test cases)**

### **Test 1: API Connection**
```bash
python3 scripts/test_nebula.py
```
**Purpose**: Check connection to NebulaBlock API
**Expected**: All endpoints (embeddings, rerank, chat) working
**Time**: ~30s

### **Test 2: Module Import**
```bash
python3 quick_test.py
```
**Purpose**: Check if all modules can be imported
**Expected**: No import errors
**Time**: ~5s

### **Test 3: Basic Question**
```bash
nebularag --docs docs --question "What is this document about?"
```
**Purpose**: Test basic pipeline
**Expected**: Return meaningful answer
**Time**: ~15s

### **Test 4: Out-of-scope Question**
```bash
nebularag --docs docs --question "What is quantum computing?"
```
**Purpose**: Test handling of unrelated questions
**Expected**: Return "I don't know" or similar
**Time**: ~15s

## ⚙️ **2. Parameter Tests (4 test cases)**

### **Test 5: Small Chunks**
```bash
nebularag --docs docs --question "What is the main topic?" --chunk-size 200 --chunk-overlap 50
```
**Purpose**: Test with small chunks
**Expected**: More chunks, may lose context
**Time**: ~20s

### **Test 6: Large Chunks**
```bash
nebularag --docs docs --question "What is the main topic?" --chunk-size 1500 --chunk-overlap 200
```
**Purpose**: Test with large chunks
**Expected**: Fewer chunks, better context
**Time**: ~20s

### **Test 7: Low Top-K**
```bash
nebularag --docs docs --question "What is the main topic?" --top-k 3 --rerank-k 2
```
**Purpose**: Test with few results
**Expected**: Concise answer
**Time**: ~15s

### **Test 8: High Top-K**
```bash
nebularag --docs docs --question "What is the main topic?" --top-k 20 --rerank-k 10
```
**Purpose**: Test with many results
**Expected**: Comprehensive answer, may have noise
**Time**: ~25s

## ❓ **3. Question Type Tests (4 test cases)**

### **Test 9: Specific Question**
```bash
nebularag --docs docs --question "What are the specific steps in the pipeline flow?"
```
**Purpose**: Test ability to answer detailed questions
**Expected**: Return specific information with sources
**Time**: ~15s

### **Test 10: Comparison Question**
```bash
nebularag --docs docs --question "Compare the different approaches mentioned in the documents"
```
**Purpose**: Test analysis and comparison capabilities
**Expected**: Return structured analysis
**Time**: ~15s

### **Test 11: Open Question**
```bash
nebularag --docs docs --question "What can you tell me about this topic?"
```
**Purpose**: Test ability to provide comprehensive overview
**Expected**: Return comprehensive overview
**Time**: ~15s

### **Test 12: Negative Question**
```bash
nebularag --docs docs --question "What is NOT mentioned in the documents?"
```
**Purpose**: Test ability to handle negative questions
**Expected**: Return information about what's not present
**Time**: ~15s

## 📄 **4. Document Tests (3 test cases)**

### **Test 13: Empty Documents**
```bash
mkdir empty_docs
nebularag --docs empty_docs --question "What is this about?"
```
**Purpose**: Test handling of empty documents
**Expected**: Report error or no documents message
**Time**: ~5s

### **Test 14: Large Document**
```bash
# Create large file first
python3 -c "
with open('docs/large_doc.txt', 'w') as f:
    for i in range(100):
        f.write(f'This is paragraph {i}. It contains information about topic {i%10}.\n')
"
nebularag --docs docs --question "What are the main topics in the large document?"
```
**Purpose**: Test performance with large documents
**Expected**: Process successfully, reasonable time
**Time**: ~30s

### **Test 15: Multiple File Types**
```bash
echo "This is a text file about machine learning." > docs/test.txt
echo "# Markdown File\n\nThis is a markdown file about AI." > docs/test.md
nebularag --docs docs --question "What types of files are processed?"
```
**Purpose**: Test handling of multiple file formats
**Expected**: Read both .txt and .md files
**Time**: ~15s

## 🚀 **How to Run All Tests**

### **Automated (Recommended)**
```bash
python3 scripts/run_all_tests.py
```

### **Manual**
Run each test one by one in order from Test 1 to Test 15.

## 📊 **Result Evaluation**

### **Success Metrics**
- **API Tests**: 100% pass
- **Basic Tests**: 100% pass
- **Parameter Tests**: 80% pass (may have variations)
- **Question Tests**: 70% pass (depends on answer quality)
- **Document Tests**: 90% pass

### **Total Time**
- **All tests**: ~5-10 minutes
- **Basic tests**: ~1 minute
- **Advanced tests**: ~4-9 minutes

### **Important Notes**
1. **API Key**: Must have valid API key
2. **Internet**: Need stable connection
3. **Documents**: Need at least 1 file in docs/
4. **Time**: Some tests may timeout if API is slow

## 🔧 **Troubleshooting**

### **Common Issues**
1. **API Key Error**: Check .env file
2. **Timeout**: Increase HTTP_TIMEOUT in .env
3. **Empty Results**: Check documents in docs/
4. **Import Error**: Run `pip3 install -e .`

### **Optimization**
1. **Chunk Size**: Customize based on document type
2. **Top-K**: Balance between accuracy and speed
3. **Models**: Try different models
4. **Caching**: Implement caching for production