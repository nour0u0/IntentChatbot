
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTableWidget,
    QTableWidgetItem, QPushButton, QLabel, QMessageBox,
    QDialog, QFormLayout, QLineEdit, QTextEdit,
    QDialogButtonBox, QHeaderView
)
from PyQt6.QtCore import Qt

from Model.Question import Question
from Model.AnswerEmbed import AnswerEmbed


DARK_STYLE = """
    QWidget {
        background-color: #101827;
        color: #E5EAF3;
        font-size: 13px;
    }

    QLabel {
        color: #CBD5E1;
        padding: 4px 0;
    }

    QLineEdit, QTextEdit {
        background-color: #172235;
        color: #E5EAF3;
        border: 1px solid #34445C;
        border-radius: 7px;
        padding: 9px;
        selection-background-color: #3478C7;
    }

    QLineEdit:focus, QTextEdit:focus {
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

    QTableWidget {
        background-color: #141F30;
        alternate-background-color: #19263A;
        color: #E5EAF3;
        border: 1px solid #263449;
        border-radius: 8px;
        gridline-color: #263449;
        selection-background-color: #294B73;
        selection-color: #FFFFFF;
        outline: none;
    }

    QTableWidget::item {
        padding: 8px;
        border-bottom: 1px solid #263449;
    }

    QHeaderView::section {
        background-color: #1E2C41;
        color: #93C5FD;
        padding: 10px 8px;
        border: none;
        border-bottom: 1px solid #344B6A;
        font-weight: 600;
    }

    QScrollBar:vertical {
        background-color: #141F30;
        width: 10px;
        margin: 0;
    }

    QScrollBar::handle:vertical {
        background-color: #34445C;
        border-radius: 4px;
        min-height: 25px;
    }

    QScrollBar::handle:vertical:hover {
        background-color: #4B6382;
    }

    QScrollBar::add-line:vertical,
    QScrollBar::sub-line:vertical {
        height: 0;
    }

    QScrollBar:horizontal {
        background-color: #141F30;
        height: 10px;
        margin: 0;
    }

    QScrollBar::handle:horizontal {
        background-color: #34445C;
        border-radius: 4px;
        min-width: 25px;
    }

    QScrollBar::add-line:horizontal,
    QScrollBar::sub-line:horizontal {
        width: 0;
    }

    QDialog {
        background-color: #101827;
    }

    QDialogButtonBox QPushButton {
        min-width: 85px;
    }

    QToolTip {
        background-color: #1E293B;
        color: #F1F5F9;
        border: 1px solid #3B82F6;
        padding: 5px;
    }
"""


class EditQuestionDialog(QDialog):
    def __init__(self, question_text, answer_text, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Edit Question and Answer")
        self.resize(550, 400)
        self.setMinimumSize(450, 320)
        self.setStyleSheet(DARK_STYLE)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(22, 22, 22, 22)
        layout.setSpacing(16)

        title = QLabel("Edit knowledge entry")
        title.setStyleSheet("""
            QLabel {
                color: #60A5FA;
                font-size: 19px;
                font-weight: 700;
            }
        """)
        layout.addWidget(title)

        subtitle = QLabel(
            "Update the question or answer. "
            "The question embedding will be regenerated."
        )
        subtitle.setWordWrap(True)
        subtitle.setStyleSheet("color: #94A3B8;")
        layout.addWidget(subtitle)

        form = QFormLayout()
        form.setSpacing(12)
        form.setLabelAlignment(
            Qt.AlignmentFlag.AlignLeft |
            Qt.AlignmentFlag.AlignVCenter
        )

        self.question_input = QLineEdit(question_text)
        self.question_input.setMinimumHeight(38)
        self.question_input.setPlaceholderText("Enter the question...")

        self.answer_input = QTextEdit()
        self.answer_input.setPlainText(answer_text)
        self.answer_input.setPlaceholderText("Enter the answer...")
        self.answer_input.setMinimumHeight(150)

        form.addRow("Question", self.question_input)
        form.addRow("Answer", self.answer_input)

        layout.addLayout(form)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Save |
            QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        save_button = buttons.button(
            QDialogButtonBox.StandardButton.Save
        )
        if save_button:
            save_button.setText("Save Changes")
            save_button.setStyleSheet("""
                QPushButton {
                    background-color: #2563EB;
                    border: 1px solid #3B82F6;
                    color: white;
                }
                QPushButton:hover {
                    background-color: #1D4ED8;
                }
            """)

        layout.addWidget(buttons)

    def get_values(self):
        return (
            self.question_input.text().strip(),
            self.answer_input.toPlainText().strip()
        )


class QuestionsView(QWidget):
    def __init__(self, chat_service):
        super().__init__()

        self.chat_service = chat_service
        self.setStyleSheet(DARK_STYLE)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(22, 22, 22, 22)
        layout.setSpacing(16)

        # Header
        header_layout = QHBoxLayout()

        title_layout = QVBoxLayout()

        title = QLabel("Knowledge Base")
        title.setStyleSheet("""
            QLabel {
                color: #E5EAF3;
                font-size: 22px;
                font-weight: 700;
            }
        """)

        subtitle = QLabel(
            "Browse, edit, and manage the chatbot's registered knowledge."
        )
        subtitle.setStyleSheet("color: #94A3B8;")

        title_layout.addWidget(title)
        title_layout.addWidget(subtitle)
        header_layout.addLayout(title_layout)
        header_layout.addStretch()

        layout.addLayout(header_layout)

        # Similarity threshold information
        self.threshold_label = QLabel()
        self.threshold_label.setStyleSheet("""
            QLabel {
                background-color: #172235;
                color: #93C5FD;
                border: 1px solid #263D5B;
                border-radius: 7px;
                padding: 10px 12px;
                font-weight: 600;
            }
        """)
        layout.addWidget(self.threshold_label)

        # Questions table
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(
            ["Question ID", "Question", "Answer"]
        )

        self.table.setEditTriggers(
            QTableWidget.EditTrigger.NoEditTriggers
        )
        self.table.setSelectionBehavior(
            QTableWidget.SelectionBehavior.SelectRows
        )
        self.table.setSelectionMode(
            QTableWidget.SelectionMode.SingleSelection
        )
        self.table.setAlternatingRowColors(True)
        self.table.setShowGrid(True)
        self.table.verticalHeader().setVisible(False)
        self.table.verticalHeader().setDefaultSectionSize(42)

        header = self.table.horizontalHeader()
        header.setSectionResizeMode(
            0, QHeaderView.ResizeMode.ResizeToContents
        )
        header.setSectionResizeMode(
            1, QHeaderView.ResizeMode.Interactive
        )
        header.setSectionResizeMode(
            2, QHeaderView.ResizeMode.Stretch
        )
        self.table.setColumnWidth(1, 300)

        layout.addWidget(self.table, 1)

        # Action buttons
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(10)

        refresh_button = QPushButton("⟳  Refresh")
        edit_button = QPushButton("✎  Edit Selected")
        delete_button = QPushButton("⌫  Delete Selected")

        refresh_button.setToolTip("Reload questions from the database")
        edit_button.setToolTip("Edit the selected question and answer")
        delete_button.setToolTip("Delete the selected question and answer")

        refresh_button.clicked.connect(self.refresh)
        edit_button.clicked.connect(self.edit_selected)
        delete_button.clicked.connect(self.delete_selected)

        delete_button.setStyleSheet("""
            QPushButton {
                background-color: #3B202B;
                color: #FCA5A5;
                border: 1px solid #713440;
                border-radius: 7px;
                padding: 10px 17px;
                font-weight: 600;
            }
            QPushButton:hover {
                background-color: #542631;
                border-color: #EF4444;
            }
        """)

        buttons_layout.addWidget(refresh_button)
        buttons_layout.addStretch()
        buttons_layout.addWidget(edit_button)
        buttons_layout.addWidget(delete_button)

        layout.addLayout(buttons_layout)

        self.refresh()

    def refresh(self):
        self.threshold_label.setText(
            f"Acceptance threshold: "
            f"{self.chat_service.threshold:.2f}"
        )

        questions = Question._load_all()
        self.table.setRowCount(len(questions))

        for row, record in enumerate(questions):
            question_id = record["QuestionId"]
            question_text = record["Text"]

            answer = AnswerEmbed.get(question_id)
            answer_text = (
                answer.Text if answer
                else "(No answer registered)"
            )

            values = [
                str(question_id),
                question_text,
                answer_text
            ]

            for column, value in enumerate(values):
                item = QTableWidgetItem(str(value))
                item.setToolTip(str(value))

                if column == 0:
                    item.setTextAlignment(
                        Qt.AlignmentFlag.AlignCenter
                    )

                self.table.setItem(row, column, item)

        self.table.clearSelection()

    def _selected_question_id(self):
        row = self.table.currentRow()

        if row < 0 or self.table.item(row, 0) is None:
            QMessageBox.warning(
                self,
                "No selection",
                "Please select a question first."
            )
            return None

        return int(self.table.item(row, 0).text())

    def edit_selected(self):
        question_id = self._selected_question_id()

        if question_id is None:
            return

        question = Question.get(question_id)
        answer = AnswerEmbed.get(question_id)

        if question is None:
            QMessageBox.warning(
                self,
                "Not found",
                "The question no longer exists."
            )
            self.refresh()
            return

        answer_text = answer.Text if answer else ""

        dialog = EditQuestionDialog(
            question.Text,
            answer_text,
            self
        )

        if dialog.exec() != QDialog.DialogCode.Accepted:
            return

        new_question, new_answer = dialog.get_values()

        if not new_question or not new_answer:
            QMessageBox.warning(
                self,
                "Invalid input",
                "Both question and answer must be non-empty."
            )
            return

        try:
            embedding = self.chat_service.model.encode(
                new_question,
                convert_to_numpy=True,
                normalize_embeddings=True
            )

            question.Text = new_question
            question.save()

            AnswerEmbed(
                question_id,
                new_answer,
                embedding
            ).save()

            self.refresh()

            QMessageBox.information(
                self,
                "Updated",
                "Question, answer, and embedding updated successfully."
            )

        except Exception as error:
            QMessageBox.critical(
                self,
                "Update error",
                str(error)
            )

    def delete_selected(self):
        question_id = self._selected_question_id()

        if question_id is None:
            return

        question = Question.get(question_id)

        if question is None:
            QMessageBox.warning(
                self,
                "Not found",
                "The question no longer exists."
            )
            self.refresh()
            return

        confirmation = QMessageBox.question(
            self,
            "Confirm deletion",
            f"Delete this question and its answer?\n\n"
            f"{question.Text}\n\n"
            f"This action cannot be undone.",
            QMessageBox.StandardButton.Yes |
            QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )

        if confirmation != QMessageBox.StandardButton.Yes:
            return

        try:
            AnswerEmbed.delete(question_id)
            Question.delete(question_id)

            self.refresh()

            QMessageBox.information(
                self,
                "Deleted",
                f"Question {question_id} and its answer were deleted."
            )

        except Exception as error:
            QMessageBox.critical(
                self,
                "Deletion error",
                str(error)
            )
