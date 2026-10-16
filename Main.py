
import sys

from PyQt6.QtWidgets import QApplication, QMessageBox
from Service.ModelDownloader import ModelDownloader
from View.MainView import MainView
def main():
    app = QApplication(sys.argv)

    setup = ModelDownloader()

    if setup.exec() != ModelDownloader.DialogCode.Accepted:
        if setup.error_message:
            QMessageBox.critical(
                None,
                "Model Setup Failed",
                setup.error_message
            )
        return

    # The model is ready. Open the existing application.
    

    window = MainView()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
