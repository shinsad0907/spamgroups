# ⚡ HƯỚNG DẪN NHANH - HỆ THỐNG KEY

## 🚀 Test nhanh chóng

### Bước 1: Tạo file key test
Copy file mẫu và rename:

```bash
/data/key.json.example  →  /data/key.json
```

Hoặc tạo file `data/key.json` với nội dung:
```json
{
  "key": "TESTKEY123",
  "use": true,
  "expire_date": "2025-12-31",
  "created_at": "2025-04-01T00:00:00"
}
```

### Bước 2: Chạy ứng dụng
```bash
python main.py
```

### Bước 3: Chuỗi workflow

**Lần đầu (chưa có key):**
1. ✅ Dialog "KÍCH HOẠT PHẦN MỀM" hiển thị
2. 📋 Copy mã máy
3. 📌 Nhập key: `TESTKEY123`
4. ✅ "Key kích hoạt thành công" → ứng dụng mở

**Lần sau (có key hợp lệ):**
1. ✅ Ứng dụng mở ngay (không show dialog)

**Nếu key sai:**
1. Nhập key sai
2. ❌ Thông báo lỗi
3. 🔄 Input được xóa, yêu cầu nhập lại

## 🧪 Chạy test toàn chứng năng

```bash
python test_key.py
```

Kết quả expected:
```
════════════════════════════════════════════════════════════
TEST HỆ THỐNG KEY
════════════════════════════════════════════════════════════

[TEST 1] Xóa file key cũ...
✅ Đã xóa file key cũ

[TEST 2] Check key khi chưa có file...
Result: is_valid=False, message='Chưa có key - Vui lòng nhập key'
✅ Kiểm tra thành công

[TEST 3] Validate key mới (lần đầu)...
Result: is_valid=True, message='✅ Key kích hoạt thành công'
✅ Key mới được lưu

[TEST 4] Check key hợp lệ...
Result: is_valid=True, message='Key hợp lệ'
✅ Key hợp lệ được chấp nhận

[TEST 5] Validate key khác (thay thế)...
Result: is_valid=True, message='✅ Key kích hoạt thành công'
✅ Key cũ được thay thế bằng key mới

[TEST 6] Kiểm tra use=False (key không sử dụng được)...
Result: is_valid=False, message='❌ Key không sử dụng được (use=False)'
✅ Key với use=False bị từ chối

[TEST 7] Kiểm tra key hết hạn...
Result: is_valid=False, message='❌ Key đã hết hạn (2025-03-31)'
✅ Key hết hạn bị từ chối

[TEST 8] Key có hạn hợp lệ...
Result: is_valid=True, message='Key hợp lệ'
✅ Key còn hạn được chấp nhận

[INFO] Nội dung file key hiện tại:
{
  "key": "VALIDKEY8901",
  "use": true,
  "expire_date": "2026-04-01",
  "created_at": "2025-04-01T12:34:56.789012"
}

════════════════════════════════════════════════════════════
✅ TẤT CẢ TEST PASSED!
════════════════════════════════════════════════════════════
```

## 📚 Các file liên quan

| File | Mô tả |
|------|-------|
| `key/check_key.py` | Module chính - quản lý key |
| `main.py` | Integration - show dialog khi cần |
| `test_key.py` | Test script - kiểm tra tất cả chức năng |
| `KEY_SYSTEM.md` | Tài liệu chi tiết |
| `data/key.json` | File key thực tế (auto-generated) |
| `data/key.json.example` | File mẫu |

## ❌ Troubleshoot

### Problem: "Module KeyChecker not found"
**Solution:**
- ✅ Kiểm tra file `key/check_key.py` có tồn tại
- ✅ Kiểm tra folder `key/` có file `__init__.py` không
  - Nếu chưa có: `touch key/__init__.py`

### Problem: Dialog vẫn hiển thị khi key đã OK
**Solution:**
- ✅ Reload application
- ✅ Kiểm tra `data/key.json` - phải có `"use": true`
- ✅ Kiểm tra `expire_date` - phải lớn hơn ngày hôm nay

### Problem: Key không được lưu
**Solution:**
- ✅ Kiểm tra folder `data/` có tồn tại hoặc có quyền ghi
- ✅ Kiểm tra ổ đĩa còn dung lượng
- ✅ Kiểm tra file permission

## 🔑 Test keys

Ready to use test keys:

| Key | Status | Expire | Use Case |
|-----|--------|--------|----------|
| `DEMO123456789` | ✅ Valid | 2025-12-31 | Development |
| `TESTKEY123` | ✅ Valid | 2025-12-31 | Testing |
| `ABC` | ❌ Invalid | N/A | Quá ngắn |
| `EXPIREDKEY` | ❌ Expired | 2024-01-01 | Test hết hạn |

## 📞 Hỗ trợ

Xem chi tiết: [KEY_SYSTEM.md](KEY_SYSTEM.md)

---
**Version:** 1.0  
**Last Updated:** 2025-04-01
