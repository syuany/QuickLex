from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_DictionaryWidget(object):
    def setupUi(self, DictionaryWidget):
        DictionaryWidget.setObjectName("DictionaryWidget")
        DictionaryWidget.resize(300, 60)

        # 主布局直接设置到窗口
        self.verticalLayout = QtWidgets.QVBoxLayout(DictionaryWidget)
        self.verticalLayout.setContentsMargins(15, 15, 15, 15)
        self.verticalLayout.setSpacing(8)

        # 自定义样式的输入框
        self.searchInput = QtWidgets.QLineEdit()
        self.searchInput.setMinimumHeight(70)
        self.verticalLayout.addWidget(self.searchInput)

        # 滚动区域容器
        self.resultScrollArea = QtWidgets.QScrollArea()
        self.resultScrollArea.setWidgetResizable(True)
        self.resultScrollArea.setSizeAdjustPolicy(
            QtWidgets.QAbstractScrollArea.AdjustToContents
        )
        self.scrollContent = QtWidgets.QWidget()
        self.resultsLayout = QtWidgets.QVBoxLayout(self.scrollContent)
        self.resultsLayout.setContentsMargins(0, 0, 0, 5)
        self.resultScrollArea.setWidget(self.scrollContent)
        self.verticalLayout.addWidget(self.resultScrollArea)

        self.retranslateUi(DictionaryWidget)

    def retranslateUi(self, DictionaryWidget):
        _translate = QtCore.QCoreApplication.translate
        DictionaryWidget.setWindowTitle(_translate("DictionaryWidget", "QuickLex"))
