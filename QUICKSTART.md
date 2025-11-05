# 🚀 Quick Start Guide

## Setup trong 3 phút

### 1. Cài đặt Dependencies

```bash
cd /Users/LENOVO/ellienguyen/rag-example

# Cài đặt với pip user (không cần venv)
python3 -m pip install --user PyPDF2 requests numpy python-dotenv

# Hoặc nếu muốn dùng virtual environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Setup API Key

```bash
# Copy file mẫu
cp .env.example .env

# Mở và sửa file .env, thay đổi dòng này:
# NEBULABLOCK_API_KEY=sk-your-api-key-here
# thành API key thực của bạn
```

**Cách lấy API Key:**
- Truy cập https://nebulablock.com hoặc portal của NebulaBlock
- Đăng ký/Đăng nhập
- Tạo API key mới
- Copy và paste vào file `.env`

### 3. Chạy Thử

```bash
# Test với documents có sẵn
python3 -m nebularag.cli.main \
  --docs docs \
  --question "What is the main topic of the documentation?"

# Hoặc với câu hỏi tiếng Việt
python3 -m nebularag.cli.main \
  --docs docs \
  --question "Tài liệu này nói về chủ đề gì?"
```

## 📚 Sử dụng với PDF ISTQB

### Bước 1: Thêm file PDF

```bash
# Copy file PDF ISTQB vào thư mục docs
cp /path/to/ISTQB_Foundation.pdf docs/
```

### Bước 2: Test đọc PDF

```bash
# Kiểm tra xem PDF có đọc được không
python3 scripts/test_pdf_reader.py docs/
```

### Bước 3: Hỏi câu hỏi

```bash
python3 -m nebularag.cli.main \
  --docs docs \
  --question "7 nguyên tắc kiểm thử trong ISTQB là gì?"
```

## 🎯 Ví dụ Câu Lệnh

### Câu hỏi đơn giản
```bash
python3 -m nebularag.cli.main \
  --docs docs \
  --question "Verification và validation khác nhau như thế nào?"
```

### Với tùy chỉnh nâng cao
```bash
python3 -m nebularag.cli.main \
  --docs docs \
  --question "Giải thích equivalence partitioning" \
  --chunk-size 1000 \
  --chunk-overlap 150 \
  --top-k 15 \
  --rerank-k 8
```

## ⚡ Troubleshooting

### Lỗi: PyPDF2 not installed
```bash
python3 -m pip install --user PyPDF2
```

### Lỗi: ModuleNotFoundError
```bash
# Cài đặt tất cả dependencies
python3 -m pip install --user -r requirements.txt
```

### Lỗi: API Key Error
- Kiểm tra file `.env` đã tạo chưa
- Kiểm tra API key đã đúng chưa
- Đảm bảo không có khoảng trắng thừa

### Test kết nối API
```bash
python3 scripts/test_nebula.py
```

## 📖 Tài liệu chi tiết

- **README.md** - Hướng dẫn đầy đủ
- **ISTQB_GUIDE.md** - Hướng dẫn học ISTQB
- **setup.py** - Cấu hình package

---

**Tip:** Thêm alias vào shell của bạn để dễ sử dụng:

```bash
# Thêm vào ~/.zshrc hoặc ~/.bashrc
alias nebularag='python3 -m nebularag.cli.main'

# Sau đó chỉ cần gõ:
nebularag --docs docs --question "Your question here"
```

