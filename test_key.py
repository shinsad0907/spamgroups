#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test Key System - Hệ thống quản lý key phần mềm
Tệp này dùng để kiểm tra hoạt động của key system
"""

from key.check_key import KeyChecker
from datetime import datetime, timedelta
import json
import os

def test_key_system():
    """Test các chức năng của key system"""
    print("=" * 60)
    print("TEST HỆ THỐNG KEY")
    print("=" * 60)
    
    # Use test_mode=True to disable Supabase during testing
    kc = KeyChecker(test_mode=True)
    
    # ────────────────────────────────────────────────────────────
    # TEST 1: Delete cũ (nếu có)
    # ────────────────────────────────────────────────────────────
    print("\n[TEST 1] Xóa file key cũ...")
    kc.delete_key()
    print("✅ Đã xóa file key cũ\n")
    
    # ────────────────────────────────────────────────────────────
    # TEST 2: Check key khi chưa có file
    # ────────────────────────────────────────────────────────────
    print("[TEST 2] Check key khi chưa có file...")
    is_valid, msg = kc.check_key_startup()
    print(f"Result: is_valid={is_valid}, message='{msg}'")
    assert not is_valid, "Phải trả về False khi chưa có file key"
    print("✅ Kiểm tra thành công\n")
    
    # ────────────────────────────────────────────────────────────
    # TEST 3: Validate key mới (lần đầu)
    # ────────────────────────────────────────────────────────────
    print("[TEST 3] Validate key mới (lần đầu)...")
    test_key = "TESTKEY12345"
    is_valid, msg, data = kc.validate_key(test_key)
    print(f"Result: is_valid={is_valid}, message='{msg}'")
    assert is_valid, "Phải accept key mới"
    assert os.path.exists(kc.key_file), "Phải tạo file key"
    print("✅ Key mới được lưu\n")
    
    # ────────────────────────────────────────────────────────────
    # TEST 4: Check key hợp lệ
    # ────────────────────────────────────────────────────────────
    print("[TEST 4] Check key hợp lệ...")
    is_valid, msg = kc.check_key_startup()
    print(f"Result: is_valid={is_valid}, message='{msg}'")
    assert is_valid, "Phải accept key hợp lệ"
    print("✅ Key hợp lệ được chấp nhận\n")
    
    # ────────────────────────────────────────────────────────────
    # TEST 5: Validate key khác (thay thế)
    # ────────────────────────────────────────────────────────────
    print("[TEST 5] Validate key khác (thay thế)...")
    new_key = "NEWKEY67890"
    is_valid, msg, data = kc.validate_key(new_key)
    print(f"Result: is_valid={is_valid}, message='{msg}'")
    assert is_valid, "Phải accept key mới để thay thế"
    print("✅ Key cũ được thay thế bằng key mới\n")
    
    # ────────────────────────────────────────────────────────────
    # TEST 6: Kiểm tra use=False
    # ────────────────────────────────────────────────────────────
    print("[TEST 6] Kiểm tra use=False (key không sử dụng được)...")
    with open(kc.key_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    data['use'] = False
    with open(kc.key_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    is_valid, msg = kc.check_key_startup()
    print(f"Result: is_valid={is_valid}, message='{msg}'")
    assert not is_valid, "Phải từ chối key với use=False"
    assert "không sử dụng được" in msg, "Thông báo phải chỉ ra use=False"
    print("✅ Key với use=False bị từ chối\n")
    
    # ────────────────────────────────────────────────────────────
    # TEST 7: Kiểm tra key hết hạn
    # ────────────────────────────────────────────────────────────
    print("[TEST 7] Kiểm tra key hết hạn...")
    is_valid, msg, data = kc.validate_key("EXPIREDKEY123")
    
    with open(kc.key_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    # Set ngày hết hạn là hôm qua
    yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
    data['expire_date'] = yesterday
    data['use'] = True  # Đảm bảo use=True
    with open(kc.key_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    is_valid, msg = kc.check_key_startup()
    print(f"Result: is_valid={is_valid}, message='{msg}'")
    assert not is_valid, "Phải từ chối key hết hạn"
    assert "hết hạn" in msg or "Hết hạn" in msg, "Thông báo phải đề cập đến hết hạn"
    print("✅ Key hết hạn bị từ chối\n")
    
    # ────────────────────────────────────────────────────────────
    # TEST 8: Key có hạn hợp lệ
    # ────────────────────────────────────────────────────────────
    print("[TEST 8] Key có hạn hợp lệ...")
    is_valid, msg, data = kc.validate_key("VALIDKEY8901")
    
    with open(kc.key_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    # Set ngày hết hạn là ngày mai
    tomorrow = (datetime.now() + timedelta(days=365)).strftime('%Y-%m-%d')
    data['expire_date'] = tomorrow
    data['use'] = True
    with open(kc.key_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    is_valid, msg = kc.check_key_startup()
    print(f"Result: is_valid={is_valid}, message='{msg}'")
    assert is_valid, "Phải accept key còn hạn"
    print("✅ Key còn hạn được chấp nhận\n")
    
    # ────────────────────────────────────────────────────────────
    # FINAL: In thông tin file key
    # ────────────────────────────────────────────────────────────
    print("[INFO] Nội dung file key hiện tại:")
    with open(kc.key_file, 'r', encoding='utf-8') as f:
        print(json.dumps(json.load(f), indent=2, ensure_ascii=False))
    
    print("\n" + "=" * 60)
    print("✅ TẤT CẢ TEST PASSED!")
    print("=" * 60)

if __name__ == '__main__':
    test_key_system()
