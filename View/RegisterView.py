
from pathlib import Path

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QLineEdit, QFileDialog, QMessageBox,
    QFrame, QSizePolicy
)
from PyQt6.QtCore import Qt


DARK_STYLE = """
    QWidget {
        background-color: #101827;
        color: #E5EAF3;
        font-size: 13px;
    }

QLabel {
        background-color: #141F30;
        color: #94A3B8;
        padding: 7px;
    }

QLineEdit {
    background-color: #141F30;
    color: #E5EAF3;
    border: 1px solid #34445C;
    border-radius: 7px;
    padding: 11px;
    selection-background-color: #3478C7;
}

    QLineEdit:focus {
        border: 1px solid #3B82F6;
    }

    QPushButton {
        background-color: #233754;
        color: #E5EAF3;
        border: 1px solid #344B6A;
        border-radius: 7px;
        padding: 10px 17px;
        font-weight: 600;
    }

    QPushButton:hover {
        background-color: #2E4A70;
        border-color: #3B82F6;
    }

    QPushButton:pressed {
        background-color: #1D2D45;
    }

    QPushButton:disabled {
        background-color: #263449;
        color: #64748B;
        border-color: #263449;
    }

    QToolTip {
        background-color: #1E293B;
        color: #F1F5F9;
        border: 1px solid #3B82F6;
        padding: 5px;
    }
"""


class RegisterView(QWidget):
    def __init__(self, register_service):
        super().__init__()

        self.register_service = register_service
        self.setStyleSheet(DARK_STYLE)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(28, 28, 28, 28)
        layout.setSpacing(18)

        # Header
        title = QLabel("Register Knowledge")
        title.setStyleSheet("""
            QLabel {
                color: #E5EAF3;
                font-size: 24px;
                font-weight: 700;
            }
        """)
        layout.addWidget(title)

        subtitle = QLabel(
            "Import questions and answers into your local chatbot."
        )
        subtitle.setStyleSheet("""
            QLabel {
                color: #94A3B8;
                font-size: 14px;
            }
        """)
        layout.addWidget(subtitle)

        # Main registration card
        card = QFrame()
        card.setObjectName("RegisterCard")
        card.setStyleSheet("""
            QFrame#RegisterCard {
                background-color: #141F30;
                border: 1px solid #263449;
                border-radius: 12px;
            }
        """)

        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(24, 24, 24, 24)
        card_layout.setSpacing(18)

        section_title = QLabel("Import a JSON dataset")
        section_title.setStyleSheet("""
            QLabel {
                color: #60A5FA;
                font-size: 17px;
                font-weight: 700;
            }
        """)
        card_layout.addWidget(section_title)

        description = QLabel(
            "Choose a JSON file containing one question/answer object "
            "or a list of objects. Your registration service will "
            "process the entries and generate question embeddings."
        )
        description.setWordWrap(True)
        description.setStyleSheet("color: #94A3B8;")
        card_layout.addWidget(description)

        file_label = QLabel("JSON file")
        file_label.setStyleSheet("font-weight: 600;")
        card_layout.addWidget(file_label)

        file_layout = QHBoxLayout()
        file_layout.setSpacing(10)

        self.file_input = QLineEdit()
        self.file_input.setMinimumHeight(42)
        self.file_input.setPlaceholderText(
            "Select a JSON file..."
        )
        self.file_input.setClearButtonEnabled(True)

        browse_button = QPushButton("Browse")
        browse_button.setMinimumHeight(42)
        browse_button.setMinimumWidth(105)
        browse_button.clicked.connect(self.browse_file)

        file_layout.addWidget(self.file_input, 1)
        file_layout.addWidget(browse_button)

        card_layout.addLayout(file_layout)

        # Register button
        self.register_button = QPushButton("Register Questions")
        self.register_button.setMinimumHeight(46)
        self.register_button.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Fixed
        )
        self.register_button.setStyleSheet("""
            QPushButton {
                background-color: #2563EB;
                color: white;
                border: 1px solid #3B82F6;
                border-radius: 8px;
                padding: 12px;
                font-size: 14px;
                font-weight: 700;
            }
            QPushButton:hover {
                background-color: #1D4ED8;
            }
            QPushButton:pressed {
                background-color: #1E40AF;
            }
            QPushButton:disabled {
                background-color: #263449;
                color: #64748B;
                border-color: #263449;
            }
        """)
        self.register_button.clicked.connect(self.register)
        card_layout.addWidget(self.register_button)

        layout.addWidget(card)

        # Status section
        status_title = QLabel("Registration status")
        status_title.setStyleSheet("""
            QLabel {
                color: #CBD5E1;
                font-weight: 700;
            }
        """)
        layout.addWidget(status_title)

        self.status_label = QLabel(
            "Select a JSON file to begin."
        )
        self.status_label.setWordWrap(True)
        self.status_label.setMinimumHeight(45)
        self.status_label.setAlignment(
            Qt.AlignmentFlag.AlignLeft |
            Qt.AlignmentFlag.AlignVCenter
        )
        self.status_label.setStyleSheet("""
    QLabel {
        background-color: #141F30;
        color: #94A3B8;
        border: 1px solid #263449;
        border-radius: 7px;
        padding: 12px;
    }
""")
        layout.addWidget(self.status_label)

        layout.addStretch()

    def browse_file(self):
        path, _ = QFileDialog.getOpenFileName(
            self,
            "Select question/answer JSON",
            "",
            "JSON Files (*.json)"
        )

        if path:
            self.file_input.setText(path)
            self.status_label.setText(
                f"Selected file: {Path(path).name}"
            )
            self.status_label.setStyleSheet("""
                QLabel {
                    color: #93C5FD;
                    border: 1px solid #263D5B;
                    border-radius: 7px;
                    padding: 12px;
                }
            """)

    def register(self):
        path = self.file_input.text().strip()

        if not path:
            QMessageBox.warning(
                self,
                "Missing file",
                "Select a JSON file first."
            )
            return

        if not Path(path).is_file():
            QMessageBox.warning(
                self,
                "File not found",
                "The selected file does not exist. Please select it again."
            )
            return

        self.register_button.setEnabled(False)
        self.register_button.setText("Registering...")
        self.status_label.setText(
            "Processing questions and generating embeddings..."
        )
        self.status_label.setStyleSheet("""
            QLabel {

                color: #93C5FD;
                border: 1px solid #263D5B;
                border-radius: 7px;
                padding: 12px;
            }
        """)

        try:
            results = self.register_service.register(path)

            # Support a service returning either one result or a list.
            if isinstance(results, dict):
                results = [results]

            if not results:
                raise ValueError(
                    "The registration service returned no results."
                )

            count = len(results)

            self.status_label.setText(
                f"Registration completed successfully. "
                f"{count} question(s) registered."
            )
            self.status_label.setStyleSheet("""
                QLabel {
                    color: #86EFAC;
                    border: 1px solid #28634B;
                    border-radius: 7px;
                    padding: 12px;
                }
            """)

            # Show a short summary rather than displaying an entire dataset.
            summary_lines = [
                f"Successfully registered {count} question(s).",
                ""
            ]

            for result in results[:5]:
                question_id = result.get("question_id", "N/A")
                question = result.get("question", "(No question)")
                summary_lines.append(
                    f"ID {question_id}: {question}"
                )

            if count > 5:
                summary_lines.append(
                    f"\n...and {count - 5} more question(s)."
                )

            QMessageBox.information(
                self,
                "Registration successful",
                "\n".join(summary_lines)
            )

        except Exception as error:
            self.status_label.setText(
                f"Registration failed: {error}"
            )
            self.status_label.setStyleSheet("""
                QLabel {
                    background-color: #3B202B;
                    color: #FCA5A5;
                    border: 1px solid #713440;
                    border-radius: 7px;
                    padding: 12px;
                }
            """)

            QMessageBox.critical(
                self,
                "Registration error",
                str(error)
            )

        finally:
            self.register_button.setEnabled(True)
            self.register_button.setText("Register Questions")
