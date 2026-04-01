# 🔐 KEY SYSTEM - QUICK REFERENCE

## 🎯 Tính năng

Hệ thống key **bắt buộc** khi khởi động ứng dụng:
- ✅ Không có key → bắt nhập
- ✅ Key sai → xóa & bắt nhập lại
- ✅ Key có use=false → xóa & bắt nhập lại  
- ✅ Key hết hạn → xóa & bắt nhập lại
- ❌ Dialog không thể tắt (no X, ESC, Alt+F4)

## 📌 File quan trọng

```
/key/
  ├── check_key.py ............ LỮU Key logic (NEW)
  ├── __init__.py ............. Module init (NEW)
  
/main.py ...................... Cập nhật: LicenseDialog + showEvent

/data/
  ├── key.json ................ Auto-generated (Runtime)
  ├── key.json.example ........ File mẫu (Commit-safe)
```

## 🚀 TEST NHANH

### Cách 1: Quicktest (Copy mẫu)
```bash
cp data/key.json.example data/key.json
python main.py
# → App mở ngay (key hợp lệ)
```

### Cách 2: Fulltest (Test scenarios)
```bash
python test_key.py
# → Check tất cả 8 test cases
```

### Cách 3: Manual test (No key)
```bash
rm -f data/key.json
python main.py
# → Dialog bắt nhập key
```

## 💡 Nhập Key

**Test keys có sẵn:**
- `TESTKEY123` - ✅ Valid
- `DEMO123456789` - ✅ Valid
- `ABC` - ❌ Quá ngắn
- Bất kỳ key ≥ 6 ký tự - ✅ Valid (first time)

**Dialog nhập:**
1. Copy mã máy (nếu cần)
2. Nhập key ≥ 6 ký tự
3. Click "KÍCH HOẠT"
4. ✅ Nếu OK → App mở
5. ❌ Nếu sai → Nhập lại

## 📋 Key file format

**File:** `data/key.json`
```json
{
  "key": "YOURKEY123",
  "use": true,
  "expire_date": "2025-12-31",
  "created_at": "2025-04-01T12:34:56.789"
}
```

**Fields:**
- `key`: String ≥ 6 ký tự
- `use`: true=OK, false=Locked
- `expire_date`: YYYY-MM-DD format
- `created_at`: ISO format (auto)

## 🔍 Validation Logic

```
Input: "MYKEY123"
  ↓
Length ≥ 6? → ✅ Yes (8 chars)
  ↓
File có key cũ? → Try to replace
  ↓
Check use? → must be true
  ↓
Check expire? → must > today
  ↓
✅ Valid → Save & Use
❌ Invalid → Delete & Retry
```

## ⚙️ API Usage

```python
from key.check_key import KeyChecker

kc = KeyChecker()

# Validate & save key
is_valid, msg, data = kc.validate_key("TESTKEY123")
# → (True, "✅ Key kích hoạt thành công", {...})

# Check at startup
is_valid, msg = kc.check_key_startup()
# → (True, "Key hợp lệ") or (False, "...")

# Get existing key
key_data = kc.get_key()
# → {'key': 'TESTKEY123', 'use': True, ...}

# Delete key file
kc.delete_key()
# → Auto-delete data/key.json
```

## 🐛 Troubleshoot

| Problem | Solution |
|---------|----------|
| Dialog vẫn show | Kiểm tra `data/key.json` hoặc delete & retry |
| Key không lưu | Check folder `data/` permissions |
| "Key quá ngắn" | Nhập key ≥ 6 ký tự |
| "use=False" | Set `"use": true` trong key.json |
| "Hết hạn" | Set future date: `"expire_date": "2026-12-31"` |

## 📚 Docs

- **[SETUP_KEY.md](SETUP_KEY.md)** - Quick setup guide
- **[KEY_SYSTEM.md](KEY_SYSTEM.md)** - Full documentation  
- **[CHANGES.md](CHANGES.md)** - What changed
- **[test_key.py](test_key.py)** - Test script

## 🔗 Related Files

| File | Purpose |
|------|---------|
| `key/check_key.py` | Core key logic |
| `main.py` | LicenseDialog integration |
| `test_key.py` | Automated tests |
| `data/key.json` | Runtime key file |
| `data/key.json.example` | Reference template |

## ⏱️ Workflow

### First Run
```
main.py start
  ↓ (500ms delay)
showEvent triggered
  ↓
_check_key_startup()
  ↓
No key file → Show LicenseDialog
  ↓
User enters key: "MYKEY123"
  ↓
Click "KÍCH HOẠT"
  ↓
validate_key("MYKEY123")
  ↓
✅ Save to data/key.json
✅ Close dialog
✅ App ready
```

### Next Runs
```
main.py start
  ↓ (500ms delay)
showEvent triggered
  ↓
_check_key_startup()
  ↓
Key file exists & valid → Skip dialog
  ↓
✅ App ready immediately
```

## 🎓 Example Scenarios

**Scenario 1: New user, no key**
```
$ python main.py
→ Dialog: "Nhập Key kích hoạt"
→ User: "TESTKEY123" + Enter
→ "✅ Key kích hoạt thành công"
→ App opens ✅
```

**Scenario 2: User reopens app**
```
$ python main.py
→ Key found in data/key.json
→ Validation: use=true, expire > today
→ "Key hợp lệ"
→ App opens immediately ✅
```

**Scenario 3: Key becomes invalid (use=false)**
```
$ python main.py
→ Key found: use=false
→ "❌ Key không sử dụng được (use=False)"
→ File deleted automatically
→ Dialog: "Nhập Key kích hoạt"
→ New key required ✅
```

## ✨ Features

| Feature | Status |
|---------|--------|
| Auto check on startup | ✅ Done |
| Local key storage | ✅ Done |
| Validate use flag | ✅ Done |
| Validate expiry | ✅ Done |
| Auto delete invalid | ✅ Done |
| No close dialog | ✅ Done |
| No ESC key | ✅ Done |
| Full test suite | ✅ Done |
| Docs | ✅ Done |

---

**Need help?** → Read [KEY_SYSTEM.md](KEY_SYSTEM.md)  
**Want to test?** → Run `python test_key.py`  
**Quick start?** → Follow [SETUP_KEY.md](SETUP_KEY.md)

**Version:** 1.0 | **Date:** 2025-04-01
