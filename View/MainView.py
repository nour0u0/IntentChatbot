
from PyQt6.QtWidgets import QMainWindow, QTabWidget
from PyQt6.QtCore import Qt

from Service.ChatService import ChatService
from Service.RegisterService import RegisterService

from View.ChatView import ChatView
from View.RegisterView import RegisterView
from View.QuestionsView import QuestionsView
from PyQt6.QtGui import QIcon
from pathlib import Path

class MainView(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Intent Chatbot")
        self.resize(850, 650)
        self.setMinimumSize(850, 650)
        self.setWindowIcon(
            QIcon(str(Path(__file__).resolve().parent.parent / "bot.png"))
        )
        self.chat_service = ChatService(threshold=0.60)
        self.register_service = RegisterService()

        self.tabs = QTabWidget()
        self.tabs.setObjectName("MainTabs")
        self.tabs.setDocumentMode(True)
        self.tabs.setMovable(False)
        self.tabs.setTabPosition(QTabWidget.TabPosition.North)

        self.chat_view = ChatView(self.chat_service)
        self.register_view = RegisterView(self.register_service)
        self.questions_view = QuestionsView(self.chat_service)

        self.tabs.addTab(self.chat_view, "  Chat Room  ")
        self.tabs.addTab(self.register_view, "  Register Q&A  ")
        self.tabs.addTab(self.questions_view, "  Questions & Answers  ")

        self.tabs.currentChanged.connect(self.on_tab_changed)

        self.setCentralWidget(self.tabs)
        self.apply_style()

    def apply_style(self):
        self.setStyleSheet("""
            QMainWindow {
                background-color: #101827;
                color: #E5EAF3;
            }

            QTabWidget#MainTabs::pane {
                background-color: #101827;
                border: 1px solid #263449;
                border-top: none;
                border-bottom-left-radius: 10px;
                border-bottom-right-radius: 10px;
            }

            QTabWidget#MainTabs::tab-bar {
                left: 12px;
            }

            QTabBar::tab {
                background-color: #172235;
                color: #9AAAC0;
                padding: 13px 20px;
                margin-right: 5px;
                border: 1px solid #263449;
                border-bottom: none;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
                font-size: 13px;
                font-weight: 600;
                min-width: 110px;
            }

            QTabBar::tab:hover {
                background-color: #202F45;
                color: #E5EAF3;
            }

            QTabBar::tab:selected {
                background-color: #233754;
                color: #60A5FA;
                border-color: #3478C7;
                border-bottom: 2px solid #3B82F6;
            }

            QTabBar::tab:!selected {
                margin-top: 4px;
            }

            QWidget {
                color: #E5EAF3;
            }

            QToolTip {
                background-color: #1E293B;
                color: #F1F5F9;
                border: 1px solid #3B82F6;
                padding: 5px;
            }
        """)

    def on_tab_changed(self, index):
        if self.tabs.widget(index) is self.questions_view:
            self.questions_view.refresh()
