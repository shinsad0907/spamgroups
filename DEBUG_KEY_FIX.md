# 🔧 DEBUG GUIDE - KEY SYSTEM

## ❌ Issue Found & Fixed

### Problem
- ✅ Key được lưu vào file
- ❌ Nhưng khi mở lại app vẫn phải nhập lại
- ❌ `check_key_startup()` luôn trả về False

### Root Cause
**Expired key!** 😅

File `key.json.example` có ngày hết hạn `2025-12-31`, nhưng hôm nay là `2026-04-01`, nên key bị reject!

```json
// ❌ WRONG
{
  "expire_date": "2025-12-31"  // Quá khứ!
}

// ✅ FIXED
{
  "expire_date": "2026-12-31"  // Tương lai
}
```

## ✅ Fixes Applied

### 1. Updated key.json.example
```diff
- "expire_date": "2025-12-31"
+ "expire_date": "2026-12-31"
```

### 2. Updated default expire in check_key.py
```python
# save_key() method
'expire_date': '2026-12-31',  # ← Updated from 2025-12-31
```

### 3. Added comprehensive debug logging
File: `key/check_key.py`
- `__init__()` - Show working dir & key file path
- `save_key()` - Log save operations
- `get_key()` - Log file read operations
- `delete_key()` - Log delete operations
- `validate_key()` - Detailed validation flow
- `check_key_startup()` - Step-by-step checks

File: `main.py`
- `LicenseDialog._activate()` - Key validation flow
- `MainWindow._check_key_startup()` - Startup check with borders

## 🧪 Testing the Fix

### Test 1: Clean start (no key)
```bash
rm -f data/key.json
python main.py
```

Expected:
```
[KEY] 🔧 KeyChecker initialized
[KEY] 📂 Working dir: c:\Users\pc\Desktop\shin\spamgroup
[KEY] 📄 Key file: c:\Users\pc\Desktop\shin\spamgroup\data\key.json

[STARTUP] 🔍 Checking key on startup...
[KEY] 🔍 Checking startup key...
[KEY] ❌ Không có key file
[STARTUP] ❌ Key invalid or missing, showing license dialog...

[LICENSE] User entered key: TESTKEY123
[KEY] 🔐 Validating key: TESTKEY123
[KEY] ✨ New key, saving...
[KEY] 💾 Lưu key vào: c:\Users\pc\Desktop\shin\spamgroup\data\key.json
[KEY] 📝 Dữ liệu: use=True, expire=2026-12-31
[KEY] ✅ Lưu thành công
[LICENSE] ✅ Valid key, closing dialog...
```

### Test 2: Key persists (app restart)
```bash
python main.py  # Run again
```

Expected (no dialog):
```
[STARTUP] 🔍 Checking key on startup...
[KEY] 🔍 Checking startup key...
[KEY] 📖 Đọc file từ: c:\Users\pc\Desktop\shin\spamgroup\data\key.json
[KEY] ✅ Đã đọc key: TESTKEY123
[KEY] 📌 Key tìm thấy: TESTKEY123
[KEY] 🏳️  Use flag: True
[KEY] 📅 Expire date: 2026-12-31
[KEY] ⏰ Today: 2026-04-01, Expire: 2026-12-31
[KEY] ✅ Key hợp lệ
[STARTUP] ✅ Key valid, app ready to use
```

### Test 3: Using example file
```bash
cp data/key.json.example data/key.json
python main.py
```

Expected (app opens immediately):
```
[KEY] ✅ Key hợp lệ
[STARTUP] ✅ Key valid, app ready to use
```

## 📊 Debug Output Format

### Console colors (key symbols)
- 🔐 `[KEY]` - KeyChecker operations
- 🔑 `[LICENSE]` - LicenseDialog operations
- 🚀 `[STARTUP]` - MainWindow startup check

### Log Levels
- ✅ Success
- ❌ Error/Failure
- 🔍 Checking/Searching
- 💾 Save operation
- 📖 Read operation
- 🗑️ Delete operation
- ⚠️ Warning

## 🔍 Troubleshooting

### Issue: "Không có key file"
```
[KEY] ❌ Không có key file
```

**Solution:**
- Check if `data/key.json` exists: `ls data/key.json`
- Check working directory: `pwd` or `os.getcwd()`
- Verify path matches: `data/key.json`

### Issue: "Key không sử dụng được (use=False)"
```
[KEY] 🏳️  Use flag: False
[KEY] ❌ Key bị khóa (use=False)
```

**Solution:**
- Edit `data/key.json`
- Change `"use": false` to `"use": true`
- Delete & re-add key

### Issue: "Key đã hết hạn"
```
[KEY] 💍 Expire date: 2025-12-31
[KEY] ⏰ Today: 2026-04-01, Expire: 2025-12-31
[KEY] ❌ Key hết hạn
```

**Solution:**
- Edit `data/key.json`
- Change expire date to future: `"expire_date": "2026-12-31"`
- Or use `key/check_key.py` to revalidate

## 📝 Manual Test

### 1. Create test key manually
```bash
cat > data/key.json << 'EOF'
{
  "key": "MANUAL_TEST_KEY",
  "use": true,
  "expire_date": "2026-12-31",
  "created_at": "2026-04-01T00:00:00"
}
EOF
```

### 2. Run app
```bash
python main.py
```

### 3. Expected output
Key should be auto-read and accepted without showing dialog.

## 🧬 Code Flow

```
main.py start
  ↓
MainWindow.__init__()
  ↓
MainWindow.showEvent()  [500ms delay]
  ↓
_check_key_startup()
  ↓
KeyChecker()
  ↓
check_key_startup()
  ├─ get_key() → read from data/key.json
  ├─ Check use flag
  ├─ Check expire_date vs today
  └─ Return (bool, message)
  ↓
if not is_valid:
  └─ _license() → Show dialog
else:
  └─ set _activated = True
```

## 📋 Files Modified

| File | Change | Why |
|------|--------|-----|
| `key/check_key.py` | Added debug logging | Track flow |
| `key/check_key.py` | Updated expire date to 2026-12-31 | Fix expired key |
| `data/key.json.example` | Updated expire date to 2026-12-31 | Fix test file |
| `main.py` | Added debug logging | Track flow |

## ✅ Verification

Run these to verify everything works:

```bash
# Test 1: Full test suite
python test_key.py

# Test 2: Quick test with example
cp data/key.json.example data/key.json
python main.py  # Should open immediately

# Test 3: Manual test (no key)
rm -f data/key.json
python main.py  # Should show dialog,
                # Enter "TESTKEY123"
                # Should proceed
```

---

**Status:** ✅ FIXED  
**Date:** 2026-04-01  
**Root Cause:** Expired key (2025-12-31 < 2026-04-01)
