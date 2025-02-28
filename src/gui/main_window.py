from PyQt5.QtCore import Qt, QTimer, QRegExp
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QTextEdit
from PyQt5.QtGui import QRegExpValidator
from core.database import DictionaryDB
from typing import Optional, List, Dict
import re


class MainWindow(QWidget):
    def __init__(self):
        # 初始化MainWindow，设置UI和关闭行为
        super().__init__()
        self.init_ui()
        self.setup_close_behavior()
        self.db = DictionaryDB()
        self.search_timer = QTimer()
        self.search_timer.setSingleShot(True)
        self.search_timer.timeout.connect(self._perform_search)

    def setup_close_behavior(self):
        # 设置关闭行为为隐藏窗口而不是关闭
        self.closeEvent = lambda event: self.hide()

    def init_ui(self):
        # 初始化用户界面
        self.setWindowTitle("QuickLex")
        self.setGeometry(600, 200, 1000, 1000)

        self.input_box = QLineEdit()
        self.result_area = QTextEdit()
        self.result_area.setReadOnly(True)

        layout = QVBoxLayout()
        self.input_box.setPlaceholderText("input word")
        layout.addWidget(self.input_box)
        layout.addWidget(self.result_area)
        self.setLayout(layout)

        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)

        self.input_box.setValidator(QRegExpValidator(QRegExp("[a-zA-Z ]*")))
        self.input_box.textChanged.connect(self.on_text_changed)

    def on_text_changed(self, text):
        self.search_timer.stop()
        if text.strip():
            self.result_area.setText("搜索中...")
            self.search_timer.start(200)
        else:
            self.result_area.clear()

    def _perform_search(self):
        query_text = self.input_box.text().strip().lower()
        results = self.db.fuzzy_query(query_text)
        self.display_results(results)

    def display_results(self, results: Optional[List[Dict]]):
        if not results:
            self.result_area.setText("未找到该单词")
            return

        result_text = ""
        keyword = self.input_box.text().strip()

        # 创建正则表达式，忽略大小写
        keyword_regex = re.compile(re.escape(keyword), re.IGNORECASE)

        for idx, item in enumerate(results, 1):
            word = item.get("word", "")
            phonetic = item.get("phonetic", "")
            definition = item.get("definition", "")
            translation = item.get("translation", "")

            # 使用正则表达式替换关键字
            formatted_word = keyword_regex.sub(
                r'<span style="color: #FF6600;">\g<0></span>', word
            )
            formatted_phonetic = keyword_regex.sub(
                r'<span style="color: #FF6600;">\g<0></span>', phonetic
            )
            formatted_definition = keyword_regex.sub(
                r'<span style="color: #FF6600;">\g<0></span>', definition
            )
            formatted_translation = keyword_regex.sub(
                r'<span style="color: #FF6600;">\g<0></span>', translation
            )

            result_text += f"""
            <p><strong>{formatted_word}</strong> {phonetic}</p>
            <p>{formatted_definition}</p>
            <p>{formatted_translation}</p>
            """
            if phonetic:
                result_text = result_text.replace(phonetic, f"[{phonetic}]")

        self.result_area.setHtml(result_text)

    def toggle_visibility(self):
        # 切换窗口的可见性，显示或隐藏窗口
        if self.isVisible():
            self.hide()
        else:
            self.showNormal()
            self.activateWindow()
            self.raise_()
            self.input_box.setFocus()
