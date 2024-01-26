from PyQt5.QtWidgets import (QMainWindow, QPushButton, QHBoxLayout, QVBoxLayout,
                             QWidget, QTextEdit, QLabel, QDialog)
from PyQt5.QtGui import QTextCursor, QColor
from PyQt5.QtCore import pyqtSlot

from openai_api.api_client import OpenAIClient

class ChatDialog(QDialog):
    def __init__(self, parent=None):
        super(ChatDialog, self).__init__(parent)
        self.openai_client = OpenAIClient()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Chat with GPT-4')
        layout = QVBoxLayout(self)

        self.chat_display = QTextEdit(self)
        self.chat_display.setReadOnly(True)
        self.user_input = QTextEdit(self)
        self.user_input.setFixedHeight(50)
        send_button = QPushButton('Send', self)
        send_button.clicked.connect(self.send_message)

        layout.addWidget(self.chat_display)
        layout.addWidget(QLabel("Type your message:"))
        layout.addWidget(self.user_input)
        layout.addWidget(send_button)

    @pyqtSlot()
    def send_message(self):
        user_message = self.user_input.toPlainText().strip()
        if user_message:
            # Append user's message to chat display
            self.append_to_chat(f"You: {user_message}")
            self.user_input.clear()

            # Here you would implement the API call to OpenAI
            # and append the response to the chat.
            # This is a placeholder for the actual implementation.
            response = self.openai_client.query_chat_model('gpt-4-turbo', user_message)
            gpt_response = response.get('choices', [])[0].get('message', {}).get('content', "Error: No response.")
            
            # Append GPT-4's response to chat display
            self.append_to_chat(f"GPT-4: {gpt_response}")

    def append_to_chat(self, message):
        self.chat_display.moveCursor(QTextCursor.End)
        self.chat_display.insertPlainText(message + "\n\n")
        self.chat_display.moveCursor(QTextCursor.End)

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('GPT Assistant GUI')
        self.setGeometry(300, 300, 800, 600)  # Adjust size as needed

        # Central widget and layout
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        main_layout = QHBoxLayout(self.central_widget)  # Horizontal layout for the two sections

        # Left side: GPT 4 Button
        self.gpt_button = QPushButton('GPT 4')
        self.gpt_button.setStyleSheet("QPushButton { color: red; font-weight: bold; font-size: 16px; }")
        self.gpt_button.clicked.connect(self.show_chat_dialog)
        self.gpt_button.setMaximumSize(120, 40)  # Set a maximum size for a better look

        # Right side: Placeholders for future buttons
        right_layout = QVBoxLayout()  # Vertical layout for the placeholders

        # Placeholder buttons (disabled for now)
        for _ in range(5):
            placeholder = QPushButton('Future Feature')
            placeholder.setStyleSheet("QPushButton { color: purple; }")
            placeholder.setEnabled(False)  # Disable the button
            right_layout.addWidget(placeholder)

        # Add widgets to the main layout
        main_layout.addWidget(self.gpt_button)
        main_layout.addLayout(right_layout)
        main_layout.addStretch(1)  # Add some space at the end

        # Set the layout to the central widget
        self.central_widget.setLayout(main_layout)

    def show_chat_dialog(self):
        # Instantiate and show the chat dialog
        self.chat_dialog = ChatDialog(self)
        self.chat_dialog.exec_()  # Use exec_() to make it modal if desired

# The rest of the code for application execution should be in main.py, not in this file.
