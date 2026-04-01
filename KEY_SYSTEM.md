# 🔐 HỆ THỐNG QUẢN LÝ KEY PHẦN MỀM

## 📋 Giới thiệu

Hệ thống key toàn diện để bảo vệ phần mềm "Tiến Khoa". Khi khởi động ứng dụng, hệ thống sẽ tự động kiểm tra key. Nếu chưa có key hoặc key không hợp lệ, người dùng sẽ được yêu cầu nhập key mới.

## 🎯 Tính năng

- ✅ **Kiểm tra key tự động** khi khởi động ứng dụng
- ✅ **Lưu trữ local** - key được lưu trong file `data/key.json`
- ✅ **Validate key** - kiểm tra status (use) và hạn sử dụng
- ✅ **Tự động xóa** - xóa key không hợp lệ tự động
- ✅ **Hướng dẫn rõ ràng** - dialog hiển thị machine ID và hướng dẫn nhập key
- ✅ **Không thể tắt** - không cho phép đóng dialog cho đến khi key hợp lệ

## 📁 Cấu trúc file key

File key được lưu tại: `data/key.json`

**Ví dụ nội dung:**
```json
{
  "key": "TESTKEY12345",
  "use": true,
  "expire_date": "2025-12-31",
  "created_at": "2025-04-01T12:34:56.789012"
}
```

**Các trường:**
- `key` (string): Key kích hoạt (bắt buộc, tối thiểu 6 ký tự)
- `use` (boolean): TRUE = có thể sử dụng, FALSE = bị khóa
- `expire_date` (string): Ngày hết hạn (định dạng YYYY-MM-DD)
- `created_at` (string): Thời gian tạo key (ISO format)

## 🔑 Tạo key test

### Cách 1: Tạo file key.json thủ công

```json
{
  "key": "MYKEY123456",
  "use": true,
  "expire_date": "2025-12-31",
  "created_at": "2025-04-01T00:00:00"
}
```

Lưu vào:  `data/key.json`

### Cách 2: Chạy test script

```bash
python test_key.py
```

Script này sẽ:
1. Xóa file key cũ
2. Test validate key mới
3. Test check key hợp lệ
4. Test thay thế key cũ
5. Test key với use=False
6. Test key hết hạn
7. Test key còn hạn

## 💻 Sử dụng API KeyChecker

### Import
```python
from key.check_key import KeyChecker

kc = KeyChecker()
```

### Các phương thức

#### 1. **validate_key(key_str)** - Kiểm tra và lưu key
```python
is_valid, message, key_data = kc.validate_key("MYKEY123456")
if is_valid:
    print(message)  # ✅ Key kích hoạt thành công
else:
    print(message)  # ❌ Key không hợp lệ
```

**Return:**
- `is_valid` (bool): True nếu key hợp lệ
- `message` (str): Thông báo chi tiết
- `key_data` (dict): Dữ liệu key nếu hợp lệ, None nếu lỗi

#### 2. **check_key_startup()** - Kiểm tra key khi khởi động
```python
is_valid, message = kc.check_key_startup()
if not is_valid:
    print("Chưa có key hoặc key không hợp lệ")
    # Show dialog nhập key
```

**Return:**
- `is_valid` (bool): True nếu key hợp lệ
- `message` (str): Thông báo

#### 3. **get_key()** - Lấy dữ liệu key từ file
```python
key_data = kc.get_key()
if key_data:
    print(f"Key: {key_data['key']}")
    print(f"Hạn sử dụng: {key_data['expire_date']}")
```

#### 4. **save_key(key_str)** - Lưu key vào file
```python
success = kc.save_key("NEWKEY789")
```

#### 5. **delete_key()** - Xóa file key
```python
kc.delete_key()  # Xóa data/key.json
```

## 🔍 Các tình huống kiểm tra

### Tình huống 1: Chưa có key
```
Action: Khởi động ứng dụng
Result: Dialog "Nhập key" hiển thị
Status: ❌ Không thể dùng ứng dụng cho đến khi nhập key đúng
```

### Tình huống 2: Key hợp lệ
```
Action: Nhập key đúng định dạng + use=true + chưa hết hạn
Result: ✅ Key kích hoạt thành công
Status: Ứng dụng hoạt động bình thường
```

### Tình huống 3: Key không hợp lệ (quá ngắn)
```
Action: Nhập "ABC" (< 6 ký tự)
Result: ❌ Key không hợp lệ (quá ngắn)
Status: Dialog vẫn mở, yêu cầu nhập lại
```

### Tình huới 4: Key bị khóa (use=false)
```
Trạng thái file: use = false
Action: Khởi động ứng dụng
Result: ❌ Key không sử dụng được (use=False)
        File key bị xóa, yêu cầu nhập key mới
Status: Dialog nhập key mở lại
```

### Tình huống 5: Key hết hạn
```
Trạng thái file: expire_date = "2025-01-01" (quá khứ)
Action: Khởi động ứng dụng
Result: ❌ Key đã hết hạn (2025-01-01)
        File key bị xóa, yêu cầu nhập key mới
Status: Dialog nhập key mở lại
```

## ⚙️ Tích hợp vào ứng dụng

### 1. MainWindow tự động check key
```python
# main.py - FacebookWindow.__init__
def __init__(self, profile_name: str):
    ...
    self._key_checked = False
    
# main.py - FacebookWindow.showEvent
def showEvent(self, e):
    super().showEvent(e)
    if not self._key_checked:
        self._key_checked = True
        QTimer.singleShot(500, self._check_key_startup)
```

### 2. LicenseDialog xử lý nhập key
```python
# main.py - LicenseDialog._activate
def _activate(self):
    key_input = self.key.text().strip()
    is_valid, message, key_data = self.key_checker.validate_key(key_input)
    
    if is_valid:
        # Đóng dialog, cho phép dùng ứng dụng
        self.activated.emit()
        QTimer.singleShot(1500, self.accept)
    else:
        # Hiển thị lỗi, yêu cầu nhập lại
        self.key.clear()
        self.key.setFocus()
```

### 3. Dialog không thể tắt
```python
# Ngăn chặn nút X
self.setWindowFlags(self.windowFlags() & ~Qt.WindowCloseButtonHint)

# Ngăn chặn ESC
def keyPressEvent(self, e):
    if e.key() != Qt.Key_Escape:
        super().keyPressEvent(e)

# Ngăn chặn Alt+F4
def closeEvent(self, e):
    e.ignore()
```

## 🧪 Chạy test

```bash
# Chạy test script toàn chứng năng
python test_key.py

# Expected output:
# ════════════════════════════════════════════════════════════
# TEST HỆ THỐNG KEY
# ════════════════════════════════════════════════════════════
# [TEST 1] Xóa file key cũ...
# ✅ Đã xóa file key cũ
# [TEST 2] Check key khi chưa có file...
# ✅ Kiểm tra thành công
# ...
# ✅ TẤT CẢ TEST PASSED!
```

## 📞 Liên hệ & Support

- **Zalo:** 0961.006.186
- **Email:** support@tienkhoa.com

## 📝 Ghi chú

- Key được lưu local trong `data/key.json` - **KHÔNG COMMIT** vào Git
- File `data/` nên thêm vào `.gitignore`
- Mỗi lần nhập key mới, file key cũ sẽ bị thay thế
- Nếu key không hợp lệ, file sẽ bị xóa tự động
- Thời hạn test key mặc định là 1 năm từ khi tạo

---

**Phiên bản:** 1.0  
**Cập nhật lần cuối:** 2025-04-01
