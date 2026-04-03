"""
AI Content Generator - Sử dụng Groq API để tạo nội dung thông minh
"""
from groq import Groq
import json


class ChatAI:
    """Lớp gọi Groq API để generate/refactor content"""

    def __init__(self, api_key: str, model: str = "llama-3.3-70b-versatile"):
        """
        Khởi tạo ChatAI client
        - api_key: Groq API key
        - model: "llama-3.3-70b-versatile" (mặc định, nhanh), "mixtral-8x7b-32768"
        """
        self.api_key = api_key
        self.model = model
        try:
            self.client = Groq(api_key=api_key)
        except Exception as e:
            print(f"[ERROR] Groq init failed: {e}")
            self.client = None

    def generate_content(self, user_content: str, ai_prompt: str, max_tokens: int = 500) -> str:
        """
        Gọi AI để xử lý/tạo lại content dựa trên prompt

        Args:
            user_content: Nội dung người dùng nhập
            ai_prompt: Prompt hướng dẫn AI (từ AIConfigDialog)
            max_tokens: Độ dài tối đa response

        Returns:
            Nội dung được AI xử lý, hoặc user_content nếu lỗi
        """
        if not self.client or not self.api_key or not ai_prompt:
            print(f"[WARN] AI not configured, dùng content gốc")
            return user_content

        try:
            # Tạo system message từ AI prompt
            system_msg = (
                f"Bạn là một content creator chuyên nghiệp. "
                f"Hãy xử lý nội dung theo hướng dẫn sau:\n\n{ai_prompt}\n\n"
                f"Trả về NỘI DUNG ĐƯỢC XỬ LÝ CHỈ, không thêm bất kỳ dòng nào khác."
            )

            messages = [
                {"role": "system", "content": system_msg},
                {"role": "user", "content": f"Nội dung cần xử lý:\n{user_content}"}
            ]

            print(f"[DEBUG] Gọi Groq API với model: {self.model}")
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7,
                max_tokens=max_tokens,
            )

            result = response.choices[0].message.content.strip()
            print(f"[DEBUG] ═══ AI RESPONSE ═══")
            print(f"[DEBUG] INPUT:  {user_content}")
            print(f"[DEBUG] OUTPUT: {result}")
            print(f"[DEBUG] CHANGED: {result != user_content}")
            print(f"[AI] ✅ Generated: {result[:80]}...")
            return result

        except Exception as e:
            print(f"[ERROR] Groq API call failed: {e}")
            return user_content  # Fallback: dùng content gốc


# ═════════════════════════════════════════════════════════════════════════════
#  HELPER FUNCTION - Dùng từ main.py
# ═════════════════════════════════════════════════════════════════════════════

def generate_ai_content(user_content: str, ai_config: dict) -> str:
    """
    Helper function - Generate content từ Groq API

    Args:
        user_content: Nội dung người dùng nhập
        ai_config: Dict từ AI config {groq_key, ai_prompt, ai_model}

    Returns:
        Content được AI xử lý
    """
    if not ai_config:
        print(f"[WARN] AI config is empty, returning original content")
        return user_content

    # Hỗ trợ cả 2 format: api_key/prompt/model hoặc groq_key/ai_prompt/ai_model
    api_key = ai_config.get("groq_key", "")
    model = ai_config.get("ai_model", "llama-3.3-70b-versatile")
    prompt = ai_config.get("ai_prompt", "")

    print(f"[DEBUG] ════════════════════════════════════════")
    print(f"[DEBUG] AI Config Check:")
    print(f"[DEBUG]   - api_key: {'✅ EXISTS' if api_key else '❌ NOT SET'}")
    print(f"[DEBUG]   - model: {model}")
    print(f"[DEBUG]   - prompt_len: {len(prompt) if prompt else 0}")
    print(f"[DEBUG]   - prompt: {prompt[:60] if prompt else 'EMPTY'}")
    print(f"[DEBUG] ════════════════════════════════════════")

    if not api_key or not prompt:
        print(f"[WARN] Missing api_key or prompt, returning original content")
        return user_content

    print(f"[DEBUG] Tạo ChatAI instance và gọi generate_content()...")
    ai = ChatAI(api_key, model)
    result = ai.generate_content(user_content, prompt)
    
    print(f"[DEBUG] ════════════════════════════════════════")
    print(f"[DEBUG] Kết quả so sánh:")
    print(f"[DEBUG]   - Input:  '{user_content}'")
    print(f"[DEBUG]   - Output: '{result}'")
    print(f"[DEBUG]   - Giống nhau: {result == user_content}")
    print(f"[DEBUG] ════════════════════════════════════════")
    
    return result