import sys

from PyQt6.QtWidgets import QApplication

from .gui.window import MainWindow

def main():
	application = QApplication(sys.argv)

	window = MainWindow()
	window.show()
	window.show_hello()
	application.exec()

if __name__ == "__main__":
	main()
