# 📚 Hướng Dẫn Sử Dụng NebulaRAG cho Học ISTQB

## 🎯 Giới Thiệu

NebulaRAG giúp bạn học ISTQB hiệu quả hơn bằng cách cho phép bạn hỏi đáp trực tiếp với tài liệu PDF của mình. Thay vì phải đọc cả cuốn sách dày, bạn có thể hỏi những câu hỏi cụ thể và nhận được câu trả lời từ chính tài liệu.

## 🚀 Bắt Đầu Nhanh

### Bước 1: Cài Đặt

```bash
# Clone repository (nếu chưa có)
cd /Users/LENOVO/ellienguyen/rag-example

# Cài đặt dependencies (bao gồm PyPDF2)
pip install -e .
```

### Bước 2: Cấu Hình API

Tạo file `.env` trong thư mục gốc:

```bash
NEBULABLOCK_BASE_URL=https://dev-llm-proxy.nebulablock.com/v1
NEBULABLOCK_API_KEY=sk-your-api-key-here
```

### Bước 3: Thêm Tài Liệu ISTQB

```bash
# Tạo thư mục cho tài liệu ISTQB (nếu chưa có)
mkdir -p docs/istqb

# Copy các file PDF ISTQB vào thư mục
# Ví dụ:
# - docs/istqb/ISTQB_Foundation_Level.pdf
# - docs/istqb/ISTQB_Test_Analyst.pdf
# - docs/istqb/ISTQB_Technical_Test_Analyst.pdf
```

### Bước 4: Test Đọc PDF

```bash
# Test xem PDF có đọc được không
python scripts/test_pdf_reader.py docs/istqb/
```

### Bước 5: Bắt Đầu Học!

```bash
# Hỏi câu hỏi về nội dung ISTQB
nebularag --docs docs/istqb --question "7 nguyên tắc kiểm thử là gì?"
```

## 💡 Ví Dụ Câu Hỏi cho ISTQB Foundation Level

### Về Các Khái Niệm Cơ Bản

```bash
nebularag --docs docs/istqb --question "Sự khác biệt giữa verification và validation là gì?"

nebularag --docs docs/istqb --question "Giải thích về 7 nguyên tắc kiểm thử (7 testing principles)"

nebularag --docs docs/istqb --question "Test case gồm những thành phần nào?"
```

### Về Kỹ Thuật Kiểm Thử

```bash
nebularag --docs docs/istqb --question "Equivalence partitioning là gì? Cho ví dụ"

nebularag --docs docs/istqb --question "Boundary value analysis hoạt động như thế nào?"

nebularag --docs docs/istqb --question "So sánh white box và black box testing"

nebularag --docs docs/istqb --question "Decision table testing được sử dụng khi nào?"
```

### Về Quy Trình Kiểm Thử

```bash
nebularag --docs docs/istqb --question "Các giai đoạn trong test process là gì?"

nebularag --docs docs/istqb --question "Entry criteria và exit criteria là gì?"

nebularag --docs docs/istqb --question "Test strategy vs test plan khác nhau thế nào?"
```

### Về Test Levels và Test Types

```bash
nebularag --docs docs/istqb --question "Các test levels trong ISTQB là gì?"

nebularag --docs docs/istqb --question "Integration testing có những approach nào?"

nebularag --docs docs/istqb --question "Functional testing và non-functional testing khác nhau như thế nào?"
```

## 🎨 Tùy Chỉnh Nâng Cao

### Điều Chỉnh Độ Chính Xác

```bash
# Lấy nhiều thông tin hơn từ tài liệu
nebularag \
  --docs docs/istqb \
  --question "Giải thích về test automation" \
  --top-k 20 \
  --rerank-k 10
```

### Điều Chỉnh Kích Thước Chunk

```bash
# Với tài liệu dày, tăng chunk size để giữ ngữ cảnh
nebularag \
  --docs docs/istqb \
  --question "Test management tools có chức năng gì?" \
  --chunk-size 1200 \
  --chunk-overlap 200
```

## 📝 Tips Học Hiệu Quả

### 1. Hỏi Câu Hỏi Cụ Thể

❌ Không tốt: "Nói về testing"  
✅ Tốt: "7 nguyên tắc kiểm thử trong ISTQB là gì?"

### 2. Chia Nhỏ Topic

Thay vì hỏi "Nói tất cả về test design techniques", hãy chia nhỏ:
- "Equivalence partitioning là gì?"
- "Boundary value analysis là gì?"
- "Decision table testing là gì?"

### 3. Yêu Cầu Ví Dụ

```bash
nebularag --docs docs/istqb --question "Cho ví dụ về boundary value analysis với input từ 1-100"
```

### 4. So Sánh Khái Niệm

```bash
nebularag --docs docs/istqb --question "So sánh regression testing và retesting"
```

### 5. Tạo Flashcards

Sử dụng câu trả lời để tạo flashcards cho việc ôn tập:

```bash
# Lưu câu trả lời vào file
nebularag --docs docs/istqb --question "7 testing principles là gì?" > flashcard_principles.txt
```

## 🔧 Troubleshooting

### PDF Không Load Được

```bash
# Kiểm tra xem PyPDF2 đã được cài chưa
pip list | grep PyPDF2

# Nếu chưa có, cài đặt
pip install PyPDF2>=3.0.0
```

### Kết Quả Không Chính Xác

1. **Tăng số lượng documents được retrieve**:
   ```bash
   nebularag --docs docs/istqb --question "..." --top-k 20 --rerank-k 10
   ```

2. **Kiểm tra tài liệu đã được load**:
   ```bash
   python scripts/test_pdf_reader.py docs/istqb/
   ```

3. **Hỏi câu hỏi cụ thể hơn**

### API Lỗi

```bash
# Test kết nối API
python scripts/test_nebula.py
```

## 🎓 Lộ Trình Học ISTQB với NebulaRAG

### Tuần 1-2: Foundation Concepts
- Testing fundamentals
- Testing throughout SDLC
- Static testing

### Tuần 3-4: Test Design Techniques
- Black-box techniques
- White-box techniques
- Experience-based techniques

### Tuần 5-6: Test Management
- Test planning
- Test monitoring and control
- Configuration management

### Tuần 7-8: Tool Support
- Tool categories
- Tool selection
- Tool lifecycle

## 📊 Theo Dõi Tiến Độ

Tạo một file để track câu hỏi và câu trả lời:

```bash
# Tạo thư mục study notes
mkdir -p study_notes

# Lưu Q&A theo chủ đề
echo "Q: 7 testing principles là gì?" >> study_notes/chapter1.txt
nebularag --docs docs/istqb --question "7 testing principles là gì?" >> study_notes/chapter1.txt
```

## 🎯 Mẹo Thi ISTQB

1. **Review các định nghĩa**: Hỏi định nghĩa chính xác của các thuật ngữ
2. **Hiểu sự khác biệt**: So sánh các khái niệm tương tự
3. **Nhớ ví dụ**: Yêu cầu ví dụ cụ thể cho từng kỹ thuật
4. **Practice questions**: Sau khi học, làm đề thi thử

## 🤝 Hỗ Trợ

Nếu gặp vấn đề, check:
- README.md - Hướng dẫn chi tiết
- scripts/test_pdf_reader.py - Test PDF reading
- scripts/test_nebula.py - Test API connection

---

**Chúc bạn học tốt và pass ISTQB! 🎉**

