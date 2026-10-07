import sys

from PyQt6.QtWidgets import QApplication

from rulescrafter.gui.main_window import MainWindow

def main():
	application = QApplication(sys.argv)

	window = MainWindow()
	window.show()
	application.exec()

if __name__ == "__main__":
	main()
