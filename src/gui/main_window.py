from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPainterPath, QPainter, QColor
from core.database import DictionaryDB
from typing import Optional, List, Dict
from .ui_main_window import Ui_DictionaryWidget
import re


class MainWindow(QWidget, Ui_DictionaryWidget):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # 样式设置
        with open("resources/style/main_window.css", encoding="utf-8") as f:
            self.setStyleSheet(f.read())

        # 窗口初始化
        self.init_window()
        self.init_behavior()

        # 数据库与定时器
        self.db = DictionaryDB()
        self.search_timer = QTimer()
        self.search_timer.setSingleShot(True)
        self.search_timer.timeout.connect(self.perform_search)

    def init_window(self):
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setFixedWidth(800)

        # 高度控制参数
        self.collapsed_height = 100
        self.expanded_height = QApplication.desktop().availableGeometry().height() - 100
        self.setMinimumHeight(self.collapsed_height)

        # 初始位置
        screen = QApplication.primaryScreen().geometry()
        self.move(screen.width() - self.width() - 20, 60)

        # 输入框配置
        self.searchInput.setPlaceholderText("Search word...")
        self.searchInput.textChanged.connect(self.on_text_changed)
        self.searchInput.setClearButtonEnabled(True)

        # 滚动区域优化
        self.resultsLayout.setContentsMargins(0, 5, 0, 5)
        self.resultsLayout.setSpacing(8)
        self.resultScrollArea.setVisible(False)

    def init_behavior(self):
        # 动画系统
        self.size_anim = QPropertyAnimation(self, b"size")
        self.size_anim.setDuration(200)

        # 关闭行为
        self.closeEvent = lambda e: self.hide()

    def on_text_changed(self, text):
        self.search_timer.stop()
        self.clean_old_results()
        if text.strip():
            self.search_timer.start(180)
        else:
            self.resultScrollArea.setVisible(False)
        self.adjust_window_height()

    def perform_search(self):
        query = self.searchInput.text().strip().lower()
        if query:
            results = self.db.fuzzy_query(query)
            self.display_results(results or [])
        else:
            self.clean_old_results()
            self.resultScrollArea.setVisible(False)

    def clean_old_results(self):
        # 清除旧结果
        while self.resultsLayout.count():
            if widget := self.resultsLayout.takeAt(0).widget():
                widget.deleteLater()

        self.scrollContent.updateGeometry()
        QApplication.processEvents(QEventLoop.ExcludeUserInputEvents)

    def display_results(self, results: List[Dict]):
        self.clean_old_results()

        # 处理空结果
        if not results:
            self.add_result_item("Word not found", "#999")
            self.add_result_item("", "#999")
            return

        # 添加新结果
        keyword = re.compile(re.escape(self.searchInput.text().strip()), re.IGNORECASE)
        for item in results:
            self.add_dictionary_item(item, keyword)

        self.adjust_window_height()
        self.resultScrollArea.setVisible(True)

    def create_label(self, text, color):
        label = QLabel(text)
        label.setWordWrap(True)
        label.setStyleSheet(
            f"""
        color: {color};
        margin: 2px 0;
        font-size: 40px;
        """
        )
        return label

    def add_dictionary_item(self, item: Dict, highlight_pattern):
        widget = QWidget()
        layout = QVBoxLayout(widget)

        # 单词行
        word = self.highlight_text(item.get("word", ""), highlight_pattern)
        phonetic = f'<span style="color:#666">[{item.get("phonetic", "")}]</span>'
        if item.get("phonetic", ""):
            layout.addWidget(self.create_label(f"{word} {phonetic}", "#333"))
        else:
            layout.addWidget(self.create_label(f"{word}", "#333"))
        # 释义
        definition = self.highlight_text(item.get("definition", ""), highlight_pattern)
        if definition:
            layout.addWidget(self.create_label(definition, "#555"))

        # 翻译
        translation = self.highlight_text(
            item.get("translation", ""), highlight_pattern
        )
        if translation:
            layout.addWidget(self.create_label(translation, "#777"))

        self.resultsLayout.addWidget(widget)

    def highlight_text(self, text: str, pattern):
        return pattern.sub(
            r'<span style="color: #FF6600; font-weight:600">\g<0></span>', text
        )

    def adjust_window_height(self):
        self.scrollContent.updateGeometry()
        self.resultsLayout.activate()
        QApplication.processEvents(QEventLoop.ExcludeUserInputEvents)

        content_height = (
            self.scrollContent.sizeHint().height() + self.searchInput.height()
        )
        target_height = min(
            max(content_height, self.collapsed_height), self.expanded_height
        )

        if abs(self.height() - target_height) < 10:
            return

        if self.size_anim.state == QPropertyAnimation.Running:
            self.size_anim.stop()
        self.size_anim.setStartValue(QSize(self.width(), self.height()))
        self.size_anim.setEndValue(QSize(self.width(), target_height))
        self.size_anim.start()

    def add_result_item(self, text: str, color: str):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.addWidget(self.create_label(text, color))
        self.resultsLayout.addWidget(widget)
        self.adjust_window_height()
        self.resultScrollArea.setVisible(True)

    def toggle_visibility(self):
        if self.isVisible():
            self.hide()
        else:
            self.showNormal()
            self.activateWindow()
            self.raise_()
            self.searchInput.setFocus()

    # 窗口拖动功能
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_pos = event.globalPos() - self.pos()

    def mouseMoveEvent(self, event):
        if hasattr(self, "drag_pos"):
            self.move(event.globalPos() - self.drag_pos)

    def mouseReleaseEvent(self, event):
        if hasattr(self, "drag_pos"):
            del self.drag_pos

    # 圆角绘制
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        path = QPainterPath()
        path.addRoundedRect(QRectF(self.rect()).adjusted(1, 1, -1, -1), 15, 15)

        # 背景绘制
        painter.fillPath(path, QColor(255, 255, 255, 245))

        # 边框阴影
        painter.setPen(QColor(0, 0, 0, 30))
        painter.drawPath(path)
