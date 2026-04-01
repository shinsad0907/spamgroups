import os
import json
from datetime import datetime
from typing import Optional, Tuple

try:
    import supabase
    SUPABASE_AVAILABLE = True
except:
    SUPABASE_AVAILABLE = False
    print("[KEY] ⚠️  Supabase not installed - remote verification disabled")


class KeyChecker:
    """Quản lý kiểm tra key phần mềm - kết hợp local + Supabase"""
    
    def __init__(self, test_mode=False):
        self.key_file = os.path.join('data', 'key.json')
        self.test_mode = test_mode  # Disable Supabase during testing
        os.makedirs('data', exist_ok=True)
        print(f"[KEY] 🔧 KeyChecker initialized (test_mode={test_mode})")
        print(f"[KEY] 📂 Working dir: {os.getcwd()}")
        print(f"[KEY] 📄 Key file: {os.path.abspath(self.key_file)}")
        
        # Supabase credentials
        self.supabase_url = 'https://rlbkfycckmuflfnmlawf.supabase.co'
        self.supabase_key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJsYmtmeWNja211Zmxmbm1sYXdmIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzUwNTUxNDUsImV4cCI6MjA5MDYzMTE0NX0.lK_HJ5KaackpTHXEjnBpsEkftMc3dFS6YebXdX00gc0'
        self.supabase_client = None
        
        if not test_mode and SUPABASE_AVAILABLE:
            try:
                self.supabase_client = supabase.create_client(self.supabase_url, self.supabase_key)
                print(f"[KEY] 🌐 Supabase client initialized")
            except Exception as e:
                print(f"[KEY] ⚠️  Supabase init error: {e}")
    
    # ═══════════════════════════════════════════════════════════
    # SAVE KEY
    # ═══════════════════════════════════════════════════════════
    def save_key(self, key_str: str) -> bool:
        """Lưu key vào file local"""
        try:
            data = {
                'key': key_str.strip(),
                'use': True,
                'expire_date': '2026-12-31',  # Mặc định hết hạn 1 năm
                'created_at': datetime.now().isoformat()
            }
            print(f"[KEY] 💾 Lưu key vào: {os.path.abspath(self.key_file)}")
            print(f"[KEY] 📝 Dữ liệu: use={data['use']}, expire={data['expire_date']}")
            with open(self.key_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            print(f"[KEY] ✅ Lưu thành công")
            return True
        except Exception as e:
            print(f"❌ Lỗi lưu key: {e}")
            return False

    # ═══════════════════════════════════════════════════════════
    # GET KEY
    # ═══════════════════════════════════════════════════════════
    def get_key(self) -> Optional[dict]:
        """Lấy key từ file local"""
        try:
            if not os.path.exists(self.key_file):
                print(f"[KEY] ⚠️  File không tồn tại: {os.path.abspath(self.key_file)}")
                return None
            
            print(f"[KEY] 📖 Đọc file từ: {os.path.abspath(self.key_file)}")
            with open(self.key_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            print(f"[KEY] ✅ Đã đọc key: {data.get('key')}")
            return data
        except Exception as e:
            print(f"❌ Lỗi đọc key: {e}")
            return None

    # ═══════════════════════════════════════════════════════════
    # DELETE KEY
    # ═══════════════════════════════════════════════════════════
    def delete_key(self) -> bool:
        """Xóa file key"""
        try:
            if os.path.exists(self.key_file):
                print(f"[KEY] 🗑️  Xóa file: {os.path.abspath(self.key_file)}")
                os.remove(self.key_file)
                print(f"[KEY] ✅ Đã xóa")
            return True
        except Exception as e:
            print(f"❌ Lỗi xóa key: {e}")
            return False

    # ═══════════════════════════════════════════════════════════
    # SUPABASE VERIFICATION
    # ═══════════════════════════════════════════════════════════
    def verify_key_on_supabase(self, key_str: str) -> Tuple[bool, str]:
        """
        Verify key trên Supabase database
        Return: (is_valid: bool, message: str)
        """
        # Skip Supabase during test mode
        if self.test_mode:
            print(f"[KEY] 🧪 Test mode - skipping Supabase verification")
            return True, "Test mode - local only"
        
        if not self.supabase_client:
            print(f"[KEY] ⚠️  Supabase not available, skipping remote verification")
            return True, "Supabase unavailable - using local only"
        
        try:
            print(f"[KEY] 🌐 Verifying key on Supabase...")
            # Query using "id" column (not "key")
            res = self.supabase_client.table("keys").select("*").eq("id", key_str).execute()
            print(f"[KEY] 📦 Supabase response: {len(res.data)} records")
            
            if not res.data:
                print(f"[KEY] ❌ Key not found in Supabase")
                return False, "❌ Key không tồn tại trên server"
            
            row = res.data[0]
            print(f"[KEY] 📋 Key row: use={row.get('use')}, expire={row.get('expire_date')}")
            
            # Check use flag from Supabase
            use_flag = row.get('use', False)
            if not use_flag:
                print(f"[KEY] ❌ Supabase: use={use_flag}")
                return False, "❌ Key bị khóa trên server (use=False)"
            
            # Check expire date from Supabase (if exists)
            if row.get('expire_date'):
                try:
                    expire_date = datetime.strptime(row['expire_date'], '%Y-%m-%d')
                    if datetime.now() > expire_date:
                        print(f"[KEY] ❌ Supabase: Key expired")
                        return False, f"❌ Key hết hạn trên server ({row['expire_date']})"
                except:
                    pass
            
            print(f"[KEY] ✅ Supabase verification passed")
            return True, "Key hợp lệ trên server"
            
        except Exception as e:
            error_str = str(e)
            print(f"[KEY] ⚠️  Lỗi Supabase: {error_str}")
            
            # Schema errors (column doesn't exist) → fail, don't allow offline mode
            if "does not exist" in error_str or "42703" in error_str:
                print(f"[KEY] ❌ Schema error - rejecting key")
                return False, f"❌ Lỗi kết nối server (schema): {error_str[:50]}"
            
            # Network errors → allow offline mode (tin key local)
            return True, f"⚠️  Cannot reach Supabase ({error_str[:30]}...) - using local"

    # ═══════════════════════════════════════════════════════════
    # VALIDATE KEY
    # ═══════════════════════════════════════════════════════════
    def validate_key(self, key_str: str) -> Tuple[bool, str, Optional[dict]]:
        """
        Kiểm tra key (local + Supabase):
        1. Check format
        2. Check Supabase remote
        3. Save to local if valid
        Return: (is_valid: bool, message: str, key_data: dict or None)
        """
        key_str = key_str.strip()
        print(f"[KEY] 🔐 Validating key: {key_str}")
        
        # Kiểm tra format key đơn giản (từ 6 ký tự trở lên)
        if len(key_str) < 6:
            print(f"[KEY] ❌ Key quá ngắn ({len(key_str)} ký tự)")
            return False, "❌ Key không hợp lệ (quá ngắn)", None
        
        print(f"[KEY] ⏱️  Checking Supabase...")
        # Verify immediately on Supabase
        is_valid_remote, msg_remote = self.verify_key_on_supabase(key_str)
        
        if not is_valid_remote:
            print(f"[KEY] ❌ Supabase rejected: {msg_remote}")
            return False, msg_remote, None
        
        # Supabase confirmed → save to local
        print(f"[KEY] ✨ Saving to local...")
        self.save_key(key_str)
        return True, "✅ Key kích hoạt thành công", {'key': key_str, 'use': True}

    # ═══════════════════════════════════════════════════════════
    # CHECK KEY STARTUP
    # ═══════════════════════════════════════════════════════════
    def check_key_startup(self) -> Tuple[bool, str]:
        """
        Check key khi khởi động (local + Supabase):
        1. Check file JSON local
        2. Check Supabase remote
        Return: (is_valid: bool, message: str)
        """
        print(f"[KEY] 🔍 Checking startup key...")
        print(f"[KEY] ⏱️  Step 1: Checking local file...")
        existing_data = self.get_key()
        
        if not existing_data:
            print(f"[KEY] ❌ Không có key file")
            return False, "Chưa có key - Vui lòng nhập key"
        
        key = existing_data.get('key')
        print(f"[KEY] 📌 Key tìm thấy: {key}")
        
        # ── Step 1: Check local file ──────────────────────────
        print(f"[KEY] ⏱️  Step 1: Validating local file...")
        
        # Check use flag
        use_flag = existing_data.get('use', False)
        print(f"[KEY] 🏳️  Use flag (local): {use_flag}")
        if not use_flag:
            print(f"[KEY] ❌ Key bị khóa (use=False)")
            self.delete_key()
            return False, "Key không sử dụng được (use=False) - Vui lòng nhập key mới"
        
        # Check expire date
        expire_date_str = existing_data.get('expire_date', '2099-12-31')
        print(f"[KEY] 📅 Expire date (local): {expire_date_str}")
        try:
            expire_date = datetime.strptime(expire_date_str, '%Y-%m-%d')
            today = datetime.now()
            print(f"[KEY] ⏰ Today: {today.date()}, Expire: {expire_date.date()}")
            if today > expire_date:
                print(f"[KEY] ❌ Key hết hạn (local)")
                self.delete_key()
                return False, f"Key đã hết hạn ({expire_date_str}) - Vui lòng nhập key mới"
        except Exception as ex:
            print(f"[KEY] ⚠️  Lỗi parse date: {ex}")
            pass
        
        print(f"[KEY] ✅ Local file passed")
        
        # ── Step 2: Verify on Supabase ───────────────────────
        print(f"\n[KEY] ⏱️  Step 2: Verifying key on Supabase...")
        is_valid_remote, msg_remote = self.verify_key_on_supabase(key)
        
        if not is_valid_remote:
            print(f"[KEY] ❌ Supabase verification failed: {msg_remote}")
            # Supabase nói không hợp lệ → xóa file, yêu cầu nhập lại
            self.delete_key()
            return False, f"{msg_remote}"
        
        print(f"[KEY] ✅ Supabase verification passed")
        print(f"[KEY] ✅ Key hợp lệ (local + remote)\n")
        return True, "Key hợp lệ"


# ═══════════════════════════════════════════════════════════
# TEST
# ═══════════════════════════════════════════════════════════
