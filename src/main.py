import sys
from PyQt5.QtWidgets import QApplication
from gui.main_window import MainWindow
from openai_api.api_client import OpenAIClient

def main():
    app = QApplication(sys.argv)
    openai_client = OpenAIClient()
    openai_client.test_query()  # Call the test function

    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
