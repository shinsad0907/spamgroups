import sys, os, random, time, json, traceback, subprocess
from datetime import datetime

from browser_engine.chrome_driver import ChromiumDriver
from action.scan_groups import GroupScanner
from action.post_groups import PostGroups
from action.comment import CommentGroups
from action.uptop import UpTop
from key.check_key import KeyChecker
from AI.chatAI import generate_ai_content

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QLineEdit, QTextEdit, QTableWidget, QTableWidgetItem,
    QGroupBox, QSpinBox, QFileDialog, QMessageBox, QDialog,
    QFrame, QStatusBar, QProgressBar, QCheckBox,
    QAbstractItemView, QMenu, QAction, QHeaderView,
    QListWidget, QListWidgetItem, QSizePolicy, QComboBox, QScrollArea, QButtonGroup
)
from PyQt5.QtCore import Qt, QTimer, QRect, pyqtSignal, QThread, QObject, QEvent
from PyQt5.QtGui import QFont, QColor, QBrush

import win32gui
import win32con

# ═══════════════════════════════════════════════════════════════════════════════
#  DARK STYLESHEET
# ═══════════════════════════════════════════════════════════════════════════════
DARK = """
QMainWindow, QDialog {
    background: #1e1e2e;
}
QWidget {
    background: #1e1e2e;
    color: #cdd6f4;
    font-family: 'Segoe UI', Arial;
    font-size: 13px;
}
QLineEdit {
    background: #313244;
    border: 1px solid #45475a;
    border-radius: 4px;
    padding: 5px 10px;
    color: #cdd6f4;
    selection-background-color: #89b4fa;
}
QLineEdit:focus { border-color: #89b4fa; }
QLineEdit:read-only { background: #2a2a3c; color: #a6adc8; }
QTextEdit {
    background: #313244;
    border: 1px solid #45475a;
    border-radius: 4px;
    padding: 6px;
    color: #cdd6f4;
}
QTextEdit:focus { border-color: #89b4fa; }
QPushButton {
    background: #45475a;
    color: #cdd6f4;
    border: 1px solid #585b70;
    border-radius: 4px;
    padding: 6px 16px;
    font-size: 13px;
}
QPushButton:hover { background: #585b70; }
QPushButton:pressed { background: #313244; }
QPushButton:disabled { background: #313244; color: #6c7086; border-color: #45475a; }
QTableWidget {
    background: #181825;
    border: 1px solid #45475a;
    border-radius: 4px;
    gridline-color: #313244;
    selection-background-color: #45475a;
    selection-color: #cdd6f4;
    alternate-background-color: #1e1e2e;
}
QTableWidget::item { padding: 4px 6px; border: none; }
QTableWidget::item:selected { background: #45475a; }
QHeaderView::section {
    background: #313244;
    border: none;
    border-right: 1px solid #45475a;
    border-bottom: 1px solid #45475a;
    padding: 5px 8px;
    font-weight: bold;
    font-size: 12px;
    color: #89b4fa;
}
QHeaderView { background: #313244; }
QCheckBox { spacing: 6px; color: #cdd6f4; }
QCheckBox::indicator {
    width: 15px; height: 15px;
    border: 1px solid #585b70;
    border-radius: 3px;
    background: #313244;
}
QCheckBox::indicator:checked {
    background: #89b4fa;
    border-color: #89b4fa;
}
QSpinBox {
    background: #313244;
    border: 1px solid #45475a;
    border-radius: 4px;
    padding: 3px 5px;
    color: #cdd6f4;
}
QSpinBox::up-button, QSpinBox::down-button {
    background: #45475a; border: none; width: 16px;
}
QSpinBox::up-button:hover, QSpinBox::down-button:hover { background: #585b70; }
QProgressBar {
    background: #313244;
    border: 1px solid #45475a;
    border-radius: 4px;
    text-align: right;
    padding-right: 6px;
    font-size: 11px;
    color: #a6adc8;
    min-height: 20px;
}
QProgressBar::chunk {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #89b4fa, stop:1 #74c7ec);
    border-radius: 4px;
}
QStatusBar {
    background: #181825;
    border-top: 1px solid #45475a;
    font-size: 12px;
    color: #a6adc8;
}
QStatusBar QLabel { background: transparent; }
QGroupBox {
    border: 1px solid #45475a;
    border-radius: 6px;
    margin-top: 12px;
    background: #24273a;
    font-weight: bold;
    font-size: 13px;
    color: #89b4fa;
    padding-top: 4px;
}
QGroupBox::title {
    subcontrol-origin: margin;
    left: 10px;
    padding: 0 6px;
    background: #24273a;
    color: #89b4fa;
}
QScrollBar:vertical {
    background: #181825; width: 8px; border-radius: 4px;
}
QScrollBar::handle:vertical {
    background: #45475a; border-radius: 4px; min-height: 20px;
}
QScrollBar::handle:vertical:hover { background: #585b70; }
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0; }
QScrollBar:horizontal {
    background: #181825; height: 8px; border-radius: 4px;
}
QScrollBar::handle:horizontal {
    background: #45475a; border-radius: 4px; min-width: 20px;
}
QScrollBar::handle:horizontal:hover { background: #585b70; }
QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal { width: 0; }
QMenu {
    background: #313244;
    border: 1px solid #45475a;
    border-radius: 6px;
    padding: 4px;
}
QMenu::item { padding: 6px 20px; border-radius: 4px; color: #cdd6f4; }
QMenu::item:selected { background: #45475a; color: #89b4fa; }
QListWidget {
    background: #181825;
    border: 1px solid #45475a;
    border-radius: 4px;
    font-size: 12px;
}
QListWidget::item { padding: 3px 6px; }
QListWidget::item:selected { background: #45475a; color: #89b4fa; }
QMenuBar {
    background: #11111b;
    color: #cdd6f4;
}
"""

class ChromeKeyboardFilter(QObject):
    """Forward keyboard events từ PyQt container sang Chrome window"""
    
    def __init__(self, chrome_hwnd_getter):
        super().__init__()
        self.chrome_hwnd_getter = chrome_hwnd_getter
        # Map Qt key codes sang Windows Virtual Key codes
        self.vk_map = {
            Qt.Key_Return: 0x0D,
            Qt.Key_Enter: 0x0D,
            Qt.Key_Tab: 0x09,
            Qt.Key_Backspace: 0x08,
            Qt.Key_Delete: 0x2E,
            Qt.Key_Escape: 0x1B,
            Qt.Key_Left: 0x25,
            Qt.Key_Right: 0x27,
            Qt.Key_Up: 0x26,
            Qt.Key_Down: 0x28,
            Qt.Key_Home: 0x24,
            Qt.Key_End: 0x23,
            Qt.Key_PageUp: 0x21,
            Qt.Key_PageDown: 0x22,
            Qt.Key_Insert: 0x2D,
            Qt.Key_Control: 0xA2,
            Qt.Key_Shift: 0xA0,
            Qt.Key_Alt: 0xA4,
            Qt.Key_Space: 0x20,
        }
    
    def eventFilter(self, obj, event):
        chrome_hwnd = self.chrome_hwnd_getter()
        
        if not chrome_hwnd:
            return False
        
        if event.type() == QEvent.KeyPress:
            return self._forward_keypress(event, chrome_hwnd)
        
        return False
    
    def _forward_keypress(self, event, hwnd):
        """Forward keyboard event sang Chrome"""
        try:
            text = event.text()
            qkey = event.key()
            
            # Nếu là printable character, send WM_CHAR
            if text and ord(text[0]) >= 32 and ord(text[0]) != 127:
                # Send char
                win32gui.PostMessage(hwnd, 0x0102, ord(text[0]), 0)  # WM_CHAR
                return True
            
            # Nếu là special key, send WM_KEYDOWN
            vk = self.vk_map.get(qkey)
            if vk:
                # WM_KEYDOWN
                win32gui.PostMessage(hwnd, 0x0100, vk, 0)
                # WM_KEYUP
                win32gui.PostMessage(hwnd, 0x0101, vk, 0)
                return True
            
        except Exception as e:
            print(f"[DEBUG] Keyboard forward error: {e}", flush=True)
        
        return False


class ResizableContainer(QWidget):
    resized = pyqtSignal()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.resized.emit()

    def moveEvent(self, event):
        super().moveEvent(event)
        self.resized.emit()

# ── Button style helpers ──────────────────────────────────────────────────────
def _btn(bg, bg_h, fg="#ffffff", fs=13, pad=8, bold=True, radius=4):
    b = "font-weight:bold;" if bold else ""
    return (f"QPushButton{{background:{bg};color:{fg};border:none;border-radius:{radius}px;"
            f"{b}font-size:{fs}px;padding:{pad}px;}}"
            f"QPushButton:hover{{background:{bg_h};}}"
            f"QPushButton:disabled{{background:#313244;color:#6c7086;}}")

BTN_GREEN = lambda fs=13, p=8: _btn("#40a02b", "#4caf30", fs=fs, pad=p)
BTN_RED   = lambda fs=13, p=8: _btn("#d20f39", "#e81144", fs=fs, pad=p)
BTN_BLUE  = lambda fs=13, p=6: _btn("#1e66f5", "#3b82f6", fs=fs, pad=p)
BTN_GRAY  = ("QPushButton{background:#313244;color:#cdd6f4;border:1px solid #45475a;"
             "border-radius:4px;font-size:13px;padding:5px 12px;}"
             "QPushButton:hover{background:#45475a;}")
BTN_NAV   = ("QPushButton{background:#313244;color:#cdd6f4;border:1px solid #45475a;"
             "border-radius:4px;font-size:14px;padding:2px 8px;"
             "min-width:30px;min-height:30px;}"
             "QPushButton:hover{background:#45475a;color:#89b4fa;}"
             "QPushButton:disabled{color:#45475a;background:#1e1e2e;border-color:#313244;}")

driver = None

# ═══════════════════════════════════════════════════════════════════════════════
#  AI CONFIG DIALOG
# ═══════════════════════════════════════════════════════════════════════════════
class AIConfigDialog(QDialog):
    """Dialog cấu hình AI - với text điều khiển, chọn model, key Groq, link tạo key"""
    
    def __init__(self, profile_name: str, parent=None):
        super().__init__(parent)
        self.profile_name = profile_name
        self.setWindowTitle(f"⚙ Cấu hình AI - {profile_name}")
        self.setFixedSize(650, 500)
        self.setStyleSheet(DARK)
        self._ai_config_file = self._get_config_path()
        self._build()
        self._load_config()

    def _get_config_path(self) -> str:
        """Đường dẫn file lưu AI config cho profile này"""
        base = os.path.dirname(os.path.abspath(__file__))
        data = os.path.join(base, "data")
        os.makedirs(data, exist_ok=True)
        return os.path.join(data, f"ai_config_{self.profile_name}.json")

    def _build(self):
        lay = QVBoxLayout(self)
        lay.setSpacing(12)
        lay.setContentsMargins(18, 18, 18, 18)

        # Tiêu đề
        title = QLabel("🤖  ĐIỀU KHIỂN AI")
        title.setFont(QFont("Segoe UI", 13, QFont.Bold))
        title.setStyleSheet("color:#89b4fa;background:transparent;")
        lay.addWidget(title)

        # ─────────────────────────
        # Phần 1: Prompt điều khiển
        # ─────────────────────────
        gb1 = QGroupBox("📝  Prompt điều khiển AI")
        gb1_lay = QVBoxLayout(gb1)
        gb1_lay.setContentsMargins(12, 8, 12, 10)
        
        hint = QLabel("💡 Hướng dẫn: Viết lệnh cho AI để viết lại bài viết. VD: 'Viết lại bài trên tông nhẹ nhàng, tươi vui'")
        hint.setStyleSheet("color:#6c7086;font-size:11px;font-style:italic;background:transparent;")
        hint.setWordWrap(True)
        gb1_lay.addWidget(hint)
        
        self.ai_prompt = QTextEdit()
        self.ai_prompt.setPlaceholderText("Nhập prompt điều khiển AI tại đây...")
        self.ai_prompt.setFixedHeight(100)
        self.ai_prompt.setStyleSheet(
            "QTextEdit{background:#181825;border:1px solid #45475a;border-radius:6px;"
            "font-size:12px;color:#cdd6f4;padding:8px;}"
            "QTextEdit:focus{border-color:#89b4fa;}")
        gb1_lay.addWidget(self.ai_prompt)
        lay.addWidget(gb1)

        # ─────────────────────────
        # Phần 2: Chọn model AI
        # ─────────────────────────
        gb2 = QGroupBox("🧠  Chọn Model AI")
        gb2_lay = QHBoxLayout(gb2)
        gb2_lay.setContentsMargins(12, 8, 12, 10)
        gb2_lay.setSpacing(10)
        
        lbl_model = QLabel("Model:")
        lbl_model.setStyleSheet("background:transparent;color:#a6adc8;font-weight:bold;")
        self.ai_model = QComboBox()
        # Hiển thị tên dễ hiểu, backend lưu tên thực
        self.ai_model.addItems([
            "🚀 Llama 3.3 (Nhanh - Khuyến nghị)",
            "⚖️ Mixtral 8x7b (Cân bằng)",
            "🔧 Llama 3.1 (Khác)"
        ])
        self.ai_model.setFixedWidth(280)
        self.ai_model.setStyleSheet(
            "QComboBox{background:#313244;border:1px solid #45475a;border-radius:4px;"
            "color:#cdd6f4;padding:4px 8px;font-size:12px;}"
            "QComboBox:focus{border-color:#89b4fa;}"
            "QComboBox::drop-down{border:none;}"
            "QComboBox QAbstractItemView{background:#313244;color:#cdd6f4;}")
        
        gb2_lay.addWidget(lbl_model)
        gb2_lay.addWidget(self.ai_model)
        gb2_lay.addStretch()
        lay.addWidget(gb2)

        # ─────────────────────────
        # Phần 3: Key Groq
        # ─────────────────────────
        gb3 = QGroupBox("🔐  Key Groq / API Key")
        gb3_lay = QVBoxLayout(gb3)
        gb3_lay.setContentsMargins(12, 8, 12, 10)
        gb3_lay.setSpacing(6)
        
        row_key = QHBoxLayout()
        row_key.setSpacing(6)
        
        self.groq_key = QLineEdit()
        self.groq_key.setPlaceholderText("Nhập Groq API Key...")
        self.groq_key.setEchoMode(QLineEdit.Password)  # Ẩn key
        self.groq_key.setStyleSheet(
            "QLineEdit{background:#181825;border:1px solid #45475a;border-radius:4px;"
            "padding:6px 10px;font-size:12px;color:#cdd6f4;}"
            "QLineEdit:focus{border-color:#89b4fa;}")
        
        btn_show = QPushButton("👁 Hiện")
        btn_show.setFixedWidth(70)
        btn_show.setStyleSheet(BTN_GRAY)
        btn_show.clicked.connect(lambda: self.groq_key.setEchoMode(
            QLineEdit.Normal if self.groq_key.echoMode() == QLineEdit.Password else QLineEdit.Password))
        
        row_key.addWidget(self.groq_key, 1)
        row_key.addWidget(btn_show)
        gb3_lay.addLayout(row_key)
        
        # Link tạo key
        row_link = QHBoxLayout()
        row_link.setSpacing(6)
        lbl_link = QLabel("🔗 Tạo API Key:")
        lbl_link.setStyleSheet("background:transparent;color:#a6adc8;font-weight:bold;font-size:11px;")
        btn_create = QPushButton("→ console.groq.com")
        btn_create.setStyleSheet(
            "QPushButton{background:transparent;color:#89b4fa;border:1px solid #89b4fa;"
            "border-radius:4px;padding:4px 12px;font-size:11px;font-weight:bold;}"
            "QPushButton:hover{background:#89b4fa;color:#1e1e2e;}")
        btn_create.clicked.connect(lambda: self._open_groq_console())
        row_link.addWidget(lbl_link)
        row_link.addWidget(btn_create)
        row_link.addStretch()
        gb3_lay.addLayout(row_link)
        
        lay.addWidget(gb3)

        # ─────────────────────────
        # Nút Lưu / Hủy
        # ─────────────────────────
        row_btn = QHBoxLayout()
        row_btn.setSpacing(8)
        
        btn_save = QPushButton("💾  LƯU CẤU HÌNH")
        btn_save.setStyleSheet(BTN_GREEN(12, 8))
        btn_save.setFixedHeight(36)
        btn_save.clicked.connect(self._save_config)
        
        btn_cancel = QPushButton("✕  HỦY")
        btn_cancel.setStyleSheet(BTN_GRAY)
        btn_cancel.setFixedHeight(36)
        btn_cancel.clicked.connect(self.reject)
        
        row_btn.addWidget(btn_save, 1)
        row_btn.addWidget(btn_cancel, 1)
        lay.addLayout(row_btn)

    def _get_model_map(self) -> dict:
        """Map giữa display name và actual model name"""
        return {
            "🚀 Llama 3.3 (Nhanh - Khuyến nghị)": "llama-3.3-70b-versatile",
            "⚖️ Mixtral 8x7b (Cân bằng)": "mixtral-8x7b-32768",
            "🔧 Llama 3.1 (Khác)": "llama-3.1-70b-versatile",
            # Support tên cũ
            "llama-3.3-70b-versatile": "llama-3.3-70b-versatile",
            "mixtral-8x7b-32768": "mixtral-8x7b-32768",
            "llama-3.1-70b-versatile": "llama-3.1-70b-versatile",
        }
    
    def _display_name_to_model(self, display_name: str) -> str:
        """Convert display name thành actual model name"""
        model_map = self._get_model_map()
        return model_map.get(display_name, "llama-3.3-70b-versatile")
    
    def _model_to_display_name(self, model_name: str) -> str:
        """Convert actual model name thành display name"""
        reverse_map = {v: k for k, v in self._get_model_map().items()}
        # Trả về display name, nếu không tìm thì trả về model name gốc
        return list(reverse_map.values())[list(reverse_map.keys()).index(model_name)] if model_name in reverse_map else model_name

    def _open_groq_console(self):
        """Mở link tạo Groq API key với Chrome"""
        try:
            # Tìm Chrome executable
            chrome_path = self._get_chrome_path()
            if chrome_path and os.path.exists(chrome_path):
                subprocess.Popen([chrome_path, "https://console.groq.com/keys"])
            else:
                # Fallback: mở với trình duyệt mặc định
                import webbrowser
                webbrowser.open("https://console.groq.com/keys")
        except Exception as e:
            print(f"[ERROR] Lỗi mở Chrome: {e}", flush=True)
        
        QMessageBox.information(self, "Groq Console", 
            "✅ Đã mở: https://console.groq.com/keys\n\n"
            "1. Đăng nhập hoặc tạo tài khoản Groq\n"
            "2. Tạo API Key mới\n"
            "3. Copy và dán vào ô 'Key Groq' ở đây")
    
    def _get_chrome_path(self) -> str:
        """Lấy đường dẫn Chrome executable"""
        base_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Cách 1: Chrome trong thư mục chrome-win
        chrome_win_path = os.path.join(base_dir, "chrome-win", "chrome.exe")
        if os.path.exists(chrome_win_path):
            return chrome_win_path
        
        # Cách 2: Chrome chuẩn trong system
        possible_paths = [
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
            os.path.expandvars(r"%ProgramFiles%\Google\Chrome\Application\chrome.exe"),
            os.path.expandvars(r"%ProgramFiles(x86)%\Google\Chrome\Application\chrome.exe"),
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                return path
        
        return None

    def _save_config(self):
        """Lưu cấu hình AI vào file JSON"""
        display_name = self.ai_model.currentText()
        actual_model = self._display_name_to_model(display_name)
        
        config = {
            'ai_prompt': self.ai_prompt.toPlainText().strip(),
            'ai_model': actual_model,  # Lưu actual model name, không phải display name
            'groq_key': self.groq_key.text().strip(),
        }
        
        try:
            with open(self._ai_config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=2)
            QMessageBox.information(self, "Thành công", "✅ Cấu hình AI đã được lưu!")
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"❌ Lỗi lưu cấu hình: {e}")

    def _load_config(self):
        """Load cấu hình AI từ file nếu tồn tại"""
        if os.path.isfile(self._ai_config_file):
            try:
                with open(self._ai_config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                self.ai_prompt.setPlainText(config.get('ai_prompt', ''))
                
                # Load model - convert actual model name thành display name
                model_val = config.get('ai_model', 'llama-3.3-70b-versatile')
                
                # Map cái tên cũ thành actual model name nếu cần
                old_to_new = {
                    'ChatGPT': 'llama-3.3-70b-versatile',
                    'Llama': 'llama-3.3-70b-versatile',
                    'Claude': 'mixtral-8x7b-32768'
                }
                model_val = old_to_new.get(model_val, model_val)
                
                # Tìm display name của model này
                model_map = self._get_model_map()
                display_name = [k for k, v in model_map.items() if v == model_val and '🚀' in k or '⚖️' in k or '🔧' in k]
                if display_name:
                    self.ai_model.setCurrentText(display_name[0])
                else:
                    self.ai_model.setCurrentIndex(0)  # Default: Llama 3.3
                
                self.groq_key.setText(config.get('groq_key', ''))
            except Exception as e:
                print(f"[AI CONFIG] Load lỗi: {e}")

    def get_config(self) -> dict:
        """Lấy cấu hình hiện tại - lưu actual model name"""
        display_name = self.ai_model.currentText()
        actual_model = self._display_name_to_model(display_name)
        
        return {
            'ai_prompt': self.ai_prompt.toPlainText().strip(),
            'ai_model': actual_model,  # Lưu actual model name
            'groq_key': self.groq_key.text().strip(),
        }


# ═══════════════════════════════════════════════════════════════════════════════
#  GROUP FILTER DIALOG
# ═══════════════════════════════════════════════════════════════════════════════
class GroupFilterDialog(QDialog):
    """Dialog lọc nhóm theo tiêu chí - thiết kế chip-button chuyên nghiệp"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("⬇  Lọc Nhóm")
        self.setFixedSize(580, 340)
        self.setStyleSheet(DARK)
        self.selected_filters = []
        self.filter_buttons = {}  # code -> button
        self._build()

    def _build(self):
        lay = QVBoxLayout(self)
        lay.setSpacing(0)
        lay.setContentsMargins(0, 0, 0, 0)

        # Header
        header = QWidget()
        header.setFixedHeight(55)
        header.setStyleSheet("background:linear-gradient(90deg, #0f0f1e 0%, #1a1a2e 100%);border-bottom:2px solid #89b4fa;")
        h_lay = QVBoxLayout(header)
        h_lay.setContentsMargins(24, 10, 24, 10)
        title = QLabel("🔍  CHỌN TIÊU CHÍ LỌC")
        title.setFont(QFont("Segoe UI", 12, QFont.Bold))
        title.setStyleSheet("color:#89b4fa;background:transparent;")
        h_lay.addWidget(title)
        lay.addWidget(header)

        # Content - Chip buttons
        content = QWidget()
        content_lay = QVBoxLayout(content)
        content_lay.setSpacing(14)
        content_lay.setContentsMargins(24, 24, 24, 20)
        
        filters = [
            ("🔥  Chạy gần nhất", "recent"),
            ("⏳  Chạy lâu nhất", "oldest"),
            ("📊  Chạy ít nhất", "least"),
            ("⭐  Chạy nhiều nhất", "most"),
            ("🆕  Chưa chạy lần nào", "never"),
        ]
        
        for label, code in filters:
            btn = self._create_chip_button(label, code)
            content_lay.addWidget(btn)
        
        content_lay.addStretch()
        lay.addWidget(content, 1)

        # Footer - Action buttons
        footer = QWidget()
        footer.setFixedHeight(65)
        footer.setStyleSheet("background:#0f0f1e;border-top:1px solid #45475a;")
        f_lay = QVBoxLayout(footer)
        f_lay.setContentsMargins(24, 12, 24, 12)
        
        row_btn = QHBoxLayout()
        row_btn.setSpacing(12)
        
        btn_apply = QPushButton("✓  LỌचTRỪ")
        btn_apply.setStyleSheet(
            "QPushButton{background:linear-gradient(135deg, #40a02b 0%, #2d8c1a 100%);color:white;border:none;"
            "border-radius:8px;font-weight:bold;font-size:11px;padding:0 24px;}"
            "QPushButton:hover{background:linear-gradient(135deg, #45ad32 0%, #318521 100%);}"
            "QPushButton:pressed{background:#2d8c1a;}")
        btn_apply.setFixedHeight(40)
        btn_apply.setFont(QFont("Segoe UI", 11, QFont.Bold))
        btn_apply.clicked.connect(self._apply_filter)
        
        btn_cancel = QPushButton("✕  HỦY")
        btn_cancel.setStyleSheet(
            "QPushButton{background:#313244;color:#cdd6f4;border:1px solid #45475a;"
            "border-radius:8px;font-weight:bold;font-size:11px;padding:0 24px;}"
            "QPushButton:hover{background:#3a3a4d;border-color:#89b4fa;}"
            "QPushButton:pressed{background:#2a2a3c;}")
        btn_cancel.setFixedHeight(40)
        btn_cancel.setFont(QFont("Segoe UI", 11, QFont.Bold))
        btn_cancel.clicked.connect(self.reject)
        
        row_btn.addWidget(btn_apply, 1)
        row_btn.addWidget(btn_cancel, 1)
        f_lay.addLayout(row_btn)
        lay.addWidget(footer)
    
    def _create_chip_button(self, label, code):
        """Tạo chip-button style chuyên nghiệp"""
        btn = QPushButton(label)
        btn.setFixedHeight(42)
        btn.setCheckable(True)
        btn.setStyleSheet(
            "QPushButton{background:#1e1e2e;color:#cdd6f4;border:2px solid #45475a;border-radius:8px;"
            "font-size:11px;font-weight:bold;padding:0 16px;text-align:left;}"
            "QPushButton:hover{background:#252535;border-color:#89b4fa;}"
            "QPushButton:checked{background:#40a02b;color:#1e1e2e;border-color:#40a02b;}"
            "QPushButton:pressed{background:#3a8f26;}")
        btn.setFont(QFont("Segoe UI", 10, QFont.Bold))
        self.filter_buttons[code] = btn
        return btn

    def _apply_filter(self):
        """Lấy danh sách filter được chọn"""
        self.selected_filters = []
        for code, btn in self.filter_buttons.items():
            if btn.isChecked():
                self.selected_filters.append(code)
        
        self.accept()

    def get_filters(self):
        """Lấy danh sách filter đã chọn"""
        return self.selected_filters


# ═══════════════════════════════════════════════════════════════════════════════
#  CONTENT MANAGER DIALOG
# ═══════════════════════════════════════════════════════════════════════════════
class ContentManagerDialog(QDialog):
    """Dialog quản lý nội dung - lưu, xem, copy các nội dung đã tạo"""
    
    def __init__(self, profile_name: str, parent=None):
        super().__init__(parent)
        self.profile_name = profile_name
        self.contents = []  # Danh sách nội dung đã lưu
        self.selected_content_idx = 0
        self.setWindowTitle(f"📝  Quản lý Nội dung - {profile_name}")
        self.setFixedSize(900, 500)
        self.setStyleSheet(DARK)
        self._content_file = self._get_content_path()
        self._load_contents()
        self._build()

    def _get_content_path(self) -> str:
        """Đường dẫn file lưu nội dung cho profile này"""
        base = os.path.dirname(os.path.abspath(__file__))
        data = os.path.join(base, "data")
        os.makedirs(data, exist_ok=True)
        return os.path.join(data, f"contents_{self.profile_name}.json")

    def _load_contents(self):
        """Load nội dung từ file JSON"""
        if os.path.isfile(self._content_file):
            try:
                with open(self._content_file, 'r', encoding='utf-8') as f:
                    self.contents = json.load(f)
            except Exception as e:
                print(f"[CONTENT] Load lỗi: {e}")
                self.contents = []

    def _save_contents(self):
        """Lưu nội dung vào file JSON"""
        try:
            with open(self._content_file, 'w', encoding='utf-8') as f:
                json.dump(self.contents, f, ensure_ascii=False, indent=2)
            print(f"[CONTENT] Đã lưu {len(self.contents)} nội dung")
        except Exception as e:
            print(f"[CONTENT] Save lỗi: {e}")

    def _build(self):
        lay = QVBoxLayout(self)
        lay.setSpacing(12)
        lay.setContentsMargins(18, 18, 18, 18)

        # ──── Tiêu đề ────
        title = QLabel("📝  QUẢN LÝ NỘI DUNG")
        title.setFont(QFont("Segoe UI", 13, QFont.Bold))
        title.setStyleSheet("color:#89b4fa;background:transparent;")
        lay.addWidget(title)

        # ──── Phần thêm nội dung mới ────
        gb_add = QGroupBox("➕  Thêm nội dung mới")
        gb_add_lay = QVBoxLayout(gb_add)
        gb_add_lay.setContentsMargins(12, 8, 12, 10)
        gb_add_lay.setSpacing(6)
        
        self.input_content = QTextEdit()
        self.input_content.setPlaceholderText("Nhập nội dung mới tại đây... (1 nội dung)")
        self.input_content.setFixedHeight(80)
        self.input_content.setStyleSheet(
            "QTextEdit{background:#181825;border:1px solid #45475a;border-radius:4px;"
            "font-size:12px;color:#cdd6f4;padding:8px;}"
            "QTextEdit:focus{border-color:#89b4fa;}")
        gb_add_lay.addWidget(self.input_content)
        
        row_btn = QHBoxLayout()
        row_btn.setSpacing(6)
        
        btn_add = QPushButton("✚  THÊM NỘI DUNG")
        btn_add.setStyleSheet(BTN_GREEN(12, 8))
        btn_add.setFixedHeight(32)
        btn_add.clicked.connect(self._add_content)
        
        btn_clear_input = QPushButton("⊘  Clear")
        btn_clear_input.setStyleSheet(BTN_GRAY)
        btn_clear_input.setFixedHeight(32)
        btn_clear_input.setFixedWidth(80)
        btn_clear_input.clicked.connect(self.input_content.clear)
        
        row_btn.addWidget(btn_add, 1)
        row_btn.addWidget(btn_clear_input)
        gb_add_lay.addLayout(row_btn)
        lay.addWidget(gb_add)

        # ──── Phần chính: Danh sách + Xem chi tiết ────
        main_lay = QHBoxLayout()
        main_lay.setSpacing(12)

        # Bên TRÁI: Danh sách nội dung (như button)
        gb_list = QGroupBox("📋  Danh sách nội dung đã lưu")
        gb_list_lay = QVBoxLayout(gb_list)
        gb_list_lay.setContentsMargins(8, 8, 8, 8)
        gb_list_lay.setSpacing(6)
        
        self.scroll_contents = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_contents)
        self.scroll_layout.setContentsMargins(0, 0, 0, 0)
        self.scroll_layout.setSpacing(6)
        self.content_buttons = []  # Danh sách button để update styling
        
        scroll_area = QScrollArea()
        scroll_area.setWidget(self.scroll_contents)
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet(
            "QScrollArea{background:#11111b;border:none;}"
            "QScrollBar:vertical{background:#313244;border:none;width:10px;}"
            "QScrollBar::handle:vertical{background:#45475a;border-radius:5px;}"
            "QScrollBar::handle:vertical:hover{background:#585b70;}")
        gb_list_lay.addWidget(scroll_area)
        main_lay.addWidget(gb_list, 1)

        # Bên PHẢI: Xem chi tiết + Copy
        gb_view = QGroupBox("👁  Xem chi tiết")
        gb_view_lay = QVBoxLayout(gb_view)
        gb_view_lay.setContentsMargins(8, 8, 8, 8)
        gb_view_lay.setSpacing(6)
        
        self.view_content = QTextEdit()
        self.view_content.setReadOnly(True)
        self.view_content.setStyleSheet(
            "QTextEdit{background:#181825;border:1px solid #45475a;border-radius:4px;"
            "font-size:12px;color:#cdd6f4;padding:8px;font-family:'Segoe UI';}")
        gb_view_lay.addWidget(self.view_content, 1)
        
        row_action = QHBoxLayout()
        row_action.setSpacing(6)
        
        btn_copy = QPushButton("📋  Copy")
        btn_copy.setStyleSheet(BTN_GREEN(12, 6))
        btn_copy.setFixedHeight(28)
        btn_copy.clicked.connect(self._copy_content)
        
        btn_delete = QPushButton("🗑  Xóa")
        btn_delete.setStyleSheet(
            "QPushButton{background:#f38ba8;color:white;border:none;border-radius:4px;"
            "padding:6px 12px;font-size:11px;font-weight:bold;}"
            "QPushButton:hover{background:#d94477;}")
        btn_delete.setFixedHeight(28)
        btn_delete.clicked.connect(self._delete_content)
        
        row_action.addWidget(btn_copy, 1)
        row_action.addWidget(btn_delete, 1)
        gb_view_lay.addLayout(row_action)
        main_lay.addWidget(gb_view, 1)

        lay.addLayout(main_lay, 1)

        # ──── Nút đóng ────
        btn_close = QPushButton("✕  Đóng")
        btn_close.setStyleSheet(BTN_GRAY)
        btn_close.setFixedHeight(32)
        btn_close.clicked.connect(self.close)
        lay.addWidget(btn_close)

        # Refresh UI danh sách
        self._refresh_content_buttons()

    def _refresh_content_buttons(self):
        """Làm sạch và tạo lại danh sách nút nội dung"""
        # Xóa layout cũ
        while self.scroll_layout.count():
            item = self.scroll_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        self.content_buttons = []  # Reset danh sách button

        if not self.contents:
            lbl = QLabel("Chưa có nội dung nào")
            lbl.setStyleSheet("color:#6c7086;font-style:italic;background:transparent;")
            lbl.setAlignment(Qt.AlignCenter)
            self.scroll_layout.addWidget(lbl)
            self.view_content.clear()
            return

        # Tạo button cho mỗi nội dung
        for idx, content_item in enumerate(self.contents):
            text = content_item if isinstance(content_item, str) else content_item.get('text', '')
            # Lấy preview (50 ký tự đầu)
            preview = text[:50] + "..." if len(text) > 50 else text
            
            btn = QPushButton(f"{idx + 1}. {preview}")
            btn.setFixedHeight(50)
            btn.setStyleSheet(
                f"QPushButton{{background:{'#89b4fa' if idx == self.selected_content_idx else '#313244'};"
                f"color:{'#1e1e2e' if idx == self.selected_content_idx else '#cdd6f4'};"
                f"border:1px solid #45475a;border-radius:4px;padding:8px;text-align:left;white-space:pre-wrap;"
                f"font-size:11px;font-weight:bold;}}"
                f"QPushButton:hover{{background:#45475a;}}")
            btn.clicked.connect(lambda checked, i=idx: self._select_content(i))
            btn._content_idx = idx  # Lưu index để dùng sau
            self.scroll_layout.addWidget(btn)
            self.content_buttons.append(btn)

        self.scroll_layout.addStretch()
        # Chọn nội dung đầu tiên mà không refresh button (vì button đã được tạo)
        if len(self.contents) > 0:
            self.selected_content_idx = min(self.selected_content_idx, len(self.contents) - 1)
            content = self.contents[self.selected_content_idx]
            text = content if isinstance(content, str) else content.get('text', '')
            self.view_content.setPlainText(text)

    def _select_content(self, idx: int):
        """Chọn và hiển thị nội dung"""
        if 0 <= idx < len(self.contents):
            self.selected_content_idx = idx
            content = self.contents[idx]
            text = content if isinstance(content, str) else content.get('text', '')
            self.view_content.setPlainText(text)
            # Update button styles khi chọn nội dung mới
            self._update_button_styles()

    def _update_button_styles(self):
        """Cập nhật styling của các button dựa trên lựa chọn hiện tại"""
        for btn in self.content_buttons:
            idx = btn._content_idx
            is_selected = (idx == self.selected_content_idx)
            btn.setStyleSheet(
                f"QPushButton{{background:{'#89b4fa' if is_selected else '#313244'};"
                f"color:{'#1e1e2e' if is_selected else '#cdd6f4'};"
                f"border:1px solid #45475a;border-radius:4px;padding:8px;text-align:left;white-space:pre-wrap;"
                f"font-size:11px;font-weight:bold;}}"
                f"QPushButton:hover{{background:#45475a;}}")

    def _add_content(self):
        """Thêm nội dung mới"""
        text = self.input_content.toPlainText().strip()
        if not text:
            QMessageBox.warning(self, "Cảnh báo", "⚠ Vui lòng nhập nội dung!")
            return
        
        self.contents.append(text)
        self._save_contents()
        self.input_content.clear()
        self._refresh_content_buttons()
        QMessageBox.information(self, "Thành công", "✅ Đã thêm nội dung!")

    def _delete_content(self):
        """Xóa nội dung đang chọn"""
        if 0 <= self.selected_content_idx < len(self.contents):
            if QMessageBox.question(self, "Xác nhận", "Bạn chắc chắn muốn xóa nội dung này?",
                                   QMessageBox.Yes | QMessageBox.No) == QMessageBox.Yes:
                self.contents.pop(self.selected_content_idx)
                self._save_contents()
                if self.selected_content_idx >= len(self.contents):
                    self.selected_content_idx = max(0, len(self.contents) - 1)
                self._refresh_content_buttons()
                QMessageBox.information(self, "Thành công", "✅ Đã xóa nội dung!")

    def _copy_content(self):
        """Copy nội dung hiện tại"""
        text = self.view_content.toPlainText()
        if text:
            QApplication.clipboard().setText(text)
            QMessageBox.information(self, "Thành công", "✅ Đã copy nội dung vào clipboard!")
        else:
            QMessageBox.warning(self, "Cảnh báo", "⚠ Nội dung trống!")




# ═══════════════════════════════════════════════════════════════════════════════
#  LICENSE DIALOG
# ═══════════════════════════════════════════════════════════════════════════════
class LicenseDialog(QDialog):
    activated = pyqtSignal()

    def __init__(self, machine_id, parent=None):
        super().__init__(parent)
        self.machine_id = machine_id
        self.key_checker = KeyChecker()
        self.setWindowTitle("License - Kích hoạt phần mềm")
        self.setFixedSize(550, 360)
        self.setStyleSheet(DARK)
        self.setWindowFlags(
            Qt.Window |
            Qt.CustomizeWindowHint |
            Qt.WindowTitleHint  # Chỉ giữ title, không có nút X, _, □
        )
        self._build()

    def keyPressEvent(self, e):
        """Ngăn chặn ESC"""
        if e.key() != Qt.Key_Escape:
            super().keyPressEvent(e)

    def closeEvent(self, e):
        """Không cho phép đóng nếu chưa có key hợp lệ"""
        e.ignore()

    def _build(self):
        lay = QVBoxLayout(self)
        lay.setSpacing(12)
        lay.setContentsMargins(22, 22, 22, 22)

        t = QLabel("🔑  KÍCH HOẠT PHẦN MỀM")
        t.setFont(QFont("Segoe UI", 14, QFont.Bold))
        t.setStyleSheet("color:#89b4fa;background:transparent;")
        lay.addWidget(t)

        sep = QFrame()
        sep.setFrameShape(QFrame.HLine)
        sep.setStyleSheet("background:#45475a;max-height:1px;")
        lay.addWidget(sep)

        # ID máy
        id_box = QGroupBox("ℹ️  Thông tin máy")
        id_lay = QHBoxLayout(id_box)
        id_lay.setContentsMargins(8, 8, 8, 8)
        self.mid = QLineEdit(self.machine_id)
        self.mid.setReadOnly(True)
        self.mid.setStyleSheet(
            "QLineEdit{background:#11111b;color:#a6e3a1;font-weight:bold;"
            "font-family:'Courier New';font-size:13px;letter-spacing:2px;"
            "border:1px solid #45475a;border-radius:4px;padding:6px 10px;}")
        btn_c = QPushButton("📋 Copy")
        btn_c.setStyleSheet(BTN_GRAY)
        btn_c.setFixedWidth(80)
        btn_c.clicked.connect(lambda: QApplication.clipboard().setText(self.machine_id))
        id_lay.addWidget(self.mid, 1)
        id_lay.addWidget(btn_c)
        lay.addWidget(id_box)

        info = QLabel("📞 Liên hệ: Zalo 0327974700\n💬 Copy mã máy và gửi để nhận Key")
        info.setStyleSheet("color:#a6adc8;font-size:11px;background:transparent;")
        lay.addWidget(info)

        # Key input
        key_box = QGroupBox("🔐 Nhập Key kích hoạt")
        key_lay = QVBoxLayout(key_box)
        key_lay.setContentsMargins(8, 8, 8, 8)
        self.key = QLineEdit()
        self.key.setPlaceholderText("Nhập Key tại đây...")
        self.key.setFont(QFont("Courier New", 12))
        self.key.setFixedHeight(36)
        self.key.returnPressed.connect(self._activate)
        key_lay.addWidget(self.key)
        lay.addWidget(key_box)

        # Status
        self.st = QLabel("")
        self.st.setAlignment(Qt.AlignCenter)
        self.st.setStyleSheet("background:transparent;font-weight:bold;")
        self.st.setFixedHeight(24)
        lay.addWidget(self.st)

        # Button
        row = QHBoxLayout()
        bk = QPushButton("✅ KÍCH HOẠT")
        bk.setStyleSheet(BTN_GREEN(14, 10))
        bk.setFixedHeight(40)
        bk.clicked.connect(self._activate)
        row.addStretch()
        row.addWidget(bk)
        row.addStretch()
        lay.addLayout(row)

    def _activate(self):
        """Kiểm tra key"""
        key_input = self.key.text().strip()
        print(f"[LICENSE] User entered key: {key_input}")
        
        if not key_input:
            self.st.setStyleSheet("color:#f38ba8;background:transparent;")
            self.st.setText("❌ Vui lòng nhập Key")
            print(f"[LICENSE] ❌ Empty key input")
            return
        
        print(f"[LICENSE] 🔐 Validating key...")
        is_valid, message, key_data = self.key_checker.validate_key(key_input)
        print(f"[LICENSE] Result: is_valid={is_valid}, message='{message}'")
        
        self.st.setStyleSheet(f"color:{'#a6e3a1' if is_valid else '#f38ba8'};background:transparent;")
        self.st.setText(message)
        
        if is_valid:
            print(f"[LICENSE] ✅ Valid key, closing dialog...")
            self.key.setText("")
            self.key.setEnabled(False)
            self.activated.emit()
            QTimer.singleShot(1500, self.accept)
        else:
            print(f"[LICENSE] ❌ Invalid key, asking to retry...")
            self.key.clear()
            self.key.setFocus()
            QTimer.singleShot(2000, lambda: self.st.setText(""))


# ═══════════════════════════════════════════════════════════════════════════════
#  CHROMIUM WORKER
# ═══════════════════════════════════════════════════════════════════════════════
class ChromiumWorker(QThread):
    ready = pyqtSignal(object)

    def __init__(self, profile_name: str, parent=None):
        super().__init__(parent)
        self.profile_name = profile_name

    def run(self):
        try:
            print(f"[INFO] Mở Chrome cho profile: {self.profile_name}", flush=True)
            d = ChromiumDriver.get_driver(
                self.profile_name,
                start_url="https://www.facebook.com",
                no_images=True
            )
            self.ready.emit(d)
        except Exception as e:
            print(f"[ERROR] Lỗi mở Chrome: {e}", flush=True)
            self.ready.emit(None)


class GroupScannerWorker(QThread):
    result = pyqtSignal(dict)

    def __init__(self, driver, profile_name, parent=None):
        super().__init__(parent)
        self.driver = driver
        self.profile_name = profile_name

    def run(self):
        try:
            scanner = GroupScanner(self.driver, self.profile_name)
            res = scanner.scan_groups()
            self.result.emit(res)
        except Exception as e:
            print(f"[ERROR] Lỗi quét nhóm: {e}", flush=True)
            self.result.emit({
                'success': False,
                'message': f'Lỗi quét nhóm: {str(e)}',
                'groups': [],
            })


# ═══════════════════════════════════════════════════════════════════════════════
#  POST GROUPS WORKER  — FIX: truyền log_callback, success_callback, fail_callback
# ═══════════════════════════════════════════════════════════════════════════════
class PostGroupsWorker(QThread):
    log_signal     = pyqtSignal(str)
    success_signal = pyqtSignal(str, str, str)   # ts, group_name, post_url
    fail_signal    = pyqtSignal(str, str, str)    # ts, group_name, error

    def __init__(self, driver, data, parent=None):
        super().__init__(parent)
        self.driver = driver
        self.data   = data

    def run(self):
        try:
            from action.post_groups import PostGroups
            poster = PostGroups(
                self.driver,
                self.data,
                log_callback=self.log_signal.emit,
                success_callback=self.success_signal.emit,
                fail_callback=self.fail_signal.emit,
            )
            poster.main_post()
        except Exception as e:
            print(f"[ERROR] Lỗi đăng nhóm: {e}", flush=True)
            self.log_signal.emit(f'❌ Lỗi: {str(e)}')


# ═══════════════════════════════════════════════════════════════════════════════
#  COMMENT GROUPS WORKER  
# ═══════════════════════════════════════════════════════════════════════════════
class CommentGroupsWorker(QThread):
    log_signal     = pyqtSignal(str)
    success_signal = pyqtSignal(str, str, str)   # ts, post_url, group_name
    fail_signal    = pyqtSignal(str, str, str)    # ts, post_url, error

    def __init__(self, driver, data, parent=None):
        super().__init__(parent)
        self.driver = driver
        self.data   = data

    def run(self):
        try:
            from action.comment import CommentGroups
            cmter = CommentGroups(
                self.driver,
                self.data,
                log_callback=self.log_signal.emit,
                success_callback=self.success_signal.emit,
                fail_callback=self.fail_signal.emit,
            )
            cmter.execute()
        except Exception as e:
            print(f"[ERROR] Lỗi comment nhóm: {e}", flush=True)
            self.log_signal.emit(f'❌ Lỗi: {str(e)}')


# ═══════════════════════════════════════════════════════════════════════════════
#  UP TOP WORKER
# ═══════════════════════════════════════════════════════════════════════════════
class UpTopWorker(QThread):
    log_signal     = pyqtSignal(str)
    success_signal = pyqtSignal(str, str, str)   # ts, post_url, action_name
    fail_signal    = pyqtSignal(str, str, str)    # ts, post_url, error

    def __init__(self, driver, data, parent=None):
        super().__init__(parent)
        self.driver = driver
        self.data   = data

    def run(self):
        try:
            from action.uptop import UpTop
            uptop = UpTop(
                self.driver,
                self.data,
                log_callback=self.log_signal.emit,
                success_callback=self.success_signal.emit,
                fail_callback=self.fail_signal.emit,
            )
            uptop.execute()
        except Exception as e:
            print(f"[ERROR] Lỗi up top: {e}", flush=True)
            self.log_signal.emit(f'❌ Lỗi: {str(e)}')


# ═══════════════════════════════════════════════════════════════════════════════
#  FACEBOOK WINDOW
# ═══════════════════════════════════════════════════════════════════════════════
class FacebookWindow(QMainWindow):
    window_closed = pyqtSignal(str)

    def __init__(self, profile_name: str):
        super().__init__()
        self.profile_name  = profile_name
        self.setWindowTitle(f"Tiến Khoa  ·  {profile_name}")
        self.resize(1400, 860)
        self.setMinimumSize(1000, 600)
        self.setStyleSheet(DARK)
        self._running      = False
        self._progress_val = 0
        self._timer        = QTimer(self)
        self._timer.timeout.connect(self._tick)
        self._driver  = None
        self._worker  = None
        self._post_worker = None
        self._cmt_worker = None
        self._uptop_worker = None
        self._opening = False
        self._cur_tab = "group"  # Track current active tab
        self._total_groups = 0
        self._done_groups  = 0
        self._chrome_hwnd = None  # Store Chrome window handle
        self._chrome_container = None  # Store Chrome container widget
        self._chrome_keep_alive_timer = None  # Timer để maintain embedding

        self._build()
        # Chrome sẽ được khởi động khi tab Browser được chuyển đến

    def closeEvent(self, e):
        if self._timer.isActive():
            self._timer.stop()
        if self._chrome_keep_alive_timer is not None and self._chrome_keep_alive_timer.isActive():
            self._chrome_keep_alive_timer.stop()
        if self._driver is not None:
            ChromiumDriver.close_driver(self._driver)
            self._driver = None
        if self._worker is not None:
            if self._worker.isRunning():
                self._worker.quit()
                self._worker.wait(3000)
            self._worker = None
        if self._post_worker is not None:
            if self._post_worker.isRunning():
                self._post_worker.quit()
                self._post_worker.wait(3000)
            self._post_worker = None
        if self._cmt_worker is not None:
            if self._cmt_worker.isRunning():
                self._cmt_worker.quit()
                self._cmt_worker.wait(3000)
            self._cmt_worker = None
        if self._uptop_worker is not None:
            if self._uptop_worker.isRunning():
                self._uptop_worker.quit()
                self._uptop_worker.wait(3000)
            self._uptop_worker = None
        self._opening = False
        self.window_closed.emit(self.profile_name)
        super().closeEvent(e)

    def _open_chrome(self):
        if self._driver is not None or self._opening:
            return
        self._opening = True
        self._worker  = ChromiumWorker(self.profile_name)
        self._worker.ready.connect(self._on_chrome_ready)
        self._worker.start()

    def _on_chrome_ready(self, driver):
        self._opening = False
        if driver is not None:
            self._driver = driver
            print(f"[SUCCESS] ✅ Chrome đã mở cho {self.profile_name}", flush=True)
            
            # Nếu đang ở tab browser, nhúng Chrome vào
            if self._cur_tab == "browser":
                QTimer.singleShot(1000, self._embed_chrome_to_browser)
        else:
            self._driver = None
            print(f"[ERROR] ❌ Không mở được Chrome cho {self.profile_name}", flush=True)
        if self._worker is not None:
            self._worker.deleteLater()
            self._worker = None

    def _embed_chrome_to_browser(self):
        """Nhúng Chrome window (win32gui approach)"""
        try:
            if self._driver is None:
                print("[ERROR] No driver available", flush=True)
                return
            
            print("[DEBUG] Bắt đầu nhúng Chrome...", flush=True)
            
            # Tìm Chrome window bằng class name
            chrome_hwnd = self._find_chrome_window()
            if not chrome_hwnd:
                print("[ERROR] ❌ Không tìm thấy Chrome window", flush=True)
                return
            
            print(f"[DEBUG] Tìm thấy Chrome HWND: {chrome_hwnd}", flush=True)
            self._chrome_hwnd = chrome_hwnd
            
            if not self._chrome_container:
                return
            
            # Get container HWND
            container_hwnd = int(self._chrome_container.winId())
            print(f"[DEBUG] Container HWND: {container_hwnd}", flush=True)
            
            # Clear layout
            layout = self._chrome_container.layout()
            if layout:
                while layout.count():
                    item = layout.takeAt(0)
                    if item.widget():
                        item.widget().deleteLater()
            
            # Nhúng Chrome
            success = self._embed_window(chrome_hwnd, container_hwnd)
            if success:
                print("[SUCCESS] ✅ Chrome đã nhúng thành công", flush=True)
                self._start_keep_alive()
            else:
                print("[ERROR] ❌ Lỗi nhúng Chrome", flush=True)
                
        except Exception as e:
            print(f"[ERROR] Exception: {e}", flush=True)
            import traceback
            traceback.print_exc()

    def _find_chrome_window(self):
        """Tìm ĐÚNG Chrome window do Selenium mở - dùng PID của driver"""
        try:
            import psutil

            if self._driver is None:
                return None

            # Lấy PID của chromedriver
            chromedriver_pid = self._driver.service.process.pid
            print(f"[DEBUG] Chromedriver PID: {chromedriver_pid}", flush=True)

            # Tìm TẤT CẢ chrome.exe là child của chromedriver này
            chrome_pids = set()
            try:
                cd_proc = psutil.Process(chromedriver_pid)
                for child in cd_proc.children(recursive=True):
                    name = child.name().lower()
                    if 'chrome.exe' in name:
                        chrome_pids.add(child.pid)
                        print(f"[DEBUG] Chrome child PID: {child.pid}", flush=True)
            except (psutil.NoSuchProcess, psutil.AccessDenied) as e:
                print(f"[DEBUG] psutil error: {e}", flush=True)

            if not chrome_pids:
                print(f"[WARN] Không tìm thấy chrome child process từ chromedriver", flush=True)
                return None

            # Enum windows, chỉ lấy window thuộc chrome_pids
            import ctypes
            from ctypes import wintypes

            found_windows = []

            def enum_callback(hwnd, _):
                try:
                    if not win32gui.IsWindowVisible(hwnd):
                        return True
                    class_name = win32gui.GetClassName(hwnd)
                    if class_name not in ("Chrome_WidgetWin_1", "Chrome_WidgetWin_0"):
                        return True

                    # Lấy PID của window này
                    pid_buf = ctypes.c_ulong()
                    ctypes.windll.user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid_buf))
                    win_pid = pid_buf.value

                    # CHỈ lấy window thuộc chrome process do Selenium mở
                    if win_pid not in chrome_pids:
                        return True  # Bỏ qua VS Code, Electron apps khác

                    rect = win32gui.GetWindowRect(hwnd)
                    w = rect[2] - rect[0]
                    h = rect[3] - rect[1]
                    if w > 200 and h > 150:
                        found_windows.append((hwnd, w * h))
                        print(f"[DEBUG] Found Selenium Chrome window: HWND={hwnd} PID={win_pid} size={w}x{h}", flush=True)
                except Exception:
                    pass
                return True

            win32gui.EnumWindows(enum_callback, None)

            if found_windows:
                found_windows.sort(key=lambda x: x[1], reverse=True)
                return found_windows[0][0]

            print(f"[WARN] Không tìm thấy window nào khớp Chrome PID", flush=True)
            return None

        except Exception as e:
            print(f"[ERROR] _find_chrome_window: {e}", flush=True)
            import traceback
            traceback.print_exc()
            return None

    def _embed_window(self, hwnd, parent_hwnd):
        """Nhúng window sử dụng win32gui (LDPlayer approach)"""
        try:
            # Get original style
            original_style = win32gui.GetWindowLong(hwnd, win32con.GWL_STYLE)
            print(f"[DEBUG] Original style: {original_style}", flush=True)
            
            # Remove decorations, add CHILD style
            new_style = original_style
            new_style &= ~(win32con.WS_CAPTION | win32con.WS_THICKFRAME | 
                          win32con.WS_SYSMENU | win32con.WS_MINIMIZEBOX | 
                          win32con.WS_MAXIMIZEBOX)
            new_style |= win32con.WS_CHILD | win32con.WS_VISIBLE
            
            win32gui.SetWindowLong(hwnd, win32con.GWL_STYLE, new_style)
            print(f"[DEBUG] Set style to: {new_style}", flush=True)
            
            # Set parent
            win32gui.SetParent(hwnd, parent_hwnd)
            print(f"[DEBUG] SetParent done", flush=True)
            
            # Get container size
            rect = win32gui.GetClientRect(parent_hwnd)
            width = rect[2] - rect[0]
            height = rect[3] - rect[1]
            
            # Move and resize
            win32gui.MoveWindow(hwnd, 0, 0, width, height, True)
            print(f"[DEBUG] MoveWindow to 0, 0, {width}, {height}", flush=True)
            
            time.sleep(0.1)
            
            # Show
            win32gui.ShowWindow(hwnd, win32con.SW_SHOW)
            win32gui.UpdateWindow(hwnd)
            
            time.sleep(0.1)
            
            # Redraw
            win32gui.InvalidateRect(hwnd, None, True)
            win32gui.RedrawWindow(hwnd, None, None, 
                                 win32con.RDW_FRAME | 
                                 win32con.RDW_INVALIDATE | 
                                 win32con.RDW_UPDATENOW | 
                                 win32con.RDW_ALLCHILDREN | 
                                 win32con.RDW_ERASE)
            
            # Final position
            win32gui.SetWindowPos(hwnd, win32con.HWND_TOP, 
                                 0, 0, width, height,
                                 win32con.SWP_SHOWWINDOW | win32con.SWP_FRAMECHANGED)
            
            time.sleep(0.2)
            
            # Enable input - chỉ dùng SetFocus, KHÔNG dùng SetForegroundWindow (không hoạt động với child)
            win32gui.EnableWindow(hwnd, True)
            win32gui.SetFocus(hwnd)
            
            # Send WM_ACTIVATE để kích hoạt window
            win32gui.PostMessage(hwnd, 0x0006, 1, 0)  # WM_ACTIVATE with WA_ACTIVATE
            
            time.sleep(0.3)
            
            print(f"[SUCCESS] Embedding successful", flush=True)
            return True
            
        except Exception as e:
            print(f"[ERROR] Lỗi embedding: {e}", flush=True)
            import traceback
            traceback.print_exc()
            return False

    def _start_keep_alive(self):
        """Bắt đầu keep alive timer"""
        if self._chrome_keep_alive_timer is None:
            self._chrome_keep_alive_timer = QTimer(self)
            self._chrome_keep_alive_timer.timeout.connect(self._keep_chrome_alive)
        
        if not self._chrome_keep_alive_timer.isActive():
            self._chrome_keep_alive_timer.start(200)
            print("[DEBUG] Keep alive timer started", flush=True)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._sync_chrome_size()

    def moveEvent(self, event):
        super().moveEvent(event)
        self._sync_chrome_size()

    def _sync_chrome_size(self):
        try:
            if self._chrome_hwnd is None or not self._chrome_container:
                return
            if not win32gui.IsWindow(self._chrome_hwnd):
                self._chrome_hwnd = None
                return
            container_hwnd = int(self._chrome_container.winId())
            rect = win32gui.GetClientRect(container_hwnd)
            w, h = rect[2] - rect[0], rect[3] - rect[1]
            if w > 0 and h > 0:
                win32gui.MoveWindow(self._chrome_hwnd, 0, 0, w, h, True)
                win32gui.SetWindowPos(
                    self._chrome_hwnd,
                    win32con.HWND_TOP,
                    0, 0, w, h,
                    win32con.SWP_SHOWWINDOW
                )
        except Exception:
            pass

    def _keep_chrome_alive(self):
        try:
            if self._chrome_hwnd is None or not self._chrome_container:
                return
            if not win32gui.IsWindow(self._chrome_hwnd):
                self._chrome_hwnd = None
                self._chrome_keep_alive_timer.stop()
                return
            container_hwnd = int(self._chrome_container.winId())
            current_parent = win32gui.GetParent(self._chrome_hwnd)
            if current_parent != container_hwnd:
                win32gui.SetParent(self._chrome_hwnd, container_hwnd)
            rect = win32gui.GetClientRect(container_hwnd)
            w, h = rect[2] - rect[0], rect[3] - rect[1]
            if w > 0 and h > 0:
                cr = win32gui.GetWindowRect(self._chrome_hwnd)
                if (cr[2] - cr[0]) != w or (cr[3] - cr[1]) != h:
                    win32gui.MoveWindow(self._chrome_hwnd, 0, 0, w, h, True)
            if not win32gui.IsWindowVisible(self._chrome_hwnd):
                win32gui.ShowWindow(self._chrome_hwnd, win32con.SW_SHOW)
        except Exception:
            pass

    def _build(self):
        central = QWidget()
        self.setCentralWidget(central)
        root = QVBoxLayout(central)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        root.addWidget(self._make_header())
        root.addWidget(self._make_tabbar())

        self._pg_group    = self._build_group()
        self._pg_page     = self._build_page()
        self._pg_settings = self._build_settings()
        self._pg_browser  = self._build_browser()

        for p in [self._pg_group, self._pg_page, self._pg_settings, self._pg_browser]:
            root.addWidget(p)

        sb = QStatusBar()
        sb.setStyleSheet("background:#11111b;border-top:1px solid #313264;"
                         "font-size:12px;color:#6c7086;")
        self.setStatusBar(sb)
        self._sb = sb
        self._switch("group")

    def _make_header(self):
        h = QWidget()
        h.setStyleSheet("background:#11111b;border-bottom:1px solid #313244;")
        h.setFixedHeight(46)
        lay = QHBoxLayout(h)
        lay.setContentsMargins(14, 0, 14, 0)
        lay.setSpacing(10)

        fb_badge = QLabel("  fb  ")
        fb_badge.setFixedHeight(28)
        fb_badge.setAlignment(Qt.AlignCenter)
        fb_badge.setStyleSheet(
            "background:#1877f2;color:white;font-weight:bold;"
            "font-size:13px;border-radius:6px;padding:0 8px;")

        lbl = QLabel(f"Tiến Khoa   ·   {self.profile_name}")
        lbl.setStyleSheet(
            "color:#cdd6f4;font-weight:bold;font-size:14px;background:transparent;")

        def pill(txt, bg):
            b = QPushButton(txt)
            b.setStyleSheet(
                f"QPushButton{{background:{bg};color:white;border:none;"
                f"border-radius:10px;padding:4px 14px;font-size:12px;font-weight:bold;}}"
                f"QPushButton:hover{{opacity:0.85;}}")
            b.setFixedHeight(26)
            return b

        lay.addWidget(fb_badge)
        lay.addWidget(lbl)
        lay.addSpacing(12)
        
        # Nút "Nội dung" - mở ContentViewerDialog
        btn_content = pill("Nội dung", "#40a02b")
        btn_content.clicked.connect(self._open_content_viewer)
        lay.addWidget(btn_content)
        
        # Nút "Cấu hình AI"
        btn_ai_cfg = pill("Cấu hình AI", "#1e66f5")
        btn_ai_cfg.clicked.connect(self._open_ai_config)
        lay.addWidget(btn_ai_cfg)
        
        lay.addStretch()
        return h

    def _make_tabbar(self):
        bar = QWidget()
        bar.setStyleSheet("background:#181825;border-bottom:1px solid #313244;")
        bar.setFixedHeight(44)
        lay = QHBoxLayout(bar)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(0)
        self._tb = {}
        for key, txt in [("group",    "  ĐĂNG NHÓM  "),
                          ("page",     "  ĐĂNG PAGE  "),
                          ("settings", "  CÁCH CANH  "),
                          ("browser",  "  🌐 TRÌNH DUYỆT  ")]:
            b = QPushButton(txt)
            b.setFixedHeight(44)
            b.setMinimumWidth(148)
            b.clicked.connect(lambda _, k=key: self._switch(k))
            self._tb[key] = b
            lay.addWidget(b)
        lay.addStretch()
        return bar

    def _switch(self, tab):
        self._cur_tab = tab
        self._pg_group.setVisible(tab == "group")
        self._pg_page.setVisible(tab == "page")
        self._pg_settings.setVisible(tab == "settings")
        self._pg_browser.setVisible(tab == "browser")
        
        # Handle Chrome lifecycle
        if tab == "browser":
            if self._driver is None and not self._opening:
                self._open_chrome()
            elif self._driver is not None and self._chrome_hwnd is None:
                QTimer.singleShot(500, self._embed_chrome_to_browser)
            elif self._chrome_hwnd is not None and (self._chrome_keep_alive_timer is None or not self._chrome_keep_alive_timer.isActive()):
                self._start_keep_alive()
        else:
            # Stop keep alive timer when leaving browser tab
            if self._chrome_keep_alive_timer is not None and self._chrome_keep_alive_timer.isActive():
                self._chrome_keep_alive_timer.stop()

        ACT = ("QPushButton{background:#1e1e2e;color:#89b4fa;border:none;"
               "border-bottom:2px solid #89b4fa;font-weight:bold;font-size:13px;"
               "padding:0 20px;min-width:148px;height:44px;}")
        OFF = ("QPushButton{background:#181825;color:#6c7086;border:none;"
               "border-bottom:2px solid transparent;font-weight:bold;font-size:13px;"
               "padding:0 20px;min-width:148px;height:44px;}"
               "QPushButton:hover{background:#1e1e2e;color:#a6adc8;}")
        for k, b in self._tb.items():
            b.setStyleSheet(ACT if k == tab else OFF)

    # ══════════════════════════════════════════════════════════════════════════
    # TAB: ĐĂNG NHÓM
    # ══════════════════════════════════════════════════════════════════════════
    def _build_group(self):
        w = QWidget()
        lay = QHBoxLayout(w)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(0)
        lay.addWidget(self._make_group_left())
        lay.addWidget(self._make_group_center(), 1)
        lay.addWidget(self._make_group_right())
        return w

    def _make_group_left(self):
        p = QWidget()
        p.setStyleSheet("background:#181825;border-right:1px solid #313244;")
        p.setFixedWidth(316)
        lay = QVBoxLayout(p)
        lay.setContentsMargins(8, 8, 8, 8)
        lay.setSpacing(6)

        fr = QHBoxLayout()
        fi = QLineEdit()
        fi.setPlaceholderText("🔍  Tìm nhóm...")
        fi.setFixedHeight(28)
        fi.setStyleSheet(
            "QLineEdit{background:#313244;border:1px solid #45475a;"
            "border-radius:4px;padding:2px 10px;font-size:12px;color:#cdd6f4;}"
            "QLineEdit:focus{border-color:#89b4fa;}")
        fb_btn = QPushButton("⬇  Lọc")
        fb_btn.setFixedSize(80, 28)
        fb_btn.setStyleSheet(BTN_GRAY)
        fb_btn.clicked.connect(self._open_filter_menu)
        fb_btn.setVisible(False)  # ẨN BUTTON LỌC
        fr.addWidget(fi, 1)
        fr.addWidget(fb_btn)
        lay.addLayout(fr)

        self._gt = QTableWidget()
        self._gt.setColumnCount(6)
        self._gt.setHorizontalHeaderLabels(["✓", "#", "ID Nhóm", "Tên Nhóm", "Số lần", "Ngày chạy"])
        self._gt.horizontalHeader().setStretchLastSection(False)
        self._gt.setColumnWidth(0, 30)
        self._gt.setColumnWidth(1, 32)
        self._gt.setColumnWidth(2, 90)
        self._gt.setColumnWidth(4, 60)
        self._gt.setColumnWidth(5, 95)
        self._gt.horizontalHeader().setSectionResizeMode(3, QHeaderView.Stretch)
        self._gt.setMinimumHeight(350)
        self._gt.setSelectionBehavior(QAbstractItemView.SelectRows)
        self._gt.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self._gt.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self._gt.setAlternatingRowColors(True)
        self._gt.verticalHeader().setVisible(False)
        self._gt.setShowGrid(False)
        self._gt.setContextMenuPolicy(Qt.CustomContextMenu)
        self._gt.customContextMenuRequested.connect(self._group_menu)
        self._gt.setStyleSheet(
            "QTableWidget{border:1px solid #45475a;border-radius:4px;font-size:12px;"
            "background:#181825;alternate-background-color:#1e1e2e;}"
            "QTableWidget::item{padding:5px 6px;border:none;}"
            "QTableWidget::item:selected{background:#45475a;color:#89b4fa;}"
            "QHeaderView::section{background:#313244;font-size:11px;color:#89b4fa;"
            "border:none;border-bottom:1px solid #45475a;padding:5px 6px;}")
        self._load_groups()
        lay.addWidget(self._gt, 1)

        br = QHBoxLayout()
        br.setSpacing(6)
        b1 = QPushButton("⬇  LẤY DS NHÓM")
        b1.setFixedHeight(34)
        b1.setStyleSheet(BTN_GREEN(12, 6))
        b1.clicked.connect(self._scan_groups)
        b2 = QPushButton("📂  LOAD DATA")
        b2.setFixedHeight(34)
        b2.setStyleSheet(BTN_GRAY)
        br.addWidget(b1)
        br.addWidget(b2)
        lay.addLayout(br)
        return p

    def _scan_groups(self):
        if self._driver is None:
            self._log_msg('<span style="color:#f38ba8;font-size:11px;">'
                          '[WARN] Chrome chưa mở hoặc chưa sẵn sàng.</span>')
            return
        if hasattr(self, '_scan_worker') and self._scan_worker is not None:
            if self._scan_worker.isRunning():
                self._log_msg('<span style="color:#fab387;font-size:11px;">'
                              '[WARN] Đang quét, vui lòng chờ...</span>')
                return

        self._log_msg('<span style="color:#89b4fa;font-size:11px;">'
                      '[INFO] Đang lấy danh sách nhóm...</span>')

        self._scan_worker = GroupScannerWorker(self._driver, self.profile_name)
        self._scan_worker.result.connect(self._on_scan_groups_done)
        self._scan_worker.finished.connect(self._on_scan_worker_finished)
        self._scan_worker.start()

    def _on_scan_groups_done(self, res: dict):
        ts = datetime.now().strftime("%H:%M:%S")
        if not res.get('success'):
            msg = res.get('message', 'Lỗi không xác định')
            self._log_msg(f'<span style="color:#f38ba8;font-size:11px;">'
                          f'[{ts}] ✖ {msg}</span>')
            return

        groups = res.get('groups', [])
        self._log_msg(f'<span style="color:#a6e3a1;font-size:11px;">'
                      f'[{ts}] ✔ {res.get("message", "")} ({len(groups)} nhóm)</span>')

        profile_file = os.path.join('data', 'profile.json')
        try:
            os.makedirs('data', exist_ok=True)
            profiles = []
            if os.path.isfile(profile_file):
                with open(profile_file, 'r', encoding='utf-8') as f:
                    profiles = json.load(f)
            found = False
            for p in profiles:
                if p.get('profile') == self.profile_name:
                    p['groups'] = groups
                    found = True
                    break
            if not found:
                profiles.append({'profile': self.profile_name, 'groups': groups})
            with open(profile_file, 'w', encoding='utf-8') as f:
                json.dump(profiles, f, ensure_ascii=False, indent=4)
            print(f"[SUCCESS] Lưu {len(groups)} groups cho {self.profile_name}", flush=True)
        except Exception as e:
            print(f"[ERROR] Lỗi lưu groups: {e}", flush=True)

        self._gt.setRowCount(0)
        for i, g in enumerate(groups):
            self._gt.insertRow(i)
            chk = QCheckBox()
            chk.setStyleSheet("QCheckBox { margin-left: 8px; }")
            self._gt.setCellWidget(i, 0, chk)
            si = QTableWidgetItem(str(i + 1))
            si.setTextAlignment(Qt.AlignCenter)
            self._gt.setItem(i, 1, si)
            self._gt.setItem(i, 2, QTableWidgetItem(g.get('url', '')))
            self._gt.setItem(i, 3, QTableWidgetItem(g.get('name', '')))
            self._gt.setRowHeight(i, 28)

    def _on_scan_worker_finished(self):
        if hasattr(self, '_scan_worker') and self._scan_worker is not None:
            self._scan_worker.deleteLater()
            self._scan_worker = None

    # ── Log helpers ───────────────────────────────────────────────────────────
    def _log_msg(self, html: str):
        """Ghi log HTML vào nhật ký."""
        self._log.append(html)

    def _on_post_log(self, msg: str):
        """Callback nhận log từ PostGroupsWorker."""
        ts = datetime.now().strftime("%H:%M:%S")
        if '✔' in msg or '✅' in msg or 'SUCCESS' in msg:
            color = '#a6e3a1'
        elif '❌' in msg or '✖' in msg or 'ERROR' in msg:
            color = '#f38ba8'
        elif '⏳' in msg or '⏱' in msg or 'Chờ' in msg or 'chờ' in msg:
            color = '#f9e2af'
        else:
            color = '#cdd6f4'
        self._log.append(
            f'<span style="color:{color};font-size:11px;">[{ts}] {msg}</span>')

    def _on_post_success(self, ts: str, group_name: str, post_url: str):
        """Thêm vào bảng kết quả thành công."""
        try:
            r = self._suc.rowCount()
            self._suc.insertRow(r)
            items = [ts, group_name, post_url, "Đăng bài"]
            for j, v in enumerate(items):
                item = QTableWidgetItem(v)
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                self._suc.setItem(r, j, item)
            self._suc.scrollToBottom()
            
            # Cập nhật thống kê nhóm
            # Tìm group_url từ group_name
            for i in range(self._gt.rowCount()):
                if self._gt.item(i, 3) and self._gt.item(i, 3).text() == group_name:
                    group_url = self._gt.item(i, 2).text() if self._gt.item(i, 2) else ''
                    if group_url:
                        self._update_group_stats(group_url, success=True)
                    break
        except Exception as e:
            print(f"[ERROR] _on_post_success: {e}", flush=True)

    def _on_post_fail(self, ts: str, group_name: str, error: str):
        """Thêm vào bảng kết quả lỗi."""
        try:
            r = self._err.rowCount()
            self._err.insertRow(r)
            items = [ts, group_name, error]
            for j, v in enumerate(items):
                item = QTableWidgetItem(v)
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                self._err.setItem(r, j, item)
            self._err.scrollToBottom()
        except Exception as e:
            print(f"[ERROR] _on_post_fail: {e}", flush=True)

    # ── Comment handlers ───────────────────────────────────────────────────────
    def _on_cmt_log(self, msg: str):
        """Callback nhận log từ CommentGroupsWorker."""
        ts = datetime.now().strftime("%H:%M:%S")
        if '✔' in msg or '✅' in msg or 'SUCCESS' in msg:
            color = '#a6e3a1'
        elif '❌' in msg or '✖' in msg or 'ERROR' in msg:
            color = '#f38ba8'
        elif '⏳' in msg or '⏱' in msg or 'Chờ' in msg or 'chờ' in msg:
            color = '#f9e2af'
        else:
            color = '#cdd6f4'
        self._log.append(
            f'<span style="color:{color};font-size:11px;">[{ts}] {msg}</span>')

    def _on_cmt_success(self, ts: str, post_url: str, group_name: str):
        """Thêm vào bảng kết quả thành công comment."""
        try:
            r = self._suc.rowCount()
            self._suc.insertRow(r)
            items = [str(ts), str(group_name), str(post_url), "Comment"]
            for j, v in enumerate(items):
                item = QTableWidgetItem(v)
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                self._suc.setItem(r, j, item)
            self._suc.scrollToBottom()
            self._done_groups += 1
            self._update_progress()
            self._log_msg(f'<span style="color:#a6e3a1;font-size:11px;">[{ts}] ✅ Bình luận thành công: {group_name}</span>')
            
            # Cập nhật thống kê nhóm
            # Tìm group_url từ group_name
            for i in range(self._gt.rowCount()):
                if self._gt.item(i, 3) and self._gt.item(i, 3).text() == group_name:
                    group_url = self._gt.item(i, 2).text() if self._gt.item(i, 2) else ''
                    if group_url:
                        self._update_group_stats(group_url, success=True)
                    break
        except Exception as e:
            print(f"[ERROR] _on_cmt_success: {e}", flush=True)

    def _on_cmt_fail(self, ts: str, post_url: str, error: str):
        """Thêm vào bảng kết quả lỗi comment."""
        try:
            r = self._err.rowCount()
            self._err.insertRow(r)
            items = [str(ts), str(post_url), str(error)]
            for j, v in enumerate(items):
                item = QTableWidgetItem(v)
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                self._err.setItem(r, j, item)
            self._err.scrollToBottom()
            self._done_groups += 1
            self._update_progress()
            self._log_msg(f'<span style="color:#ff7a7a;font-size:11px;">[{ts}] ❌ Lỗi: {error}</span>')
        except Exception as e:
            print(f"[ERROR] _on_cmt_fail: {e}", flush=True)

    def _on_cmt_finished(self):
        self._running = False
        self._timer.stop()
        self._pbar.setValue(100)
        self._set_btn_enabled(True)
        self._st_lbl.setText("✔ Hoàn thành")
        if hasattr(self, '_cmt_worker') and self._cmt_worker is not None:
            self._cmt_worker.deleteLater()
            self._cmt_worker = None

    # ── UpTop handlers ──────────────────────────────────────────────
    def _on_uptop_log(self, msg: str):
        """Callback nhận log từ UpTopWorker."""
        ts = datetime.now().strftime("%H:%M:%S")
        if '✔' in msg or '✅' in msg or 'SUCCESS' in msg:
            color = '#a6e3a1'
        elif '❌' in msg or '✖' in msg or 'ERROR' in msg:
            color = '#f38ba8'
        elif '⏳' in msg or '⏱' in msg or 'Chờ' in msg or 'chờ' in msg:
            color = '#f9e2af'
        else:
            color = '#cdd6f4'
        self._log.append(
            f'<span style="color:{color};font-size:11px;">[{ts}] {msg}</span>')

    def _on_uptop_success(self, ts: str, post_url: str, action_name: str):
        """Thêm vào bảng kết quả thành công uptop."""
        try:
            r = self._suc.rowCount()
            self._suc.insertRow(r)
            # Cột: Time, Nhóm (lấy từ URL), Link, Loại
            url_short = post_url.replace('https://www.facebook.com/groups/', '')[:50]
            items = [str(ts), url_short, str(post_url), "UpTop"]
            for j, v in enumerate(items):
                item = QTableWidgetItem(v)
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                self._suc.setItem(r, j, item)
            self._suc.scrollToBottom()
            self._done_groups += 1
            self._update_progress()
            self._log_msg(f'<span style="color:#a6e3a1;font-size:11px;">[{ts}] ✅ Up top thành công: {action_name}</span>')
            
            # Cập nhật thống kê nhóm - extract group ID từ post_url
            # Format: https://www.facebook.com/groups/{group_id}/posts/{post_id}
            if 'groups/' in post_url:
                parts = post_url.split('groups/')
                if len(parts) > 1:
                    group_id = parts[1].split('/')[0]
                    # Tìm group URL từ group_id hoặc sử dụng group_id trực tiếp
                    for i in range(self._gt.rowCount()):
                        if self._gt.item(i, 2):
                            item_url = self._gt.item(i, 2).text()
                            if group_id in item_url:
                                self._update_group_stats(item_url, success=True)
                                break
        except Exception as e:
            print(f"[ERROR] _on_uptop_success: {e}", flush=True)

    def _on_uptop_fail(self, ts: str, post_url: str, error: str):
        """Thêm vào bảng kết quả lỗi uptop."""
        try:
            r = self._err.rowCount()
            self._err.insertRow(r)
            items = [str(ts), str(post_url), str(error)]
            for j, v in enumerate(items):
                item = QTableWidgetItem(v)
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                self._err.setItem(r, j, item)
            self._err.scrollToBottom()
            self._done_groups += 1
            self._update_progress()
            self._log_msg(f'<span style="color:#ff7a7a;font-size:11px;">[{ts}] ❌ Lỗi: {error}</span>')
        except Exception as e:
            print(f"[ERROR] _on_uptop_fail: {e}", flush=True)

    def _on_uptop_finished(self):
        self._running = False
        self._timer.stop()
        self._pbar.setValue(100)
        self._set_btn_enabled(True)
        self._st_lbl.setText("✔ Hoàn thành")
        if hasattr(self, '_uptop_worker') and self._uptop_worker is not None:
            self._uptop_worker.deleteLater()
            self._uptop_worker = None

    # ──────────────────────────────────────────────────────────────
    # Hàm mở Dialog Cấu hình AI
    # ──────────────────────────────────────────────────────────────
    def _open_ai_config(self):
        """Mở dialog cấu hình AI cho profile hiện tại"""
        dialog = AIConfigDialog(self.profile_name, self)
        dialog.exec_()

    # ──────────────────────────────────────────────────────────────
    # Xem trước AI làm lại nội dung
    # ──────────────────────────────────────────────────────────────
    def _preview_ai_content(self, mode: str):
        """Preview AI sẽ làm lại nội dung như thế nào"""
        content = self._content.toPlainText().strip()
        if not content:
            QMessageBox.warning(self, "⚠️ Cảnh báo", "Chưa nhập nội dung để preview!")
            return
        
        # Load AI config
        ai_config = self._get_ai_config()
        if not ai_config or not ai_config.get('groq_key') or not ai_config.get('ai_prompt'):
            QMessageBox.warning(self, "⚠️ Cảnh báo", "Chưa cấu hình AI!\n\nHãy click 'Cấu hình AI' trước.")
            return
        
        # Gọi AI
        try:
            self._log_msg(f'<span style="color:#89b4fa;font-size:11px;">[INFO] 🤖 Đang gọi AI để xem trước...</span>')
            from AI.chatAI import generate_ai_content
            ai_result = generate_ai_content(content, ai_config)
            
            # Hiển thị dialog preview
            preview_dialog = QDialog(self)
            preview_dialog.setWindowTitle("👁 XEM TRƯỚC AI XỬ LÝ NỘI DUNG")
            preview_dialog.setFixedSize(600, 400)
            preview_dialog.setStyleSheet(DARK)
            
            layout = QVBoxLayout(preview_dialog)
            layout.setSpacing(10)
            layout.setContentsMargins(15, 15, 15, 15)
            
            # Tiêu đề
            lbl_title = QLabel("📝  So Sánh Nội Dung")
            lbl_title.setFont(QFont("Segoe UI", 12, QFont.Bold))
            lbl_title.setStyleSheet("color:#89b4fa;background:transparent;")
            layout.addWidget(lbl_title)
            
            # Splitter để hiển thị 2 bên
            splitter = QWidget()
            splitter_lay = QHBoxLayout(splitter)
            splitter_lay.setSpacing(10)
            splitter_lay.setContentsMargins(0, 0, 0, 0)
            
            # Bên trái: Nội dung gốc
            left_lay = QVBoxLayout()
            lbl_left = QLabel("📌 Nội Dung Gốc")
            lbl_left.setStyleSheet("color:#a6e3a1;font-weight:bold;font-size:11px;background:transparent;")
            left_lay.addWidget(lbl_left)
            text_left = QTextEdit()
            text_left.setPlainText(content)
            text_left.setReadOnly(True)
            text_left.setStyleSheet(
                "QTextEdit{background:#181825;border:1px solid #45475a;border-radius:4px;"
                "font-size:12px;color:#a6adc8;padding:8px;}")
            left_lay.addWidget(text_left)
            
            # Bên phải: Nội dung AI làm
            right_lay = QVBoxLayout()
            lbl_right = QLabel("🤖 AI Làm Lại")
            lbl_right.setStyleSheet("color:#89b4fa;font-weight:bold;font-size:11px;background:transparent;")
            right_lay.addWidget(lbl_right)
            text_right = QTextEdit()
            text_right.setPlainText(ai_result)
            text_right.setReadOnly(True)
            text_right.setStyleSheet(
                "QTextEdit{background:#181825;border:1px solid #45475a;border-radius:4px;"
                "font-size:12px;color:#89b4fa;padding:8px;}")
            right_lay.addWidget(text_right)
            
            splitter_lay.addLayout(left_lay, 1)
            splitter_lay.addLayout(right_lay, 1)
            layout.addWidget(splitter)
            
            # Nút hành động
            btn_lay = QHBoxLayout()
            
            btn_copy = QPushButton("📋 Copy AI Result")
            btn_copy.setFixedHeight(32)
            btn_copy.setStyleSheet(BTN_BLUE(12, 8))
            btn_copy.clicked.connect(lambda: self._copy_to_clipboard(ai_result))
            
            btn_accept = QPushButton("✅ Dùng Nội Dung AI")
            btn_accept.setFixedHeight(32)
            btn_accept.setStyleSheet(BTN_BLUE(12, 8))
            btn_accept.clicked.connect(lambda: self._use_ai_result(ai_result, preview_dialog))
            
            btn_close = QPushButton("✕ Đóng")
            btn_close.setFixedHeight(32)
            btn_close.setStyleSheet(BTN_GRAY)
            btn_close.clicked.connect(preview_dialog.reject)
            
            btn_lay.addWidget(btn_copy)
            btn_lay.addWidget(btn_accept)
            btn_lay.addStretch()
            btn_lay.addWidget(btn_close)
            layout.addLayout(btn_lay)
            
            preview_dialog.exec_()
            self._log_msg(f'<span style="color:#a6e3a1;font-size:11px;">[OK] Preview hoàn thành</span>')
            
        except Exception as e:
            self._log_msg(f'<span style="color:#f38ba8;font-size:11px;">[ERROR] Lỗi preview: {str(e)[:60]}</span>')
            QMessageBox.critical(self, "❌ Lỗi", f"Lỗi khi gọi AI:\n\n{str(e)}")
    
    def _copy_to_clipboard(self, text: str):
        """Copy nội dung vào clipboard"""
        import subprocess
        try:
            process = subprocess.Popen(['clip'], stdin=subprocess.PIPE)
            process.communicate(text.encode('utf-8'))
            QMessageBox.information(self, "✅ Thành công", "Đã copy vào clipboard!")
        except Exception as e:
            QMessageBox.critical(self, "❌ Lỗi", f"Copy lỗi: {e}")
    
    def _use_ai_result(self, ai_result: str, dialog):
        """Dùng nội dung AI, replace vào ô nội dung"""
        self._content.setPlainText(ai_result)
        dialog.accept()
        self._log_msg(f'<span style="color:#a6e3a1;font-size:11px;">[OK] ✅ Đã cập nhật nội dung từ AI</span>')

    # ──────────────────────────────────────────────────────────────
    # Hàm mở Dialog Quản lý Nội dung
    # ──────────────────────────────────────────────────────────────
    def _open_content_viewer(self):
        """Mở dialog quản lý nội dung - thêm, xem, copy"""
        dialog = ContentManagerDialog(self.profile_name, self)
        dialog.exec_()

    def _get_ai_config(self) -> dict:
        """Load AI config từ file JSON"""
        try:
            base = os.path.dirname(os.path.abspath(__file__))
            data_dir = os.path.join(base, "data")
            config_file = os.path.join(data_dir, f"ai_config_{self.profile_name}.json")
            
            print(f"[DEBUG] Loading AI config from: {config_file}")
            print(f"[DEBUG] File exists: {os.path.isfile(config_file)}")
            
            if os.path.isfile(config_file):
                with open(config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    print(f"[DEBUG] AI Config loaded: api_key={'***' if config.get('api_key') else 'NOT SET'}, prompt_len={len(config.get('prompt', ''))}, model={config.get('model')}")
                    return config
            else:
                print(f"[WARN] AI config file not found: {config_file}")
        except Exception as e:
            print(f"[ERROR] Load AI config failed: {e}")
        
        print(f"[WARN] Returning empty AI config")
        return {}

    def _spin_content_simple(self, text: str) -> str:
        """
        Spin content đơn giản - chọn ngẫu nhiên từ các đoạn cách nhau bằng |  và {} 
        Ví dụ: 'A | B | C' → chọn 1 trong 3
                'Bán {nhà|đất|app}' → chọn 1 trong 3
        """
        if not text or len(text.strip()) == 0:
            return text
        
        import re
        
        # Bước 1: Chọn segment nếu có |
        segments = text.split(' | ')
        if len(segments) > 1:
            chosen = random.choice(segments).strip()
            self._log_msg(f'<span style="color:#fab387;font-size:11px;">'
                         f'[SPIN] Chọn đoạn 1/{len(segments)}</span>')
        else:
            chosen = text.strip()
        
        # Bước 2: Spin {var1|var2|var3}
        def replacer(m):
            choices = m.group(1).split('|')
            return random.choice(choices).strip()
        
        result = re.sub(r'\{([^}]+)\}', replacer, chosen)
        return result

    def _process_content_with_ai(self, content: str, use_ai_checkbox=None) -> str:
        """
        Xử lý nội dung với AI nếu checkbox được tick + SPIN nội dung
        
        Args:
            content: Nội dung cần xử lý
            use_ai_checkbox: QCheckBox object (nếu None, dùng self._chk_ai)
        
        Returns: Nội dung được xử lý + spin hoặc nội dung gốc nếu lỗi
        """
        # Xác định checkbox
        chk = use_ai_checkbox if use_ai_checkbox else self._chk_ai
        
        # Kiểm tra checkbox
        if not chk.isChecked():
            # Không dùng AI, nhưng vẫn SPIN content
            return self._spin_content_simple(content)
        
        # Load AI config
        ai_config = self._get_ai_config()
        if not ai_config or not ai_config.get('groq_key'):
            self._log_msg(f'<span style="color:#fab387;font-size:11px;">'
                         f'[WARN] AI chưa cấu hình, dùng nội dung gốc + spin</span>')
            return self._spin_content_simple(content)
        
        # Gọi AI để xử lý nội dung
        try:
            self._log_msg(f'<span style="color:#89b4fa;font-size:11px;">'
                         f'[INFO] 🤖 Đang gọi AI để xử lý nội dung...</span>')
            
            processed = generate_ai_content(content, ai_config)
            
            if processed and processed != content:
                self._log_msg(f'<span style="color:#a6e3a1;font-size:11px;">'
                             f'[OK] AI xử lý xong</span>')
            else:
                processed = content
            
            # SPIN nội dung sau khi xử lý AI
            final = self._spin_content_simple(processed)
            return final
            
        except Exception as e:
            self._log_msg(f'<span style="color:#f38ba8;font-size:11px;">'
                         f'[ERROR] AI failed: {str(e)[:60]}</span>')
            return self._spin_content_simple(content)

    def _load_groups(self):
        groups = []
        profile_file = os.path.join('data', 'profile.json')
        if os.path.isfile(profile_file):
            try:
                with open(profile_file, 'r', encoding='utf-8') as f:
                    profiles = json.load(f)
                for p in profiles:
                    if p.get('profile') == self.profile_name:
                        groups = p.get('groups', [])
                        break
            except Exception as e:
                print(f"[ERROR] Lỗi load groups: {e}", flush=True)

        # Load thống kê nhóm
        stats = self._load_group_stats()

        self._gt.setRowCount(len(groups))
        for i, g in enumerate(groups):
            chk = QCheckBox()
            chk.setStyleSheet("QCheckBox { margin-left: 8px; }")
            self._gt.setCellWidget(i, 0, chk)
            si = QTableWidgetItem(str(i + 1))
            si.setTextAlignment(Qt.AlignCenter)
            self._gt.setItem(i, 1, si)
            if isinstance(g, dict):
                gurl = g.get('url', '')
                gnm  = g.get('name', '')
            else:
                gurl = g[0] if len(g) > 0 else ''
                gnm  = g[1] if len(g) > 1 else ''
            self._gt.setItem(i, 2, QTableWidgetItem(gurl))
            self._gt.setItem(i, 3, QTableWidgetItem(gnm))
            
            # Cột số lần chạy
            run_count = stats.get(gurl, {}).get('run_count', 0)
            self._gt.setItem(i, 4, QTableWidgetItem(str(run_count)))
            
            # Cột lần chạy gần nhất
            last_run = stats.get(gurl, {}).get('last_run', '-')
            self._gt.setItem(i, 5, QTableWidgetItem(str(last_run)))
            
            self._gt.setRowHeight(i, 28)

    def _get_group_stats_file(self) -> str:
        """Đường dẫn file lưu thống kê nhóm"""
        base = os.path.dirname(os.path.abspath(__file__))
        data = os.path.join(base, "data")
        os.makedirs(data, exist_ok=True)
        return os.path.join(data, f"group_stats_{self.profile_name}.json")

    def _load_group_stats(self) -> dict:
        """Load thống kê nhóm từ file JSON"""
        stats_file = self._get_group_stats_file()
        if os.path.isfile(stats_file):
            try:
                with open(stats_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"[STATS] Load lỗi: {e}")
        return {}

    def _save_group_stats(self, stats: dict):
        """Lưu thống kê nhóm vào file JSON"""
        stats_file = self._get_group_stats_file()
        try:
            with open(stats_file, 'w', encoding='utf-8') as f:
                json.dump(stats, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"[STATS] Save lỗi: {e}")

    def _update_group_stats(self, group_url: str, success: bool = True):
        """Cập nhật thống kê khi chạy xong 1 nhóm"""
        stats = self._load_group_stats()
        if group_url not in stats:
            stats[group_url] = {'run_count': 0, 'last_run': '-'}
        
        if success:
            stats[group_url]['run_count'] = stats[group_url].get('run_count', 0) + 1
            stats[group_url]['last_run'] = datetime.now().strftime("%d/%m/%Y")
        
        self._save_group_stats(stats)
        self._load_groups()  # Reload để update UI

    def _open_filter_menu(self):
        """Mở dialog lọc nhóm"""
        dialog = GroupFilterDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            filters = dialog.get_filters()
            if filters:
                self._apply_group_filters(filters)

    def _apply_group_filters(self, filters: list):
        """Lọc nhóm theo tiêu chí đã chọn"""
        if not filters:
            return
        
        stats = self._load_group_stats()
        
        # Thu thập dữ liệu tất cả nhóm
        all_data = []
        for i in range(self._gt.rowCount()):
            run_count = int(self._gt.item(i, 4).text()) if self._gt.item(i, 4) else 0
            all_data.append({
                'row': i,
                'url': self._gt.item(i, 2).text() if self._gt.item(i, 2) else '',
                'run_count': run_count,
                'last_run': self._gt.item(i, 5).text() if self._gt.item(i, 5) else '-',
                'has_run': run_count > 0
            })
        
        # Tính toán thống kê
        run_counts = [d['run_count'] for d in all_data if d['has_run']]
        median = sorted(run_counts)[len(run_counts)//2] if run_counts else 0
        max_count = max(run_counts) if run_counts else 0
        min_count = min(run_counts) if run_counts else 0
        
        rows_to_check = set()
        
        for filter_code in filters:
            if filter_code == "recent":
                # Lấy nhóm đã chạy gần nhất (có last_run)
                recent_rows = [d['row'] for d in all_data if d['last_run'] != '-']
                if recent_rows:
                    # Lấy 50% nhóm được chạy gần nhất (run_count cao)
                    threshold = median if median > 0 else 1
                    rows_to_check.update([d['row'] for d in all_data if d['run_count'] >= threshold])
            
            elif filter_code == "oldest":
                # Lấy nhóm chạy từ lâu nhất (run_count thấp nhưng > 0)
                if run_counts:
                    threshold = median if median > 0 else 1
                    rows_to_check.update([d['row'] for d in all_data if 0 < d['run_count'] < threshold])
            
            elif filter_code == "least":
                # Lấy nhóm chạy ít nhất (run_count = 1 hoặc gần nhất)
                if run_counts:
                    rows_to_check.update([d['row'] for d in all_data if d['run_count'] == min_count])
            
            elif filter_code == "most":
                # Lấy nhóm chạy nhiều nhất (run_count cao)
                if run_counts:
                    threshold = max(min_count, max_count - 3) if max_count > 0 else 0
                    rows_to_check.update([d['row'] for d in all_data if d['run_count'] >= threshold])
            
            elif filter_code == "never":
                # Lấy nhóm chưa chạy lần nào
                rows_to_check.update([d['row'] for d in all_data if d['run_count'] == 0])
        
        # Áp dụng check vào bảng
        for i in range(self._gt.rowCount()):
            chk = self._gt.cellWidget(i, 0)
            if isinstance(chk, QCheckBox):
                chk.setChecked(i in rows_to_check)

    def _group_menu(self, pos):
        m = QMenu(self)
        a1 = QAction("✓ Chọn tất cả", self)
        a1.triggered.connect(self._check_all_groups)
        m.addAction(a1)
        a2 = QAction("✗ Bỏ chọn tất cả", self)
        a2.triggered.connect(self._uncheck_all_groups)
        m.addAction(a2)
        m.addSeparator()
        a3 = QAction("⚫ Chọn những nhóm bôi đen", self)
        a3.triggered.connect(self._check_colored_groups)
        m.addAction(a3)
        m.exec_(self._gt.viewport().mapToGlobal(pos))

    def _check_all_groups(self):
        for i in range(self._gt.rowCount()):
            chk = self._gt.cellWidget(i, 0)
            if isinstance(chk, QCheckBox):
                chk.setChecked(True)

    def _uncheck_all_groups(self):
        for i in range(self._gt.rowCount()):
            chk = self._gt.cellWidget(i, 0)
            if isinstance(chk, QCheckBox):
                chk.setChecked(False)

    def _check_colored_groups(self):
        for i in range(self._gt.rowCount()):
            item = self._gt.item(i, 1)
            if item and item.isSelected():
                chk = self._gt.cellWidget(i, 0)
                if isinstance(chk, QCheckBox):
                    chk.setChecked(True)

    def _make_group_center(self):
        p = QWidget()
        lay = QVBoxLayout(p)
        lay.setContentsMargins(10, 10, 10, 8)
        lay.setSpacing(8)

        self._gb_nd = QGroupBox("📝  Nội dung bài viết")
        gbl = QVBoxLayout(self._gb_nd)
        gbl.setContentsMargins(10, 8, 10, 10)

        # ── Hướng dẫn spin content ────────────────────────────────
        spin_hint = QLabel(
            "💡 Spin bằng dấu  |  (pipe)  ·  Mỗi đoạn cách nhau bằng  |  sẽ random 1 đoạn\n"
            "Ví dụ:  Nội dung 1 | Nội dung 2 | Nội dung 3   →  tự động chọn ngẫu nhiên 1 đoạn")
        spin_hint.setStyleSheet(
            "color:#6c7086;font-size:11px;font-style:italic;background:transparent;")
        spin_hint.setWordWrap(True)
        gbl.addWidget(spin_hint)

        self._content = QTextEdit()
        self._content.setPlaceholderText(
            "Nhập nội dung vào đây...\n\n"
            "Spin bằng | :  Nội dung A | Nội dung B | Nội dung C\n"
            "Hoặc spin từng từ bằng {}: Bán nhà {quận 1|q1|Q.1}, giá {tốt|hợp lý}")
        self._content.setMinimumHeight(140)
        self._content.setStyleSheet(
            "QTextEdit{background:#181825;border:1px solid #45475a;border-radius:6px;"
            "font-size:13px;color:#cdd6f4;padding:8px;}"
            "QTextEdit:focus{border-color:#89b4fa;}")
        gbl.addWidget(self._content)
        lay.addWidget(self._gb_nd)

        gb_av = QGroupBox("🖼  Danh sách ảnh / Video")
        gb_av.setFixedHeight(112)
        avl = QHBoxLayout(gb_av)
        avl.setContentsMargins(10, 6, 10, 10)
        self._media = QListWidget()
        self._media.setStyleSheet(
            "QListWidget{background:#181825;border:1px solid #45475a;border-radius:4px;"
            "font-size:12px;color:#cdd6f4;}"
            "QListWidget::item:selected{background:#45475a;color:#89b4fa;}")
        avr = QVBoxLayout()
        avr.setSpacing(4)
        for txt in ["+ Thêm", "✕ Xóa", "⊘ Clear"]:
            b = QPushButton(txt)
            b.setFixedSize(90, 26)
            b.setStyleSheet(BTN_GRAY)
            if "Thêm" in txt:
                b.clicked.connect(self._add_media)
            elif "Xóa" in txt:
                b.clicked.connect(self._rm_media)
            elif "Clear" in txt:
                b.clicked.connect(self._media.clear)
            avr.addWidget(b)
        avr.addStretch()
        avl.addWidget(self._media, 1)
        avl.addLayout(avr)
        lay.addWidget(gb_av)

        sub_bar = QWidget()
        sub_bar.setStyleSheet(
            "background:#181825;border:1px solid #45475a;border-radius:6px;")
        sub_bar.setFixedHeight(42)
        sl = QHBoxLayout(sub_bar)
        sl.setContentsMargins(4, 4, 4, 4)
        sl.setSpacing(4)
        self._sb_btns = {}
        for k, txt in [("post", "ĐĂNG BÀI"), ("comment", "COMMENT"), ("uptop", "UP TOP")]:
            b = QPushButton(txt)
            b.setFixedHeight(32)
            b.clicked.connect(lambda _, k=k: self._sub_switch(k))
            self._sb_btns[k] = b
            sl.addWidget(b)
        sl.addStretch()
        lay.addWidget(sub_bar)
        self._sub_switch("post")

        self._pnl_main  = self._make_settings_panel()
        self._pnl_comment = self._make_comment_panel()
        self._pnl_uptop = self._make_uptop_panel()
        lay.addWidget(self._pnl_main)
        lay.addWidget(self._pnl_comment)
        lay.addWidget(self._pnl_uptop)
        self._pnl_comment.setVisible(False)
        self._pnl_uptop.setVisible(False)

        ctrl = QHBoxLayout()
        ctrl.setSpacing(8)
        
        # 3 nút bắt đầu khác nhau cho 3 tab
        self._btn_start_post = QPushButton("▶  BẮT ĐẦU ĐĂNG BÀI")
        self._btn_start_post.setFixedHeight(48)
        self._btn_start_post.setStyleSheet(BTN_GREEN(15, 10))
        self._btn_start_post.clicked.connect(lambda: self._start_action("post"))
        
        self._btn_start_comment = QPushButton("▶  BẮT ĐẦU COMMENT")
        self._btn_start_comment.setFixedHeight(48)
        self._btn_start_comment.setStyleSheet(BTN_GREEN(15, 10))
        self._btn_start_comment.clicked.connect(lambda: self._start_action("comment"))
        self._btn_start_comment.setVisible(False)
        
        self._btn_start_uptop = QPushButton("▶  BẮT ĐẦU UP TOP")
        self._btn_start_uptop.setFixedHeight(48)
        self._btn_start_uptop.setStyleSheet(BTN_GREEN(15, 10))
        self._btn_start_uptop.clicked.connect(lambda: self._start_action("uptop"))
        self._btn_start_uptop.setVisible(False)
        
        self._btn_stop = QPushButton("■  DỪNG LẠI")
        self._btn_stop.setFixedHeight(48)
        self._btn_stop.setEnabled(False)
        self._btn_stop.setStyleSheet(BTN_RED(15, 10))
        self._btn_stop.clicked.connect(self._stop)
        
        ctrl.addWidget(self._btn_start_post)
        ctrl.addWidget(self._btn_start_comment)
        ctrl.addWidget(self._btn_start_uptop)
        ctrl.addWidget(self._btn_stop)
        lay.addLayout(ctrl)

        prog = QHBoxLayout()
        self._st_lbl = QLabel("Sẵn sàng")
        self._st_lbl.setStyleSheet("color:#6c7086;font-size:12px;background:transparent;")
        self._pbar = QProgressBar()
        self._pbar.setValue(0)
        self._pbar.setFormat("%p%")
        self._pbar.setFixedHeight(18)
        prog.addWidget(self._st_lbl)
        prog.addWidget(self._pbar, 1)
        lay.addLayout(prog)
        return p

    def _make_settings_panel(self):
        gb = QGroupBox("⚙  Cấu hình đăng bài")
        lay = QVBoxLayout(gb)
        lay.setContentsMargins(12, 8, 12, 10)
        lay.setSpacing(8)

        r1 = QHBoxLayout()
        self._chk_ai = QCheckBox("Dùng AI viết lại bài")
        self._chk_ai.setChecked(True)
        self._chk_ai.setEnabled(True)
        self._chk_ai.setVisible(True)
        
        ba = QPushButton("⚙ Cấu hình AI")
        ba.setFixedHeight(28)
        ba.setStyleSheet(BTN_BLUE(12, 6))
        ba.setEnabled(True)
        ba.setVisible(True)
        ba.clicked.connect(self._open_ai_config)
        
        bp = QPushButton("👁 Xem trước AI")
        bp.setFixedHeight(28)
        bp.setStyleSheet(BTN_GRAY)
        bp.setEnabled(True)
        bp.setVisible(True)
        bp.clicked.connect(lambda: self._preview_ai_content("post"))
        
        bc = QPushButton("📄 Chọn nội dung")
        bc.setFixedHeight(28)
        bc.setStyleSheet(BTN_GRAY)
        bc.setEnabled(True)
        bc.setVisible(True)
        bc.clicked.connect(self._open_content_viewer)
        
        r1.addWidget(self._chk_ai)
        r1.addStretch()
        r1.addWidget(ba)
        r1.addWidget(bp)
        r1.addWidget(bc)
        lay.addLayout(r1)

        r2 = QHBoxLayout()
        self._chk_rand = QCheckBox("Ngẫu nhiên số ảnh/video:")
        self._spin_med = QSpinBox()
        self._spin_med.setRange(1, 20)
        self._spin_med.setValue(1)
        self._spin_med.setFixedSize(58, 26)
        r2.addWidget(self._chk_rand)
        r2.addWidget(self._spin_med)
        r2.addStretch()
        lay.addLayout(r2)

        r3 = QHBoxLayout()
        dl = QLabel("⏱  Thời gian chờ:")
        dl.setStyleSheet("background:transparent;color:#a6adc8;")
        self._sp_d1 = QSpinBox()
        self._sp_d1.setRange(5, 3600)
        self._sp_d1.setValue(60)
        self._sp_d1.setFixedSize(68, 26)
        sep = QLabel("~")
        sep.setStyleSheet("background:transparent;color:#6c7086;")
        self._sp_d2 = QSpinBox()
        self._sp_d2.setRange(5, 3600)
        self._sp_d2.setValue(120)
        self._sp_d2.setFixedSize(68, 26)
        un = QLabel("giây / nhóm")
        un.setStyleSheet("background:transparent;color:#6c7086;font-size:12px;")
        r3.addWidget(dl)
        r3.addWidget(self._sp_d1)
        r3.addWidget(sep)
        r3.addWidget(self._sp_d2)
        r3.addWidget(un)
        r3.addStretch()
        lay.addLayout(r3)
        return gb

    def _make_uptop_panel(self):
        gb = QGroupBox("🔝  Cấu hình Up Top")
        lay = QVBoxLayout(gb)
        lay.setContentsMargins(12, 8, 12, 10)
        lay.setSpacing(6)

        guide = QLabel("📌  Dán link bài đã đăng (mỗi link 1 dòng). Nội dung comment dùng chung từ phần 'Nội dung bài viết'.")
        guide.setStyleSheet(
            "color:#6c7086;font-size:11px;font-style:italic;background:transparent;")
        guide.setWordWrap(True)
        lay.addWidget(guide)

        lay.addWidget(self._lbl("Link bài cần up top:"))
        self._uptop_links = QTextEdit()
        self._uptop_links.setPlaceholderText("https://www.facebook.com/groups/.../posts/...")
        self._uptop_links.setFixedHeight(100)
        self._uptop_links.setStyleSheet(
            "QTextEdit{background:#181825;border:1px solid #45475a;border-radius:4px;"
            "font-size:12px;font-family:'Courier New';color:#cdd6f4;padding:5px;}"
            "QTextEdit:focus{border-color:#89b4fa;}")
        lay.addWidget(self._uptop_links)

        r1 = QHBoxLayout()
        ql = QLabel("Số comment mỗi bài:")
        ql.setStyleSheet("background:transparent;color:#a6adc8;")
        self._uptop_cmt_count = QSpinBox()
        self._uptop_cmt_count.setRange(1, 100)
        self._uptop_cmt_count.setValue(1)
        self._uptop_cmt_count.setFixedSize(70, 26)
        r1.addWidget(ql)
        r1.addWidget(self._uptop_cmt_count)
        r1.addStretch()
        lay.addLayout(r1)

        r = QHBoxLayout()
        dl = QLabel("⏱  Thời gian chờ:")
        dl.setStyleSheet("background:transparent;color:#a6adc8;")
        self._sp_ut1 = QSpinBox()
        self._sp_ut1.setRange(5, 3600)
        self._sp_ut1.setValue(60)
        self._sp_ut1.setFixedSize(68, 26)
        sep = QLabel("~")
        sep.setStyleSheet("background:transparent;color:#6c7086;")
        self._sp_ut2 = QSpinBox()
        self._sp_ut2.setRange(5, 3600)
        self._sp_ut2.setValue(120)
        self._sp_ut2.setFixedSize(68, 26)
        un = QLabel("giây / bài")
        un.setStyleSheet("background:transparent;color:#6c7086;font-size:12px;")
        r.addWidget(dl)
        r.addWidget(self._sp_ut1)
        r.addWidget(sep)
        r.addWidget(self._sp_ut2)
        r.addWidget(un)
        r.addStretch()
        lay.addLayout(r)
        return gb

    def _make_comment_panel(self):
        gb = QGroupBox("💬  Cấu hình Comment")
        lay = QVBoxLayout(gb)
        lay.setContentsMargins(12, 8, 12, 10)
        lay.setSpacing(6)

        r1 = QHBoxLayout()
        ql = QLabel("Số lượng bài viết:")
        ql.setStyleSheet("background:transparent;color:#a6adc8;")
        self._cmt_count = QSpinBox()
        self._cmt_count.setRange(1, 100)
        self._cmt_count.setValue(3)
        self._cmt_count.setFixedSize(70, 26)
        r1.addWidget(ql)
        r1.addWidget(self._cmt_count)
        r1.addStretch()
        lay.addLayout(r1)

        # AI для comment
        r_ai = QHBoxLayout()
        self._cmt_chk_ai = QCheckBox("Dùng AI viết lại comment")
        self._cmt_chk_ai.setChecked(True)
        self._cmt_chk_ai.setVisible(True)
        self._cmt_chk_ai.setEnabled(True)
        
        ba_cmt = QPushButton("⚙ Cấu hình AI")
        ba_cmt.setFixedHeight(28)
        ba_cmt.setStyleSheet(BTN_BLUE(12, 6))
        ba_cmt.clicked.connect(self._open_ai_config)
        
        bp_cmt = QPushButton("👁 Xem trước AI")
        bp_cmt.setFixedHeight(28)
        bp_cmt.setStyleSheet(BTN_GRAY)
        bp_cmt.clicked.connect(lambda: self._preview_ai_content("comment"))
        
        bc_cmt = QPushButton("📄 Chọn nội dung")
        bc_cmt.setFixedHeight(28)
        bc_cmt.setStyleSheet(BTN_GRAY)
        bc_cmt.clicked.connect(self._open_content_viewer)
        
        r_ai.addWidget(self._cmt_chk_ai)
        r_ai.addStretch()
        r_ai.addWidget(ba_cmt)
        r_ai.addWidget(bp_cmt)
        r_ai.addWidget(bc_cmt)
        lay.addLayout(r_ai)

        # r2: Ẩn options random ảnh cho comment
        r2 = QHBoxLayout()
        self._cmt_chk_rand = QCheckBox("Ngẫu nhiên số ảnh/video:")
        self._cmt_spin_med = QSpinBox()
        self._cmt_spin_med.setRange(1, 20)
        self._cmt_spin_med.setValue(1)
        self._cmt_spin_med.setFixedSize(58, 26)
        r2.addWidget(self._cmt_chk_rand)
        r2.addWidget(self._cmt_spin_med)
        r2.addStretch()
        r2_widget = QWidget()
        r2_widget.setLayout(r2)
        r2_widget.setVisible(False)
        lay.addWidget(r2_widget)

        r3 = QHBoxLayout()
        dl = QLabel("⏱  Thời gian chờ:")
        dl.setStyleSheet("background:transparent;color:#a6adc8;")
        self._cmt_sp_d1 = QSpinBox()
        self._cmt_sp_d1.setRange(5, 3600)
        self._cmt_sp_d1.setValue(60)
        self._cmt_sp_d1.setFixedSize(68, 26)
        sep = QLabel("~")
        sep.setStyleSheet("background:transparent;color:#6c7086;")
        self._cmt_sp_d2 = QSpinBox()
        self._cmt_sp_d2.setRange(5, 3600)
        self._cmt_sp_d2.setValue(120)
        self._cmt_sp_d2.setFixedSize(68, 26)
        un = QLabel("giây / nhóm")
        un.setStyleSheet("background:transparent;color:#6c7086;font-size:12px;")
        r3.addWidget(dl)
        r3.addWidget(self._cmt_sp_d1)
        r3.addWidget(sep)
        r3.addWidget(self._cmt_sp_d2)
        r3.addWidget(un)
        r3.addStretch()
        lay.addLayout(r3)
        return gb

    def _make_group_right(self):
        p = QWidget()
        p.setStyleSheet("background:#181825;border-left:1px solid #313244;")
        p.setFixedWidth(500)
        lay = QVBoxLayout(p)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(0)

        h1 = QLabel("✔  KẾT QUẢ THÀNH CÔNG")
        h1.setFixedHeight(30)
        h1.setStyleSheet("background:#1c2e1c;color:#a6e3a1;font-weight:bold;font-size:12px;"
                         "padding:0 10px;border-bottom:1px solid #2e4a2e;")
        lay.addWidget(h1)
        self._suc = self._make_result_table(
            ["Time", "Nhóm", "Link Bài Viết", "Loại"], [60, 70, 200, 70], "#1c2e1c", "#a6e3a1", multiselect=True)
        self._suc.setContextMenuPolicy(Qt.CustomContextMenu)
        self._suc.customContextMenuRequested.connect(
            lambda p: self._res_menu(p, self._suc))
        lay.addWidget(self._suc, 2)

        h2 = QLabel("✖  KẾT QUẢ LỖI")
        h2.setFixedHeight(30)
        h2.setStyleSheet("background:#2e1c1c;color:#f38ba8;font-weight:bold;font-size:12px;"
                         "padding:0 10px;border-top:1px solid #4a2e2e;border-bottom:1px solid #4a2e2e;")
        lay.addWidget(h2)
        self._err = self._make_result_table(
            ["Time", "Nhóm", "Lỗi"], [68, 80], "#2e1c1c", "#f38ba8")
        lay.addWidget(self._err, 1)

        lh = QWidget()
        lh.setFixedHeight(30)
        lh.setStyleSheet("background:#1a1a2e;border-top:1px solid #313264;"
                         "border-bottom:1px solid #313264;")
        lhl = QHBoxLayout(lh)
        lhl.setContentsMargins(10, 0, 10, 0)
        ll = QLabel("📋  NHẬT KÝ GROUP")
        ll.setStyleSheet("color:#89b4fa;font-weight:bold;font-size:12px;background:transparent;")
        bc = QPushButton("Xóa")
        bc.setFixedHeight(22)
        bc.setStyleSheet("QPushButton{background:#313244;color:#a6adc8;border:1px solid #45475a;"
                         "border-radius:3px;font-size:11px;padding:0 8px;}"
                         "QPushButton:hover{background:#45475a;}")
        lhl.addWidget(ll)
        lhl.addStretch()
        lhl.addWidget(bc)
        lay.addWidget(lh)

        self._log = QTextEdit()
        self._log.setReadOnly(True)
        self._log.setStyleSheet(
            "QTextEdit{font-size:11px;background:#11111b;border:none;"
            "font-family:'Consolas','Courier New';color:#a6adc8;padding:4px;}")
        bc.clicked.connect(self._log.clear)
        lay.addWidget(self._log, 2)
        return p

    def _make_result_table(self, headers, col_widths, bg, hdr_color, multiselect=False):
        t = QTableWidget()
        t.setColumnCount(len(headers))
        t.setHorizontalHeaderLabels(headers)
        t.horizontalHeader().setStretchLastSection(True)
        for i, w in enumerate(col_widths):
            t.setColumnWidth(i, w)
        t.verticalHeader().setVisible(False)
        t.setEditTriggers(QAbstractItemView.NoEditTriggers)
        t.setShowGrid(False)
        # Cho phép multi-select nếu cần
        if multiselect:
            t.setSelectionMode(QAbstractItemView.ExtendedSelection)
            t.setSelectionBehavior(QAbstractItemView.SelectRows)
        t.setStyleSheet(
            f"QTableWidget{{font-size:11px;background:{bg};border:none;color:#cdd6f4;}}"
            f"QTableWidget::item{{padding:4px 6px;border:none;}}"
            f"QHeaderView::section{{background:#313244;font-size:11px;color:{hdr_color};"
            f"border:none;border-bottom:1px solid #45475a;padding:4px 6px;}}")
        return t

    def _sub_switch(self, tab):
        self._current_tab = tab  # Save current tab
        ACT = ("QPushButton{background:#89b4fa;color:#1e1e2e;border:none;"
               "border-radius:4px;font-size:12px;font-weight:bold;padding:4px 16px;}")
        OFF = ("QPushButton{background:#313244;color:#a6adc8;border:1px solid #45475a;"
               "border-radius:4px;font-size:12px;padding:4px 16px;}"
               "QPushButton:hover{background:#45475a;}")
        for k, b in self._sb_btns.items():
            b.setStyleSheet(ACT if k == tab else OFF)
        if hasattr(self, "_pnl_main"):
            self._pnl_main.setVisible(tab == "post")
            self._pnl_comment.setVisible(tab == "comment")
            self._pnl_uptop.setVisible(tab == "uptop")
            # Đổi tên nội dung bài viết
            if tab == "post":
                self._gb_nd.setTitle("📝  Nội dung bài viết")
            elif tab == "comment":
                self._gb_nd.setTitle("📝  Nội dung comment")
        
        # Hiển thị nút BẮT ĐẦU tương ứng
        if hasattr(self, "_btn_start_post"):
            self._btn_start_post.setVisible(tab == "post")
            self._btn_start_comment.setVisible(tab == "comment")
            self._btn_start_uptop.setVisible(tab == "uptop")

    def _res_menu(self, pos, tbl):
        m = QMenu(self)
        a = QAction("📋  Copy link bài viết", self)
        a.triggered.connect(lambda: self._copy_links(tbl))
        m.addAction(a)
        m.exec_(tbl.viewport().mapToGlobal(pos))

    def _copy_links(self, tbl):
        """Copy links từ các rows được chọn (hoặc tất cả nếu không chọn)."""
        selected_rows = tbl.selectionModel().selectedRows() if tbl.selectionModel() else []
        if selected_rows:
            links = [tbl.item(row.row(), 2).text() for row in selected_rows if tbl.item(row.row(), 2)]
        else:
            links = [tbl.item(r, 2).text() for r in range(tbl.rowCount()) if tbl.item(r, 2)]
        if links:
            text = "\n".join(links)
            QApplication.clipboard().setText(text)
            self._log_msg(f'<span style="color:#a6e3a1;font-size:11px;">✔ Copied {len(links)} link(s)</span>')

    def _add_media(self):
        files, _ = QFileDialog.getOpenFileNames(
            self, "Chọn ảnh/Video", "",
            "Media (*.jpg *.jpeg *.png *.gif *.bmp *.mp4 *.avi *.mov);;All Files (*)")
        for f in files:
            self._media.addItem(f)

    def _rm_media(self):
        for item in self._media.selectedItems():
            self._media.takeItem(self._media.row(item))

    def _start_action(self, action_type):
        """Bắt đầu thực thi dựa trên loại action (post/comment/uptop)"""
        if self._driver is None:
            self._log_msg('<span style="color:#f38ba8;font-size:11px;">'
                          '[ERROR] Chrome chưa mở hoặc chưa sẵn sàng.</span>')
            return

        # ── Lọc các groups được checkbox ─────────────────────────
        selected_groups = []
        for i in range(self._gt.rowCount()):
            chk = self._gt.cellWidget(i, 0)
            if isinstance(chk, QCheckBox) and chk.isChecked():
                url_item  = self._gt.item(i, 2)
                name_item = self._gt.item(i, 3)
                gurl = url_item.text()  if url_item  else ''
                gnm  = name_item.text() if name_item else ''
                if gurl:
                    selected_groups.append({'url': gurl, 'name': gnm})

        if not selected_groups:
            self._log_msg('<span style="color:#f38ba8;font-size:11px;">'
                          '[WARN] Chưa chọn nhóm nào (hãy tick checkbox ✓).</span>')
            return

        # ── Nội dung ──────────────────────────────────────────────
        content = self._content.toPlainText().strip()
        if not content:
            self._log_msg('<span style="color:#f38ba8;font-size:11px;">'
                          '[WARN] Chưa nhập nội dung.</span>')
            return

        # ── Danh sách ảnh / video ─────────────────────────────────
        media_list = []
        for i in range(self._media.count()):
            item = self._media.item(i)
            if item:
                file_path = item.text()
                file_name = os.path.basename(file_path)
                media_list.append({
                    'path': file_path,
                    'name': file_name
                })

        # ── Xử lý theo loại action ────────────────────────────────
        if action_type == "comment":
            use_random_media  = self._cmt_chk_rand.isChecked()
            random_media_count = self._cmt_spin_med.value() if use_random_media else 1
            delay_min = self._cmt_sp_d1.value()
            delay_max = self._cmt_sp_d2.value()
            cmt_count = self._cmt_count.value()
            use_ai = self._cmt_chk_ai.isChecked()
            ai_config = self._get_ai_config()

            data = {
                'profile':      self.profile_name,
                'groups':       selected_groups,
                'content':      content,
                'media':        media_list,
                'random_media': use_random_media,
                'media_count':  random_media_count,
                'cmt_count':    cmt_count,
                'delay_min':    delay_min,
                'delay_max':    delay_max,
                'use_ai':       use_ai,
                'ai_config':    ai_config,
            }

            ts = datetime.now().strftime("%H:%M:%S")
            self._log_msg(
                f'<span style="color:#89b4fa;font-size:11px;">'
                f'[{ts}] 💬 Bắt đầu comment {cmt_count} bài/nhóm | '
                f'{len(selected_groups)} nhóm | '
                f'Delay: {delay_min}~{delay_max}s</span>')

            # ── Khởi động worker ──────────────────────────────────────
            self._running      = True
            self._progress_val = 0
            self._total_groups = len(selected_groups)
            self._done_groups  = 0
            self._set_btn_enabled(False)
            self._st_lbl.setText(f"⏳  Đang chạy... 0/{self._total_groups}")
            self._pbar.setValue(0)
            self._pbar.setFormat(f"0 / {self._total_groups}")

            self._cmt_worker = CommentGroupsWorker(self._driver, data)
            self._cmt_worker.log_signal.connect(self._on_cmt_log)
            self._cmt_worker.success_signal.connect(self._on_cmt_success)
            self._cmt_worker.fail_signal.connect(self._on_cmt_fail)
            self._cmt_worker.finished.connect(self._on_cmt_finished)
            self._cmt_worker.start()

        elif action_type == "post":
            use_random_media  = self._chk_rand.isChecked()
            random_media_count = self._spin_med.value() if use_random_media else 1
            delay_min = self._sp_d1.value()
            delay_max = self._sp_d2.value()
            use_ai = self._chk_ai.isChecked()
            ai_config = self._get_ai_config()

            data = {
                'profile':      self.profile_name,
                'groups':       selected_groups,
                'content':      content,
                'media':        media_list,
                'random_media': use_random_media,
                'media_count':  random_media_count,
                'delay_min':    delay_min,
                'delay_max':    delay_max,
                'use_ai':       use_ai,
                'ai_config':    ai_config,
            }

            ts = datetime.now().strftime("%H:%M:%S")
            self._log_msg(
                f'<span style="color:#89b4fa;font-size:11px;">'
                f'[{ts}] 🚀 Bắt đầu đăng {len(selected_groups)} nhóm | '
                f'Delay: {delay_min}~{delay_max}s | '
                f'Media: {"random " + str(random_media_count) if use_random_media else "tuần tự"}</span>')

            print(f"[INFO] Start posting: {json.dumps(data, ensure_ascii=False)}", flush=True)

            # ── Khởi động worker ──────────────────────────────────────
            self._running      = True
            self._progress_val = 0
            self._total_groups = len(selected_groups)
            self._done_groups  = 0
            self._set_btn_enabled(False)
            self._st_lbl.setText(f"⏳  Đang chạy... 0/{self._total_groups}")
            self._pbar.setValue(0)
            self._pbar.setFormat(f"0 / {self._total_groups}")

            self._post_worker = PostGroupsWorker(self._driver, data)
            self._post_worker.log_signal.connect(self._on_post_log)
            self._post_worker.success_signal.connect(self._on_post_success)
            self._post_worker.fail_signal.connect(self._on_post_fail)
            self._post_worker.finished.connect(self._on_post_finished)
            self._post_worker.start()

        elif action_type == "uptop":
            # ── Lấy danh sách links từ text area ──────────────────
            uptop_links_text = self._uptop_links.toPlainText().strip()
            if not uptop_links_text:
                self._log_msg('<span style="color:#f38ba8;font-size:11px;">'
                              '[WARN] Chưa nhập link bài viết.</span>')
                return
            
            uptop_links = [link.strip() for link in uptop_links_text.split('\n') if link.strip()]
            cmt_count = self._uptop_cmt_count.value()
            delay_min = self._sp_ut1.value()
            delay_max = self._sp_ut2.value()
            use_ai = self._chk_ai.isChecked()
            ai_config = self._get_ai_config()

            data = {
                'profile':      self.profile_name,
                'posts':        uptop_links,
                'content':      content,
                'media':        media_list,
                'cmt_count':    cmt_count,
                'delay_min':    delay_min,
                'delay_max':    delay_max,
                'use_ai':       use_ai,
                'ai_config':    ai_config,
            }

            ts = datetime.now().strftime("%H:%M:%S")
            self._log_msg(
                f'<span style="color:#89b4fa;font-size:11px;">'
                f'[{ts}] 🔝 Bắt đầu UP TOP {cmt_count} comment/bài | '
                f'{len(uptop_links)} bài | '
                f'Delay: {delay_min}~{delay_max}s</span>')

            # ── Khởi động worker ──────────────────────────────────────
            self._running      = True
            self._progress_val = 0
            self._total_groups = len(uptop_links)
            self._done_groups  = 0
            self._set_btn_enabled(False)
            self._st_lbl.setText(f"⏳  Đang chạy... 0/{self._total_groups}")
            self._pbar.setValue(0)
            self._pbar.setFormat(f"0 / {self._total_groups}")

            self._uptop_worker = UpTopWorker(self._driver, data)
            self._uptop_worker.log_signal.connect(self._on_uptop_log)
            self._uptop_worker.success_signal.connect(self._on_uptop_success)
            self._uptop_worker.fail_signal.connect(self._on_uptop_fail)
            self._uptop_worker.finished.connect(self._on_uptop_finished)
            self._uptop_worker.start()

    def _set_btn_enabled(self, enabled):
        """Enable/disable nút start tương ứng với tab hiện tại"""
        if hasattr(self, "_btn_start_post"):
            if self._current_tab == "post":
                self._btn_start_post.setEnabled(enabled)
            elif self._current_tab == "comment":
                self._btn_start_comment.setEnabled(enabled)
            elif self._current_tab == "uptop":
                self._btn_start_uptop.setEnabled(enabled)
        self._btn_stop.setEnabled(not enabled)

    def _update_progress(self):
        """Cập nhật progress bar theo số nhóm đã xử lý."""
        if not hasattr(self, '_total_groups') or self._total_groups == 0:
            return
        pct = int(self._done_groups / self._total_groups * 100)
        self._pbar.setValue(pct)
        self._pbar.setFormat(f"{self._done_groups} / {self._total_groups}")
        self._st_lbl.setText(f"⏳  Đang chạy... {self._done_groups}/{self._total_groups}")

    def _on_post_finished(self):
        self._running = False
        self._timer.stop()
        self._pbar.setValue(100)
        if hasattr(self, '_total_groups'):
            self._pbar.setFormat(f"{self._total_groups} / {self._total_groups}")
        self._set_btn_enabled(True)
        ts = datetime.now().strftime("%H:%M:%S")
        suc = self._suc.rowCount()
        err = self._err.rowCount()
        self._st_lbl.setText(f"✔ Hoàn thành  ✅{suc}  ❌{err}")
        self._log_msg(
            f'<span style="color:#a6e3a1;font-size:11px;">'
            f'[{ts}] ✅ HOÀN THÀNH — Thành công: {suc} | Lỗi: {err}</span>')
        if hasattr(self, '_post_worker') and self._post_worker is not None:
            self._post_worker.deleteLater()
            self._post_worker = None

    def _stop(self):
        self._running = False
        self._timer.stop()
        self._set_btn_enabled(True)
        self._st_lbl.setText("⏹  Đã dừng")

    def _tick(self):
        """Tick timer — không còn dùng để fake progress, chỉ giữ lại phòng trường hợp cần."""
        pass

    # ══════════════════════════════════════════════════════════════════════════
    # TAB: ĐĂNG PAGE
    # ══════════════════════════════════════════════════════════════════════════
    def _build_page(self):
        w = QWidget()
        lay = QHBoxLayout(w)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(0)
        lay.addWidget(self._make_page_left())
        lay.addWidget(self._make_page_center(), 1)
        lay.addWidget(self._make_page_right())
        return w

    def _make_page_left(self):
        p = QWidget()
        p.setStyleSheet("background:#181825;border-right:1px solid #313244;")
        p.setFixedWidth(316)
        lay = QVBoxLayout(p)
        lay.setContentsMargins(8, 8, 8, 8)
        lay.setSpacing(6)

        fi = QLineEdit()
        fi.setPlaceholderText("🔍  Tìm page...")
        fi.setFixedHeight(28)
        fi.setStyleSheet(
            "QLineEdit{background:#313244;border:1px solid #45475a;"
            "border-radius:4px;padding:2px 10px;font-size:12px;color:#cdd6f4;}"
            "QLineEdit:focus{border-color:#89b4fa;}")
        lay.addWidget(fi)

        self._pt = QTableWidget()
        self._pt.setColumnCount(3)
        self._pt.setHorizontalHeaderLabels(["#", "ID Page", "Tên Page"])
        self._pt.horizontalHeader().setStretchLastSection(True)
        self._pt.setColumnWidth(0, 32)
        self._pt.setColumnWidth(1, 95)
        self._pt.setSelectionBehavior(QAbstractItemView.SelectRows)
        self._pt.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self._pt.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self._pt.setAlternatingRowColors(True)
        self._pt.verticalHeader().setVisible(False)
        self._pt.setShowGrid(False)
        self._pt.setContextMenuPolicy(Qt.CustomContextMenu)
        self._pt.customContextMenuRequested.connect(
            lambda pos: self._simple_menu(pos, self._pt))
        self._pt.setStyleSheet(self._gt.styleSheet())
        lay.addWidget(self._pt, 1)

        br = QHBoxLayout()
        br.setSpacing(6)
        b1 = QPushButton("⬇  LẤY DS PAGE")
        b1.setFixedHeight(34)
        b1.setStyleSheet(BTN_GREEN(12, 6))
        b1.clicked.connect(self._load_pages)
        b2 = QPushButton("📂  LOAD DATA")
        b2.setFixedHeight(34)
        b2.setStyleSheet(BTN_GRAY)
        br.addWidget(b1)
        br.addWidget(b2)
        lay.addLayout(br)
        return p

    def _load_pages(self):
        pages = [
            ("101834829", "Tiến Khoa Official"),
            ("209384756", "BĐS Sài Gòn 24h"),
            ("345678901", "Nhà Đất TP.HCM"),
            ("456789012", "Bất Động Sản Việt"),
            ("567890123", "Mua Bán Nhà Đất"),
        ]
        self._pt.setRowCount(len(pages))
        for i, (pid, pnm) in enumerate(pages):
            si = QTableWidgetItem(str(i + 1))
            si.setTextAlignment(Qt.AlignCenter)
            self._pt.setItem(i, 0, si)
            self._pt.setItem(i, 1, QTableWidgetItem(pid))
            self._pt.setItem(i, 2, QTableWidgetItem(pnm))
            self._pt.setRowHeight(i, 28)

    def _simple_menu(self, pos, tbl):
        m = QMenu(self)
        for txt, fn in [("Chọn tất cả", tbl.selectAll),
                        ("Bỏ chọn tất cả", tbl.clearSelection)]:
            a = QAction(txt, self)
            a.triggered.connect(fn)
            m.addAction(a)
        m.exec_(tbl.viewport().mapToGlobal(pos))

    def _make_page_center(self):
        p = QWidget()
        lay = QVBoxLayout(p)
        lay.setContentsMargins(10, 10, 10, 8)
        lay.setSpacing(8)

        gb_nd = QGroupBox("📝  Nội dung bài viết")
        gbl = QVBoxLayout(gb_nd)
        gbl.setContentsMargins(10, 8, 10, 10)
        self._page_content = QTextEdit()
        self._page_content.setPlaceholderText(
            "Nhập nội dung... Hỗ trợ Spin {nội dung 1|nội dung 2}")
        self._page_content.setMinimumHeight(140)
        self._page_content.setStyleSheet(
            "QTextEdit{background:#181825;border:1px solid #45475a;border-radius:6px;"
            "font-size:13px;color:#cdd6f4;padding:8px;}"
            "QTextEdit:focus{border-color:#89b4fa;}")
        gbl.addWidget(self._page_content)
        lay.addWidget(gb_nd)

        gb_av = QGroupBox("🖼  Danh sách ảnh / Video")
        gb_av.setFixedHeight(112)
        avl = QHBoxLayout(gb_av)
        avl.setContentsMargins(10, 6, 10, 10)
        self._page_media = QListWidget()
        avr = QVBoxLayout()
        avr.setSpacing(4)
        for txt in ["+ Thêm", "✕ Xóa", "⊘ Clear"]:
            b = QPushButton(txt)
            b.setFixedSize(90, 26)
            b.setStyleSheet(BTN_GRAY)
            avr.addWidget(b)
        avr.addStretch()
        avl.addWidget(self._page_media, 1)
        avl.addLayout(avr)
        lay.addWidget(gb_av)

        gb_cfg = QGroupBox("⚙  Cấu hình đăng page")
        psl = QVBoxLayout(gb_cfg)
        psl.setContentsMargins(12, 8, 12, 10)
        psl.setSpacing(8)

        r1 = QHBoxLayout()
        chk = QCheckBox("Dùng AI viết lại bài")
        chk.setChecked(True)
        ba = QPushButton("⚙ Cấu hình AI")
        ba.setFixedHeight(28)
        ba.setStyleSheet(BTN_BLUE(12, 6))
        bc2 = QPushButton("📄 Chọn nội dung")
        bc2.setFixedHeight(28)
        bc2.setStyleSheet(BTN_GRAY)
        r1.addWidget(chk)
        r1.addStretch()
        r1.addWidget(ba)
        r1.addWidget(bc2)
        psl.addLayout(r1)

        r2 = QHBoxLayout()
        chk2 = QCheckBox("Ngẫu nhiên số ảnh/video:")
        sp2 = QSpinBox()
        sp2.setRange(1, 20)
        sp2.setValue(1)
        sp2.setFixedSize(58, 26)
        r2.addWidget(chk2)
        r2.addWidget(sp2)
        r2.addStretch()
        psl.addLayout(r2)

        r3 = QHBoxLayout()
        dl = QLabel("⏱  Thời gian chờ:")
        dl.setStyleSheet("background:transparent;color:#a6adc8;")
        sp3a = QSpinBox()
        sp3a.setRange(5, 3600)
        sp3a.setValue(60)
        sp3a.setFixedSize(68, 26)
        ss = QLabel("~")
        ss.setStyleSheet("background:transparent;color:#6c7086;")
        sp3b = QSpinBox()
        sp3b.setRange(5, 3600)
        sp3b.setValue(120)
        sp3b.setFixedSize(68, 26)
        un = QLabel("giây / page")
        un.setStyleSheet("background:transparent;color:#6c7086;font-size:12px;")
        r3.addWidget(dl)
        r3.addWidget(sp3a)
        r3.addWidget(ss)
        r3.addWidget(sp3b)
        r3.addWidget(un)
        r3.addStretch()
        psl.addLayout(r3)
        lay.addWidget(gb_cfg)
        lay.addStretch()

        cr = QHBoxLayout()
        cr.setSpacing(8)
        self._pg_start = QPushButton("▶  BẮT ĐẦU")
        self._pg_start.setFixedHeight(48)
        self._pg_start.setStyleSheet(BTN_GREEN(15, 10))
        self._pg_stop = QPushButton("■  DỪNG LẠI")
        self._pg_stop.setFixedHeight(48)
        self._pg_stop.setEnabled(False)
        self._pg_stop.setStyleSheet(BTN_RED(15, 10))
        cr.addWidget(self._pg_start)
        cr.addWidget(self._pg_stop)
        lay.addLayout(cr)

        pr = QHBoxLayout()
        self._pg_st_lbl = QLabel("Sẵn sàng")
        self._pg_st_lbl.setStyleSheet("color:#6c7086;font-size:12px;background:transparent;")
        self._pg_pbar = QProgressBar()
        self._pg_pbar.setValue(0)
        self._pg_pbar.setFormat("%p%")
        self._pg_pbar.setFixedHeight(18)
        pr.addWidget(self._pg_st_lbl)
        pr.addWidget(self._pg_pbar, 1)
        lay.addLayout(pr)
        return p

    def _make_page_right(self):
        p = QWidget()
        p.setStyleSheet("background:#181825;border-left:1px solid #313244;")
        p.setFixedWidth(358)
        lay = QVBoxLayout(p)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(0)

        h1 = QLabel("✔  KẾT QUẢ THÀNH CÔNG")
        h1.setFixedHeight(30)
        h1.setStyleSheet("background:#1c2e1c;color:#a6e3a1;font-weight:bold;font-size:12px;"
                         "padding:0 10px;border-bottom:1px solid #2e4a2e;")
        lay.addWidget(h1)
        self._pg_suc = self._make_result_table(
            ["Time", "Page", "Link"], [68, 80], "#1c2e1c", "#a6e3a1")
        lay.addWidget(self._pg_suc, 2)

        h2 = QLabel("✖  KẾT QUẢ LỖI")
        h2.setFixedHeight(30)
        h2.setStyleSheet("background:#2e1c1c;color:#f38ba8;font-weight:bold;font-size:12px;"
                         "padding:0 10px;border-top:1px solid #4a2e2e;border-bottom:1px solid #4a2e2e;")
        lay.addWidget(h2)
        self._pg_err = self._make_result_table(
            ["Time", "Page", "Lỗi"], [68, 80], "#2e1c1c", "#f38ba8")
        lay.addWidget(self._pg_err, 1)

        lh = QWidget()
        lh.setFixedHeight(30)
        lh.setStyleSheet("background:#1a1a2e;border-top:1px solid #313264;"
                         "border-bottom:1px solid #313264;")
        lhl = QHBoxLayout(lh)
        lhl.setContentsMargins(10, 0, 10, 0)
        ll = QLabel("📋  NHẬT KÝ PAGE")
        ll.setStyleSheet("color:#89b4fa;font-weight:bold;font-size:12px;background:transparent;")
        bc = QPushButton("Xóa")
        bc.setFixedHeight(22)
        bc.setStyleSheet("QPushButton{background:#313244;color:#a6adc8;border:1px solid #45475a;"
                         "border-radius:3px;font-size:11px;padding:0 8px;}"
                         "QPushButton:hover{background:#45475a;}")
        lhl.addWidget(ll)
        lhl.addStretch()
        lhl.addWidget(bc)
        lay.addWidget(lh)

        self._pg_log = QTextEdit()
        self._pg_log.setReadOnly(True)
        self._pg_log.setStyleSheet(
            "QTextEdit{font-size:11px;background:#11111b;border:none;"
            "font-family:'Consolas','Courier New';color:#a6adc8;padding:4px;}")
        bc.clicked.connect(self._pg_log.clear)
        lay.addWidget(self._pg_log, 2)
        return p

    @staticmethod
    def _lbl(txt):
        l = QLabel(txt)
        l.setStyleSheet(
            "background:transparent;font-weight:bold;font-size:12px;color:#a6adc8;")
        return l

    # ══════════════════════════════════════════════════════════════════════════
    # TAB: CÁCH CANH
    # ══════════════════════════════════════════════════════════════════════════
    def _build_settings(self):
        w = QWidget()
        w.setStyleSheet("background:#1e1e2e;")
        lay = QVBoxLayout(w)
        lay.setContentsMargins(16, 16, 16, 16)
        lay.setSpacing(12)

        title = QLabel("🔧  QUẢN LÝ PROFILE")
        title.setFont(QFont("Segoe UI", 14, QFont.Bold))
        title.setStyleSheet("color:#89b4fa;background:transparent;")
        lay.addWidget(title)

        info = QLabel(f"Profile hiện tại: {self.profile_name}")
        info.setStyleSheet("color:#a6adc8;background:transparent;font-size:12px;")
        lay.addWidget(info)
        lay.addStretch()
        return w
    def _focus_chrome(self, event):
        """Forward mouse focus về Chrome khi click vào container"""
        if self._chrome_hwnd and win32gui.IsWindow(self._chrome_hwnd):
            try:
                win32gui.SetFocus(self._chrome_hwnd)
            except Exception:
                pass
    def _build_browser(self):
        w = QWidget()
        w.setStyleSheet("background:#1e1e2e;")
        lay = QVBoxLayout(w)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(0)

        # Container for Chrome
        self._chrome_container = ResizableContainer()
        self._chrome_container.resized.connect(self._sync_chrome_size)
        self._chrome_container.mousePressEvent = self._focus_chrome
        self._chrome_container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self._chrome_container.setStyleSheet("background:#000000;")
        self._chrome_container.setAttribute(Qt.WA_NativeWindow)
        self._chrome_container.setAttribute(Qt.WA_DontCreateNativeAncestors)
        
        # Install keyboard event filter để forward input tới Chrome
        self._chrome_kb_filter = ChromeKeyboardFilter(lambda: self._chrome_hwnd)
        self._chrome_container.installEventFilter(self._chrome_kb_filter)        
        container_layout = QVBoxLayout(self._chrome_container)
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.setSpacing(0)
        
        # Status label
        self._chrome_status = QLabel("⏳  Khởi động Chrome...")
        self._chrome_status.setAlignment(Qt.AlignCenter)
        self._chrome_status.setStyleSheet("color:#89b4fa;font-size:14px;background:transparent;")
        container_layout.addWidget(self._chrome_status)
        
        lay.addWidget(self._chrome_container, 1)

        return w


# ═══════════════════════════════════════════════════════════════════════════════
#  MAIN WINDOW
# ═══════════════════════════════════════════════════════════════════════════════
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tiến Khoa  ·  Marketing Tự động")
        self.resize(1120, 700)
        self.setMinimumSize(820, 520)
        self.setStyleSheet(DARK)
        self._windows: dict[str, FacebookWindow] = {}
        self._machine_id = self._mk_id()
        self._activated  = False
        self._key_checked = False
        self._build()

    def showEvent(self, e):
        """Check key lần đầu khi window được show"""
        super().showEvent(e)
        if not self._key_checked:
            self._key_checked = True
            QTimer.singleShot(500, self._check_key_startup)

    def _mk_id(self):
        import hashlib, uuid
        h = hashlib.md5(str(uuid.getnode()).encode()).hexdigest().upper()
        return f"{h[:4]}-{h[4:8]}-{h[8:12]}-{h[12:16]}"

    def _check_key_startup(self):
        """Kiểm tra key khi khởi động ứng dụng"""
        print(f"\n{'='*60}")
        print(f"[STARTUP] 🔍 Checking key on startup...")
        print(f"{'='*60}")
        key_checker = KeyChecker()
        is_valid, message = key_checker.check_key_startup()
        print(f"[STARTUP] Result: is_valid={is_valid}, message='{message}'")
        print(f"{'='*60}\n")
        
        if not is_valid:
            print(f"[STARTUP] ❌ Key invalid or missing, showing license dialog...")
            # Key không hợp lệ → show dialog
            self._license()
        else:
            print(f"[STARTUP] ✅ Key valid, app ready to use")
            self._activated = True

    def _build(self):
        mb = self.menuBar()
        mb.setStyleSheet(
            "QMenuBar{background:#11111b;color:#cdd6f4;font-size:15px;"
            "font-weight:bold;min-height:44px;padding:0 14px;border-bottom:1px solid #313244;}"
            "QMenuBar::item{background:transparent;color:#cdd6f4;padding:10px 0;}"
            "QMenuBar::item:disabled{color:#89b4fa;}")
        act = QAction("◈  Tiến Khoa", self)
        act.setEnabled(False)
        mb.addAction(act)

        corner = QWidget()
        corner.setStyleSheet("background:#11111b;")
        cl = QHBoxLayout(corner)
        cl.setContentsMargins(0, 0, 12, 0)
        cl.setSpacing(2)
        for txt, slot in [("📖 Hướng dẫn", self._help),
                           ("🔑 License",   self._license),
                           ("🔄 Update",    self._update)]:
            b = QPushButton(txt)
            b.setStyleSheet(
                "QPushButton{background:transparent;color:#a6adc8;border:none;"
                "padding:8px 12px;font-size:12px;border-radius:4px;}"
                "QPushButton:hover{background:#313244;color:#cdd6f4;}")
            b.clicked.connect(slot)
            cl.addWidget(b)
        mb.setCornerWidget(corner, Qt.TopRightCorner)

        cw = QWidget()
        self.setCentralWidget(cw)
        root = QHBoxLayout(cw)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)
        root.addWidget(self._make_left())
        root.addWidget(self._make_right(), 1)

        sb = QStatusBar()
        sb.setStyleSheet("QStatusBar{background:#11111b;border-top:1px solid #313244;"
                         "font-size:12px;color:#6c7086;}"
                         "QStatusBar QLabel{background:transparent;}")
        self.setStatusBar(sb)
        self._sr = QLabel(
            "Hạn sử dụng: Chưa kích hoạt   ·   Version 13.3.26   ·   Zalo 0327974700")
        self._sr.setStyleSheet(
            "color:#6c7086;font-size:12px;padding-right:12px;background:transparent;")
        sb.addPermanentWidget(self._sr)
        sb.showMessage(
            "  Sẵn sàng   ·   Gói 6 tháng: 600.000đ   ·   12 tháng: 1.000.000đ   ·   Vĩnh Viễn: 3.000.000đ")

    def _make_left(self):
        p = QWidget()
        p.setStyleSheet("background:#181825;border-right:1px solid #313244;")
        p.setFixedWidth(292)
        lay = QVBoxLayout(p)
        lay.setContentsMargins(14, 14, 14, 14)
        lay.setSpacing(12)

        ab = QGroupBox("➕  Thêm Profile Mới")
        al = QVBoxLayout(ab)
        al.setContentsMargins(12, 10, 12, 12)
        al.setSpacing(8)
        lbl = QLabel("Tên Profile:")
        lbl.setStyleSheet("background:transparent;color:#a6adc8;font-size:12px;")
        self._name_in = QLineEdit()
        self._name_in.setPlaceholderText("VD: FB Sales 01")
        self._name_in.setFixedHeight(30)
        self._name_in.returnPressed.connect(self._create)
        btn_cr = QPushButton("✚  TẠO PROFILE")
        btn_cr.setFixedHeight(36)
        btn_cr.setStyleSheet(BTN_GREEN(13, 7))
        btn_cr.clicked.connect(self._create)
        brow = QHBoxLayout()
        brow.setSpacing(6)
        for txt, fn in [("🗑 Xóa", self._delete),
                        ("↺ Làm mới", self._load_profiles),
                        ("✕ Đóng", self.close)]:
            b = QPushButton(txt)
            b.setFixedHeight(28)
            b.setStyleSheet(BTN_GRAY)
            b.clicked.connect(fn)
            brow.addWidget(b)
        al.addWidget(lbl)
        al.addWidget(self._name_in)
        al.addWidget(btn_cr)
        al.addLayout(brow)
        lay.addWidget(ab)

        cb = QGroupBox("🎛  Bảng Điều Khiển")
        cl2 = QVBoxLayout(cb)
        cl2.setContentsMargins(12, 10, 12, 12)
        cl2.setSpacing(10)
        self._chk_mute = QCheckBox("Tắt âm thanh trình duyệt")
        self._chk_mute.setChecked(True)

        self._btn_fb = QPushButton("🌐  MỞ TÍNH NĂNG FACEBOOK")
        self._btn_fb.setFixedHeight(46)
        self._btn_fb.setStyleSheet(BTN_BLUE(13, 10))
        self._btn_fb.clicked.connect(self._open_fb)

        note = QLabel(
            "✦ Chọn 1 tài khoản → bấm nút\n  (Double-click tên cũng mở được)\n"
            "✦ Chrome tự khởi động khi mở cửa sổ")
        note.setStyleSheet(
            "color:#6c7086;font-size:11px;font-style:italic;background:transparent;")
        note.setWordWrap(True)

        self._btn_zalo = QPushButton("💬  MỞ TÍNH NĂNG ZALO")
        self._btn_zalo.setFixedHeight(46)
        self._btn_zalo.setStyleSheet(BTN_GREEN(13, 10))
        self._btn_zalo.clicked.connect(self._open_zalo)

        cl2.addWidget(self._chk_mute)
        cl2.addWidget(self._btn_fb)
        cl2.addWidget(note)
        cl2.addWidget(self._btn_zalo)
        lay.addWidget(cb)

        sb2 = QGroupBox("⊞  Sắp xếp cửa sổ")
        sl = QVBoxLayout(sb2)
        sl.setContentsMargins(12, 10, 12, 12)
        sl.setSpacing(8)
        row1 = QHBoxLayout()
        lbl2 = QLabel("Số cột:")
        lbl2.setStyleSheet("background:transparent;color:#a6adc8;font-size:12px;")
        self._spin_cols = QSpinBox()
        self._spin_cols.setRange(1, 6)
        self._spin_cols.setValue(2)
        self._spin_cols.setFixedSize(54, 28)
        row1.addWidget(lbl2)
        row1.addWidget(self._spin_cols)
        row1.addStretch()
        sl.addLayout(row1)
        btn_tile = QPushButton("⊞  SẮP XẾP CỬA SỔ")
        btn_tile.setFixedHeight(34)
        btn_tile.setStyleSheet(BTN_GRAY)
        btn_tile.clicked.connect(self._tile_windows)
        sl.addWidget(btn_tile)
        lay.addWidget(sb2)
        lay.addStretch()
        return p

    def _make_right(self):
        p = QWidget()
        p.setStyleSheet("background:#1e1e2e;")
        lay = QVBoxLayout(p)
        lay.setContentsMargins(12, 12, 12, 12)
        lay.setSpacing(8)

        tl = QLabel("Danh sách tài khoản (Profiles)")
        tl.setFont(QFont("Segoe UI", 13, QFont.Bold))
        tl.setStyleSheet("color:#cdd6f4;background:transparent;")
        lay.addWidget(tl)

        self._tbl = QTableWidget()
        self._tbl.setColumnCount(8)
        self._tbl.setHorizontalHeaderLabels(
            ["#", "Profile", "Trạng thái", "UID", "Pass", "2FA", "Email", "PassMail"])
        self._tbl.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self._tbl.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        for col, w in [(0, 40), (3, 92), (4, 80), (5, 60), (6, 90), (7, 82)]:
            self._tbl.setColumnWidth(col, w)
        self._tbl.setSelectionBehavior(QAbstractItemView.SelectRows)
        self._tbl.setSelectionMode(QAbstractItemView.SingleSelection)
        self._tbl.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self._tbl.setAlternatingRowColors(True)
        self._tbl.verticalHeader().setVisible(False)
        self._tbl.setShowGrid(False)
        self._tbl.setContextMenuPolicy(Qt.CustomContextMenu)
        self._tbl.customContextMenuRequested.connect(self._tbl_menu)
        self._tbl.doubleClicked.connect(self._open_fb)
        self._tbl.setStyleSheet(
            "QTableWidget{border:1px solid #45475a;border-radius:6px;background:#181825;"
            "alternate-background-color:#1e1e2e;}"
            "QTableWidget::item{padding:5px 6px;border:none;}"
            "QTableWidget::item:selected{background:#45475a;color:#89b4fa;}"
            "QHeaderView::section{background:#313244;color:#89b4fa;font-weight:bold;"
            "border:none;border-bottom:1px solid #45475a;padding:6px 8px;font-size:12px;}")
        lay.addWidget(self._tbl)
        self._load_profiles()
        return p

    def _tbl_menu(self, pos):
        m = QMenu(self)
        for txt, fn in [("🌐 Mở tính năng Facebook", self._open_fb),
                        ("💬 Mở tính năng Zalo",     self._open_zalo),
                        ("🗑 Xóa Profile",            self._delete)]:
            a = QAction(txt, self)
            a.triggered.connect(fn)
            m.addAction(a)
        m.exec_(self._tbl.viewport().mapToGlobal(pos))

    def _create(self):
        name = self._name_in.text().strip()
        if not name:
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập tên Profile!")
            return
        for r in range(self._tbl.rowCount()):
            it = self._tbl.item(r, 1)
            if it and it.text() == name:
                QMessageBox.warning(self, "Lỗi", f"Profile '{name}' đã tồn tại!")
                return
        r = self._tbl.rowCount()
        self._tbl.insertRow(r)
        for j, v in enumerate([str(r + 1), name, "disconnect", "", "", "", "", ""]):
            it = QTableWidgetItem(v)
            if j == 0:
                it.setTextAlignment(Qt.AlignCenter)
            self._tbl.setItem(r, j, it)
        self._tbl.setRowHeight(r, 32)
        self._name_in.clear()
        self._tbl.selectRow(r)
        self._save_profiles()

    def _delete(self):
        r = self._tbl.currentRow()
        if r < 0:
            QMessageBox.information(self, "", "Vui lòng chọn Profile cần xóa!")
            return
        nm = self._tbl.item(r, 1).text() if self._tbl.item(r, 1) else ""
        if QMessageBox.question(self, "Xác nhận", f"Xóa Profile '{nm}'?",
                                QMessageBox.Yes | QMessageBox.No) == QMessageBox.Yes:
            self._tbl.removeRow(r)
            self._save_profiles()

    def _profile_file(self) -> str:
        base = os.path.dirname(os.path.abspath(__file__))
        data = os.path.join(base, "data")
        os.makedirs(data, exist_ok=True)
        return os.path.join(data, "profile.json")

    def _load_profiles(self):
        path = self._profile_file()
        if not os.path.isfile(path):
            return
        try:
            with open(path, "r", encoding="utf-8") as f:
                profiles = json.load(f)
            self._tbl.setRowCount(0)
            for profile in profiles:
                r = self._tbl.rowCount()
                self._tbl.insertRow(r)
                if isinstance(profile, dict):
                    row_data = [
                        profile.get("id", ""),
                        profile.get("profile", ""),
                        profile.get("status", ""),
                        profile.get("uid", ""),
                        profile.get("pass", ""),
                        profile.get("2fa", ""),
                        profile.get("email", ""),
                        profile.get("passmail", ""),
                    ]
                else:
                    row_data = profile
                for j, v in enumerate(row_data):
                    it = QTableWidgetItem(str(v))
                    if j == 0:
                        it.setTextAlignment(Qt.AlignCenter)
                    self._tbl.setItem(r, j, it)
                self._tbl.setRowHeight(r, 32)
        except Exception as e:
            print(f"[Profile] Load lỗi: {e}")

    def _save_profiles(self):
        path = self._profile_file()
        try:
            profiles = []
            for r in range(self._tbl.rowCount()):
                def cell(col, _r=r):
                    it = self._tbl.item(_r, col)
                    return it.text() if it else ""
                profiles.append({
                    "id":       cell(0),
                    "profile":  cell(1),
                    "status":   cell(2),
                    "uid":      cell(3),
                    "pass":     cell(4),
                    "2fa":      cell(5),
                    "email":    cell(6),
                    "passmail": cell(7),
                })
            with open(path, "w", encoding="utf-8") as f:
                json.dump(profiles, f, ensure_ascii=False, indent=2)
            print(f"[Profile] Đã lưu {len(profiles)} profiles", flush=True)
        except Exception as e:
            print(f"[Profile] Save lỗi: {e}")

    def _open_fb(self):
        r = self._tbl.currentRow()
        if r < 0:
            QMessageBox.information(
                self, "",
                "Vui lòng chọn 1 tài khoản!\n(hoặc double-click vào tên profile)")
            return
        nm_it = self._tbl.item(r, 1)
        name  = nm_it.text() if nm_it else f"Profile {r + 1}"

        if name in self._windows and self._windows[name].isVisible():
            w = self._windows[name]
            if w.isMinimized():
                w.showNormal()
            w.raise_()
            w.activateWindow()
        else:
            w = FacebookWindow(name)
            w.window_closed.connect(lambda nm: self._windows.pop(nm, None))
            self._windows[name] = w
            offset = len(self._windows) * 28
            scr = QApplication.primaryScreen().availableGeometry()
            w.move(min(scr.left() + 80 + offset, scr.right() - 820),
                   min(scr.top()  + 40 + offset, scr.bottom() - 620))
            w.show()

        it = self._tbl.item(r, 2)
        if it:
            it.setText("Chưa login")
            it.setForeground(QBrush(QColor("#a6e3a1")))

    def _open_zalo(self):
        r = self._tbl.currentRow()
        if r < 0:
            QMessageBox.information(self, "", "Vui lòng chọn 1 tài khoản!")
            return
        nm = self._tbl.item(r, 1).text() if self._tbl.item(r, 1) else "Profile"
        QMessageBox.information(self, "Zalo Tiến Khoa",
            f"Đang mở Zalo cho: {nm}\n\n"
            "• Nhắn tin & kết bạn theo danh sách SĐT\n"
            "• Nhắn tin đến bạn bè và nhóm Zalo")

    def _tile_windows(self):
        wins = [w for w in self._windows.values() if w.isVisible()]
        if not wins:
            QMessageBox.information(self, "", "Chưa có cửa sổ Facebook nào đang mở!")
            return
        cols = max(1, self._spin_cols.value())
        rows = (len(wins) + cols - 1) // cols
        scr  = QApplication.primaryScreen().availableGeometry()
        cw   = scr.width() // cols
        ch   = scr.height() // rows
        for idx, win in enumerate(wins):
            col = idx % cols
            row = idx // cols
            win.showNormal()
            win.setGeometry(QRect(
                scr.left() + col * cw,
                scr.top()  + row * ch,
                cw - 4, ch - 4))
            win.raise_()

    def _help(self):
        QMessageBox.information(self, "Hướng dẫn Tiến Khoa",
            "📖 HƯỚNG DẪN:\n\n"
            "1. Nhập tên profile → TẠO PROFILE\n"
            "2. Chọn profile trong bảng\n"
            "3. Bấm MỞ TÍNH NĂNG FACEBOOK\n"
            "4. Đăng nhập Facebook trong tab Trình Duyệt\n"
            "5. Chuyển sang ĐĂNG NHÓM / ĐĂNG PAGE\n\n"
            "📞 HOTLINE: 0327974700 (Zalo)")

    def _license(self):
        """Show dialog kích hoạt key"""
        d = LicenseDialog(self._machine_id, self)
        d.activated.connect(self._on_activated)
        result = d.exec_()
        if result == QDialog.Accepted:
            self._activated = True
        else:
            # Nếu người dùng cố gắng tắt app mà chưa kích hoạt key → hiển thị lại dialog
            if not self._activated:
                QTimer.singleShot(1000, self._license)

    def _on_activated(self):
        self._activated = True
        self._sr.setText(
            "✅  Hạn sử dụng: Vĩnh Viễn   ·   Version 13.3.26   ·   Zalo 0327974700")
        self._sr.setStyleSheet(
            "color:#a6e3a1;font-weight:bold;font-size:12px;"
            "padding-right:12px;background:transparent;")

    def _update(self):
        QMessageBox.information(self, "Cập nhật", "✅ Phiên bản mới nhất!\n\nVersion 13.3.26")


# ═══════════════════════════════════════════════════════════════════════════════
#  ENTRY POINT
# ═══════════════════════════════════════════════════════════════════════════════
def main():
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

    app = QApplication(sys.argv)
    app.setApplicationName("Tiến Khoa")
    app.setQuitOnLastWindowClosed(False)
    mw = MainWindow()
    mw.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()