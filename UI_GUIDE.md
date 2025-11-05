# 🤖 NebulaRAG Web Interface Guide

## 🚀 Cách chạy giao diện web ChatGPT-like

### Bước 1: Cài đặt dependencies
```bash
pip install streamlit>=1.28.0
```

### Bước 2: Chạy ứng dụng web
```bash
streamlit run app.py
```

### Bước 3: Mở trình duyệt
- Truy cập: `http://localhost:8501`
- Giao diện sẽ tự động mở trong trình duyệt

## 🎨 Tính năng của giao diện

### ✨ **Giao diện ChatGPT-like**
- **Chat interface**: Giao diện chat giống ChatGPT
- **Message history**: Lưu lịch sử cuộc trò chuyện
- **Real-time responses**: Phản hồi real-time với loading animation
- **Source citations**: Hiển thị nguồn tài liệu được sử dụng

### ⚙️ **Configuration Panel (Sidebar)**
- **Documents Path**: Chọn thư mục chứa tài liệu
- **RAG Parameters**: Tùy chỉnh các tham số RAG
  - Chunk Size: Kích thước đoạn văn (200-2000)
  - Chunk Overlap: Độ chồng lấp (50-500)
  - Top-K: Số lượng kết quả tìm kiếm (5-30)
  - Rerank-K: Số lượng kết quả sau rerank (3-15)

### 📊 **Status Panel**
- **Pipeline Status**: Trạng thái hệ thống RAG
- **Documents Count**: Số lượng tài liệu đã load
- **Clear Chat**: Xóa lịch sử chat

### 💬 **Chat Features**
- **Question Input**: Nhập câu hỏi về tài liệu
- **Answer Display**: Hiển thị câu trả lời từ RAG
- **Source Display**: Hiển thị nguồn tài liệu được sử dụng
- **Error Handling**: Xử lý lỗi một cách thân thiện

## 🎯 **Cách sử dụng**

### 1. **Khởi tạo hệ thống**
- Chọn đường dẫn tài liệu (mặc định: `docs`)
- Tùy chỉnh các tham số RAG nếu cần
- Nhấn "🚀 Initialize RAG Pipeline"

### 2. **Đặt câu hỏi**
- Nhập câu hỏi vào ô chat
- Nhấn Enter hoặc nút gửi
- Chờ hệ thống xử lý và trả lời

### 3. **Xem kết quả**
- Câu trả lời sẽ hiển thị trong chat
- Nhấn "📚 Sources" để xem nguồn tài liệu
- Tiếp tục đặt câu hỏi khác

## 🔧 **Troubleshooting**

### Lỗi thường gặp:
1. **"RAG pipeline not initialized"**
   - Giải pháp: Nhấn "Initialize RAG Pipeline" trong sidebar

2. **"No documents found"**
   - Giải pháp: Kiểm tra đường dẫn tài liệu và đảm bảo có file .txt, .md, .pdf

3. **"API Error"**
   - Giải pháp: Kiểm tra API key và URL trong file .env

4. **"Streamlit not found"**
   - Giải pháp: Cài đặt streamlit: `pip install streamlit`

## 🌟 **Ví dụ sử dụng**

### Câu hỏi mẫu:
- "What are the 7 testing principles in ISTQB?"
- "Explain black box testing techniques"
- "What is the difference between verification and validation?"
- "Summarize the main topics in the documentation"

### Tùy chỉnh nâng cao:
- Thay đổi chunk size để tối ưu cho tài liệu dài
- Điều chỉnh top-k để lấy nhiều/ít kết quả hơn
- Sử dụng rerank-k để cải thiện độ chính xác

## 🎨 **Customization**

Bạn có thể tùy chỉnh giao diện bằng cách:
- Sửa file `app.py`
- Thay đổi CSS styling
- Thêm tính năng mới
- Tùy chỉnh màu sắc và layout

## 📱 **Responsive Design**

Giao diện được thiết kế responsive:
- Hoạt động tốt trên desktop
- Tương thích với tablet
- Giao diện mobile-friendly

---

**🚀 Enjoy your AI Document Assistant!**
