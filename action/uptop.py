"""
UpTop Module - Comment trên bài viết đã đăng để đẩy lên đầu (Up Top)
"""

import time
import json
import re
import os
import random
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import StaleElementReferenceException
from AI.chatAI import generate_ai_content


class UpTop:

    def __init__(self, driver, data, log_callback=None, success_callback=None, fail_callback=None):
        self.driver       = driver
        self.data         = data
        self.profile      = data.get('profile', 'Unknown')
        self.posts        = data.get('posts', [])  # Danh sách URLs
        self.content      = data.get('content', '')
        self.media        = data.get('media', [])
        self.cmt_count    = data.get('cmt_count', 1)  # Số lần comment trên mỗi bài
        self.delay_min    = data.get('delay_min', 30)
        self.delay_max    = data.get('delay_max', 60)
        self.use_ai       = data.get('use_ai', False)
        self.ai_config    = data.get('ai_config', {})

        self.log_callback     = log_callback
        self.success_callback = success_callback
        self.fail_callback    = fail_callback

        self.success_count = 0
        self.fail_count    = 0

    # ─────────────────────────────────────────────────────────────
    #  LOGGING & HELPERS
    # ─────────────────────────────────────────────────────────────

    def _log(self, msg):
        print(msg, flush=True)
        if self.log_callback:
            self.log_callback(msg)

    def _ts(self):
        from datetime import datetime
        return datetime.now().strftime("%H:%M:%S")

    def _sleep(self, mn, mx=None):
        t = random.randint(mn, mx) if mx else mn
        time.sleep(t)

    def _get_media_path(self, item):
        return item.get('path', '') if isinstance(item, dict) else item

    # ─────────────────────────────────────────────────────────────
    #  SPIN CONTENT
    # ─────────────────────────────────────────────────────────────

    def _spin_content(self, text: str) -> str:
        def normalize_pipes(t):
            result, depth, i = [], 0, 0
            while i < len(t):
                c = t[i]
                if c == '{':
                    depth += 1; result.append(c); i += 1
                elif c == '}':
                    depth -= 1; result.append(c); i += 1
                elif depth == 0:
                    if t[i:i+3] == '\n|\n':
                        result.append(' | '); i += 3
                    elif t[i:i+2] == '\n|':
                        result.append(' | '); i += 2
                    elif t[i:i+2] == '|\n':
                        result.append(' | '); i += 2
                    elif t[i:i+3] == ' | ':
                        result.append(' | '); i += 3
                    elif c == '|':
                        while result and result[-1] == ' ':
                            result.pop()
                        result.append(' | '); i += 1
                        while i < len(t) and t[i] == ' ':
                            i += 1
                    else:
                        result.append(c); i += 1
                else:
                    result.append(c); i += 1
            return ''.join(result)

        normalized = normalize_pipes(text)
        segments = self._split_top_level_pipe(normalized)

        if len(segments) > 1:
            chosen = random.choice(segments).strip()
            preview = f'"{chosen[:40]}..."' if len(chosen) > 40 else f'"{chosen}"'
            self._log(f"[SPIN] {len(segments)} đoạn → chọn: {preview}")
        else:
            chosen = normalized.strip()

        result = re.sub(r'\{([^}]+)\}', lambda m: random.choice(m.group(1).split('|')).strip(), chosen)
        return result

    def _split_top_level_pipe(self, text: str) -> list:
        segments, buf, depth = [], [], 0
        i = 0
        while i < len(text):
            c = text[i]
            if c == '{':
                depth += 1; buf.append(c)
            elif c == '}':
                depth -= 1; buf.append(c)
            elif depth == 0 and text[i:i+3] == ' | ':
                segments.append(''.join(buf)); buf = []; i += 2
            else:
                buf.append(c)
            i += 1
        segments.append(''.join(buf))
        return [s for s in segments if s.strip()]

    # ─────────────────────────────────────────────────────────────
    #  CHỌN MEDIA
    # ─────────────────────────────────────────────────────────────

    def _select_media(self) -> list:
        if not self.media:
            return []
        # Mặc định chỉ lấy 1 ảnh
        count = min(1, len(self.media))
        selected = self.media[:count]
        self._log(f"[MEDIA] Lấy {count}/{len(self.media)} ảnh")
        paths = [self._get_media_path(m) for m in selected]
        valid = [os.path.abspath(p) for p in paths if p and os.path.exists(p)]
        for p in valid:
            self._log(f"[MEDIA]  → {os.path.basename(p)}")
        if len(valid) < len(paths):
            self._log(f"[WARN] {len(paths)-len(valid)} file không tồn tại, bỏ qua")
        return valid

    # ─────────────────────────────────────────────────────────────
    #  FLOW CHÍNH: VÀO LINK → COMMENT → GỬI
    # ─────────────────────────────────────────────────────────────

    def _comment_to_post(self, post_url: str) -> bool:
        try:
            self._log(f"[INFO] Mở bài: {post_url}")
            self.driver.get(post_url)
            self._sleep(3)
            self._close_post_dialog()

            comment_box = self._find_comment_box()
            if not comment_box:
                self._log("[ERROR] Không tìm được ô comment")
                return False

            # ── Xử lý nội dung với AI nếu được enable ────────────
            content_to_use = self.content
            if self.use_ai and self.ai_config:
                try:
                    self._log("[INFO] 🤖 Đang gọi AI để xử lý nội dung...")
                    self._log(f"[DEBUG] BEFORE AI: '{self.content}'")
                    content_to_use = generate_ai_content(self.content, self.ai_config)
                    self._log(f"[DEBUG] AFTER AI:  '{content_to_use}'")
                    self._log(f"[DEBUG] CHANGED:   {content_to_use != self.content}")
                    if content_to_use and content_to_use.strip():
                        self._log(f"[OK] AI xử lý xong: {content_to_use[:60]}...")
                    else:
                        self._log("[WARN] AI trả về nội dung rỗng, dùng nội dung gốc")
                        content_to_use = self.content
                except Exception as e:
                    self._log(f"[ERROR] AI call failed: {e}, dùng nội dung gốc")
                    content_to_use = self.content
            
            spin_text = self._spin_content(content_to_use)
            comment_box.click()
            self._sleep(1)
            comment_box.send_keys(spin_text)
            self._log(f"[OK] Đã nhập: {spin_text[:60]}...")
            self._sleep(1)

            media_paths = self._select_media()
            if media_paths:
                self._log(f"[INFO] Đính kèm {len(media_paths)} ảnh...")
                self._close_post_dialog()
                if not self._attach_images(media_paths, comment_box):
                    self._log("[WARN] Đính kèm ảnh thất bại, vẫn tiếp tục gửi")
                self._sleep(2)

            if not self._submit_comment(comment_box):
                self._log("[ERROR] Không gửi được comment")
                return False

            self._log(f"[SUCCESS] Bình luận thành công: {post_url}")
            return True

        except Exception as e:
            self._log(f"[ERROR] Lỗi khi bình luận {post_url}: {e}")
            return False

    def _close_post_dialog(self):
        closed = self.driver.execute_script("""
            let count = 0;
            document.querySelectorAll('div[role="dialog"]').forEach(d => {
                const heading = (d.innerText || '').toLowerCase();
                if (!heading.includes('tạo bài') && !heading.includes('create post')
                    && !heading.includes('what') && !heading.includes('nghĩ gì')) return;
                const closeBtn = d.querySelector(
                    '[aria-label="Đóng"], [aria-label="Close"], '
                    + '[aria-label*="óng"], [aria-label*="lose"]'
                );
                if (closeBtn) { closeBtn.click(); count++; }
            });
            return count;
        """)
        if closed:
            self._log(f"[INFO] Đã đóng {closed} dialog tạo bài viết")
            self._sleep(1)

    def _find_comment_box(self):
        self._log("[INFO] Tìm ô comment...")
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight * 0.4);")
        self._sleep(1.5)

        box = self.driver.execute_script("""
            for (let p of document.querySelectorAll('[data-pagelet*="Comment"]')) {
                const b = p.querySelector('div[contenteditable="true"]');
                if (b) return b;
            }
            for (let b of document.querySelectorAll('div[contenteditable="true"]')) {
                const ph   = (b.dataset.placeholder || b.getAttribute('data-placeholder') || '').toLowerCase();
                const aria = (b.getAttribute('aria-label') || '').toLowerCase();
                if (ph.includes('nghĩ gì') || aria.includes('tạo bài') || aria.includes('create post')) continue;
                if (ph.includes('bình luận') || ph.includes('comment') || aria.includes('bình luận')) return b;
            }
            const all = Array.from(document.querySelectorAll('div[contenteditable="true"]'));
            return all.length >= 2 ? all[all.length - 1] : (all[0] || null);
        """)

        if box:
            self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", box)
            self._sleep(0.5)
            self._log("[OK] Tìm thấy ô comment")
            return box

        self._log("[WARN] Không tìm được ô comment")
        return None

    def _find_comment_file_input(self, comment_box):
        return self.driver.execute_script("""
            const box = arguments[0];

            function isCommentInput(inp) {
                const dialog = inp.closest('[role="dialog"]');
                if (dialog) {
                    const txt = (dialog.innerText || '').toLowerCase();
                    if (txt.includes('tạo bài') || txt.includes('create post')
                        || txt.includes('nghĩ gì') || txt.includes("what's on"))
                        return false;
                }
                return true;
            }

            function show(inp) {
                inp.style.cssText = 'display:block!important;visibility:visible!important;'
                    + 'opacity:1!important;position:fixed!important;top:0;left:0;'
                    + 'width:1px;height:1px;z-index:99999;';
                return inp;
            }

            if (box) {
                const form = box.closest('form');
                if (form) {
                    for (let inp of form.querySelectorAll('input[type="file"]')) {
                        if (isCommentInput(inp)) return show(inp);
                    }
                }
                let node = box.parentElement;
                for (let i = 0; i < 15; i++) {
                    if (!node) break;
                    for (let inp of node.querySelectorAll('input[type="file"]')) {
                        if (isCommentInput(inp)) return show(inp);
                    }
                    node = node.parentElement;
                }
            }

            for (let p of document.querySelectorAll('[data-pagelet*="Comment"]')) {
                for (let inp of p.querySelectorAll('input[type="file"]')) {
                    if (isCommentInput(inp)) return show(inp);
                }
            }

            for (let inp of document.querySelectorAll('input[type="file"]')) {
                if (isCommentInput(inp)) return show(inp);
            }

            return null;
        """, comment_box)

    def _attach_images(self, paths: list, comment_box=None) -> bool:
        try:
            file_input = self._find_comment_file_input(comment_box)

            if not file_input:
                self._log("[INFO] Không có file input sẵn, thử click nút ảnh...")
                if not self._click_photo_btn(comment_box):
                    self._log("[ERROR] Không tìm được file input cho comment")
                    return False
                time.sleep(1.5)
                file_input = self._find_comment_file_input(comment_box)

            if not file_input:
                self._log("[ERROR] Vẫn không tìm được file input")
                return False

            if len(paths) > 1:
                self.driver.execute_script(
                    "arguments[0].setAttribute('multiple', ''); "
                    "arguments[0].removeAttribute('accept');",
                    file_input
                )

            all_paths = '\n'.join(paths)
            self._log(f"[INFO] Gửi {len(paths)} file cùng lúc...")
            file_input.send_keys(all_paths)
            self._log(f"[OK] Đã gửi {len(paths)} file")

            self._wait_upload(timeout=60)
            return True

        except Exception as e:
            self._log(f"[ERROR] Đính kèm ảnh lỗi: {e}")
            return False

    def _click_photo_btn(self, comment_box) -> bool:
        xpath_candidates = [
            "//div[5]//form//ul/li[3]",
            "//form[.//div[@contenteditable='true']]//ul/li[3]",
            "//form[.//div[@contenteditable='true']]//*[contains(@aria-label,'ảnh') or contains(@aria-label,'Photo')]",
        ]
        for xpath in xpath_candidates:
            try:
                btns = self.driver.find_elements(By.XPATH, xpath)
                for btn in btns:
                    try:
                        dialog = btn.find_element(By.XPATH, "ancestor::div[@role='dialog']")
                        txt = dialog.text.lower()
                        if 'tạo bài' in txt or 'create post' in txt:
                            continue
                    except Exception:
                        pass
                    btn.click()
                    self._log(f"[OK] Click nút ảnh via XPath: {xpath}")
                    self._sleep(1.5)
                    self._close_post_dialog()
                    return True
            except Exception:
                continue
        return False

    def _wait_upload(self, timeout=60):
        self._log("[INFO] Chờ upload...")
        deadline = time.time() + timeout
        while time.time() < deadline:
            count = self.driver.execute_script("""
                return document.querySelectorAll(
                    'img[src^="blob:"], img[src*="scontent"], [data-visualcompletion="media-vc-image"]'
                ).length;
            """)
            if count:
                self._log(f"[OK] Upload xong ({count} ảnh)")
                return
            time.sleep(1.5)
        self._log("[WARN] Timeout chờ upload")

    def _submit_comment(self, comment_box) -> bool:
        try:
            comment_box.send_keys(Keys.RETURN)
            self._sleep(2)

            is_empty = self.driver.execute_script(
                "return !arguments[0].innerText.trim();", comment_box
            )
            if is_empty:
                self._log("[OK] Gửi bằng Enter thành công")
                self._sleep(2)
                return True

            sent = self.driver.execute_script("""
                const keywords = ['post', 'reply', 'comment', 'gửi', 'trả lời', 'bình luận'];
                const box = arguments[0];
                let container = box;
                for (let i = 0; i < 8; i++) {
                    container = container.parentElement;
                    if (!container) break;
                    for (let btn of container.querySelectorAll('[role="button"], button')) {
                        const t = (btn.innerText + (btn.getAttribute('aria-label') || '')).toLowerCase();
                        if (keywords.some(k => t.includes(k)) && !btn.disabled) {
                            btn.click(); return true;
                        }
                    }
                }
                return false;
            """, comment_box)

            if sent:
                self._log("[OK] Gửi bằng nút thành công")
                self._sleep(2)
                return True

            self._log("[WARN] Không gửi được comment")
            return False

        except Exception as e:
            self._log(f"[ERROR] Submit lỗi: {e}")
            return False

    # ─────────────────────────────────────────────────────────────
    #  MAIN: LOOP TỪNG LINK, COMMENT BẬO NHIÊU LẦN
    # ─────────────────────────────────────────────────────────────

    def main_uptop(self):
        self._log(
            f"\n[{self._ts()}] 🚀 Bắt đầu UP TOP | "
            f"{len(self.posts)} bài | {self.cmt_count} comment/bài | "
            f"Delay {self.delay_min}~{self.delay_max}s"
        )

        for post_idx, post_url in enumerate(self.posts, 1):
            if not post_url.strip():
                self._log(f"[SKIP] Bài {post_idx}: link trống")
                continue

            self._log(f"\n[{self._ts()}] 📌 [{post_idx}/{len(self.posts)}] {post_url}")

            # Comment bao nhiêu lần trên từng bài
            for cmt_idx in range(1, self.cmt_count + 1):
                ts = self._ts()
                self._log(f"  [{cmt_idx}/{self.cmt_count}] Comment lần thứ {cmt_idx}")

                if self._comment_to_post(post_url):
                    self.success_count += 1
                    if self.success_callback:
                        self.success_callback(ts, post_url, f"UpTop - Comment {cmt_idx}/{self.cmt_count}")
                else:
                    self.fail_count += 1
                    if self.fail_callback:
                        self.fail_callback(ts, post_url, f"UpTop - Comment {cmt_idx}/{self.cmt_count} thất bại")

                # Delay giữa các comment
                if cmt_idx < self.cmt_count:
                    delay = random.randint(self.delay_min, self.delay_max)
                    self._log(f"⏰ Chờ {delay}s...")
                    self._sleep(delay)

            # Delay giữa các bài
            if post_idx < len(self.posts):
                delay = random.randint(self.delay_min * 2, self.delay_max * 2)
                self._log(f"⏰ Chờ {delay}s trước bài tiếp theo...")
                self._sleep(delay)

        self._log(
            f"\n[{self._ts()}] Kết quả: "
            f"✅ {self.success_count} thành công | "
            f"❌ {self.fail_count} thất bại"
        )

    def execute(self):
        ts = self._ts()
        print(f"\n{'='*60}", flush=True)
        print(f"[{ts}] BẮT ĐẦU UP TOP", flush=True)
        print(f"{'='*60}", flush=True)
        print(json.dumps({
            'profile'       : self.profile,
            'posts'         : len(self.posts),
            'cmt_count'     : self.cmt_count,
            'content_preview': self.content[:80],
            'media_count'   : len(self.media),
            'delay'         : f"{self.delay_min}~{self.delay_max}s",
        }, ensure_ascii=False, indent=2), flush=True)
        print(f"{'='*60}\n", flush=True)

        self.main_uptop()
