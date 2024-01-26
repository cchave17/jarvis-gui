from PyQt5.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QWidget, QTextEdit, QLabel
from PyQt5.QtGui import QTextCursor 
from PyQt5.QtCore import pyqtSlot
from openai_api.api_client import OpenAIClient
class ChatDialog(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.openai_client = OpenAIClient()
        self.initUI()
        
    def initUI(self):
        layout = QVBoxLayout()

        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        self.user_input = QTextEdit()
        self.user_input.setFixedHeight(50)
        send_button = QPushButton('Send')
        send_button.clicked.connect(self.send_message)

        layout.addWidget(self.chat_display)
        layout.addWidget(QLabel("Ask a question:"))
        layout.addWidget(self.user_input)
        layout.addWidget(send_button)

        self.setLayout(layout)
        
    @pyqtSlot()
    def send_message(self):
        user_message = self.user_input.toPlainText().strip()
        if user_message:
            # Append user's message to chat display
            self.append_to_chat(f"You: {user_message}")
            self.user_input.clear()

            # Send message to OpenAI API
            response = self.openai_client.query_chat_model('gpt-4-turbo', user_message)
            # Assume response is a dict with a 'choices' key containing the reply.
            gpt_response = response['choices'][0]['message']['content'] if 'choices' in response else "Error: No response."
            
            # Append GPT-4's response to chat display
            self.append_to_chat(f"GPT-4: {gpt_response}")
    
    def append_to_chat(self, message):
        self.chat_display.moveCursor(QTextCursor.End)
        self.chat_display.insertPlainText(message + "\n")
        self.chat_display.moveCursor(QTextCursor.End)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle('Personal Assistant')
        self.setGeometry(300, 300, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        layout = QVBoxLayout()

        self.gpt_button = QPushButton('GPT 4')
        self.gpt_button.setStyleSheet("color: red;")
        self.gpt_button.clicked.connect(self.show_chat_dialog)

        layout.addWidget(self.gpt_button)

        # Placeholder for future buttons
        # For now, just using labels with purple text as placeholders.
        for _ in range(5):
            placeholder = QLabel('Future Feature')
            placeholder.setStyleSheet("color: purple;")
            layout.addWidget(placeholder)

        self.central_widget.setLayout(layout)
    
    def show_chat_dialog(self):
        self.chat_dialog = ChatDialog(self)
        self.chat_dialog.show()
