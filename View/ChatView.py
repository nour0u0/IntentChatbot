
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTextBrowser,
    QLineEdit, QPushButton, QLabel, QDoubleSpinBox,
    QFrame, QSizePolicy
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QTextCursor
from html import escape

class ChatView(QWidget):
    def __init__(self, chat_service):
        super().__init__()
        self.chat_service = chat_service

        self.setObjectName("ChatView")
        self.setStyleSheet("""
            QWidget#ChatView {
                background-color: #101827;
                color: #E5E7EB;
                font-family: 'Segoe UI';
                font-size: 10pt;
            }

            QLabel {
                color: #AAB6C8;
            }

            QLabel#Title {
                color: #F8FAFC;
                font-size: 20pt;
                font-weight: 700;
            }

            QLabel#Subtitle {
                color: #8492A6;
                font-size: 9pt;
            }

            QFrame#Toolbar, QFrame#Composer {
                background-color: #182438;
                border: 1px solid #29374D;
                border-radius: 12px;
            }

            QTextBrowser {
                background-color: #101827;
                color: #E5E7EB;
                border: none;
                padding: 12px;
                selection-background-color: #315C96;
            }

            QLineEdit {
                background-color: #0F1929;
                color: #F1F5F9;
                border: 1px solid #34445D;
                border-radius: 9px;
                padding: 12px;
                selection-background-color: #315C96;
            }

            QLineEdit:focus {
                border: 1px solid #60A5FA;
            }

            QDoubleSpinBox {
                background-color: #0F1929;
                color: #F1F5F9;
                border: 1px solid #34445D;
                border-radius: 7px;
                padding: 6px;
                min-width: 90px;
            }

            QPushButton {
                background-color: #3478F6;
                color: white;
                border: none;
                border-radius: 9px;
                padding: 10px 18px;
                font-weight: 600;
            }

            QPushButton:hover {
                background-color: #4C8DFF;
            }

            QPushButton:pressed {
                background-color: #245CC4;
            }

            QPushButton:disabled {
                background-color: #34445D;
                color: #8492A6;
            }
        """)

        root = QVBoxLayout(self)
        root.setContentsMargins(22, 20, 22, 20)
        root.setSpacing(16)

        # Header
        header = QVBoxLayout()
        header.setSpacing(4)

        title = QLabel("ChatRoom")
        title.setObjectName("Title")

        subtitle = QLabel(
            "Local AI · Semantic retrieval · Private on-device processing"
        )
        subtitle.setObjectName("Subtitle")

        header.addWidget(title)
        header.addWidget(subtitle)
        root.addLayout(header)

        # Threshold toolbar
        toolbar = QFrame()
        toolbar.setObjectName("Toolbar")

        toolbar_layout = QHBoxLayout(toolbar)
        toolbar_layout.setContentsMargins(16, 10, 16, 10)

        threshold_label = QLabel("Similarity threshold")

        self.threshold_input = QDoubleSpinBox()
        self.threshold_input.setRange(-1.0, 1.0)
        self.threshold_input.setSingleStep(0.05)
        self.threshold_input.setDecimals(2)
        self.threshold_input.setValue(chat_service.threshold)

        self.threshold_status = QLabel()
        self.threshold_status.setAlignment(
            Qt.AlignmentFlag.AlignRight |
            Qt.AlignmentFlag.AlignVCenter
        )

        self.threshold_input.valueChanged.connect(
            self.update_threshold_status
        )
        self.update_threshold_status(self.threshold_input.value())

        toolbar_layout.addWidget(threshold_label)
        toolbar_layout.addWidget(self.threshold_input)
        toolbar_layout.addStretch()
        toolbar_layout.addWidget(self.threshold_status)

        root.addWidget(toolbar)

        # Conversation area
        self.conversation = QTextBrowser()
        self.conversation.setOpenExternalLinks(False)
        self.conversation.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding
        )

        self.conversation.setHtml("""
            <html>
            <body style="font-family:'Segoe UI'; color:#8492A6;">
                <div style="text-align:center; margin-top:100px;">
                    <div style="font-size:32px;">✦</div>
                    <h2 style="color:#E5E7EB;">Welcome to your assistant</h2>
                    <p>Register answers and question  and start conversation.</p>
                </div>
            </body>
            </html>
        """)

        root.addWidget(self.conversation, 1)

        # Message composer
        composer = QFrame()
        composer.setObjectName("Composer")

        composer_layout = QHBoxLayout(composer)
        composer_layout.setContentsMargins(10, 10, 10, 10)
        composer_layout.setSpacing(10)

        self.prompt_input = QLineEdit()
        self.prompt_input.setPlaceholderText(
            "Ask about crops, irrigation, soil, or farming..."
        )
        self.prompt_input.returnPressed.connect(self.send_message)

        self.send_button = QPushButton("Send  ➤")
        self.send_button.setMinimumWidth(105)
        self.send_button.clicked.connect(self.send_message)

        composer_layout.addWidget(self.prompt_input, 1)
        composer_layout.addWidget(self.send_button)

        root.addWidget(composer)

    def update_threshold_status(self, value):
        self.threshold_status.setText(
            f"Acceptance score ≥ {value:.2f}"
        )

    def add_message(self, sender, message, color, metadata=None):
        cursor = self.conversation.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)

  

        safe_message = escape(str(message)).replace("\n", "<br>")
        safe_sender = escape(sender)
        safe_metadata = escape(metadata or "")

        # Different frame backgrounds for each message type.
        if sender == "YOU":
            background = "#1C3554"
            border_color = "#60A5FA"
            alignment = "right"
            label = "YOU"
        elif sender == "ASSISTANT":
            background = "#183A32"
            border_color = "#34D399"
            alignment = "left"
            label = "ASSISTANT"
        else:
            background = "#3B202B"
            border_color = "#F87171"
            alignment = "left"
            label = safe_sender

        html = f"""
            <table width="100%" cellspacing="0" cellpadding="0"
                style="margin-top:12px; margin-bottom:12px;">
                <tr>
                    <td align="{alignment}">
                        <table cellspacing="0" cellpadding="0"
                            style="
                                background-color:{background};
                                border:1px solid {border_color};
                                border-radius:10px;
                            ">
                            <tr>
                                <td style="
                                    padding:14px;
                                    background-color:{background};
                                ">
                                    <div style="
                                        color:{border_color};
                                        font-size:10pt;
                                        font-weight:bold;
                                        margin-bottom:8px;
                                    ">{label}</div>

                                    <div style="
                                        color:#E5EAF3;
                                        font-size:10pt;
                                    ">{safe_message}</div>

                                    <div style="
                                        color:#AAB6C8;
                                        font-size:8pt;
                                        margin-top:8px;
                                    ">{safe_metadata}</div>
                                </td>
                            </tr>
                        </table>
                    </td>
                </tr>
            </table>
        """

        cursor.insertHtml(html)
        cursor.insertBlock()
        self.conversation.setTextCursor(cursor)
        self.conversation.ensureCursorVisible()
    def send_message(self):
        prompt = self.prompt_input.text().strip()

        if not prompt:
            return

        self.chat_service.threshold = self.threshold_input.value()

        self.add_message("YOU", prompt, "#60A5FA")

        self.prompt_input.clear()
        self.send_button.setEnabled(False)
        self.send_button.setText("Thinking...")

        try:
            result = self.chat_service.respond(prompt)

            if result is None:
                self.add_message(
                    "ASSISTANT",
                    "I couldn't find a matching answer.",
                    "#F59E0B",
                    f"Threshold: {self.chat_service.threshold:.2f}"
                )
            else:
                self.add_message(
                    "ASSISTANT",
                    result["answer"],
                    "#34D399",
                    (
                        f"Similarity: {result['similarity']:.3f}"
                        f"  ·  Threshold: {self.chat_service.threshold:.2f}"
                        f"  ·  Question ID: {result['question_id']}"
                    )
                )

        except Exception as error:
            self.add_message(
                "ERROR",
                str(error),
                "#F87171"
            )

        finally:
            self.send_button.setEnabled(True)
            self.send_button.setText("Send  ➤")
            self.prompt_input.setFocus()
