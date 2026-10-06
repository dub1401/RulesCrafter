from typing import TYPE_CHECKING

from PyQt6.QtWidgets import (
	QDialog,
	QLineEdit,
	QPushButton,
	QTextEdit,
	QVBoxLayout,
)

if TYPE_CHECKING:
	from ..window import MainWindow

class MetainfoEditor(QDialog):
	"""Metainfo editor window."""

	def __apply(self):
		"""Apply tags."""

		self.__window.operator.rename(self.__name.text())
		self.__window.operator.set_description(self.__description.toPlainText())
		self.__window.set_unsaved_state(True)
		self.close()

	def __build(self):
		"""Build interface."""

		layout = QVBoxLayout()

		self.__name = QLineEdit()
		self.__name.setPlaceholderText("Ruleset name")

		self.__description = QTextEdit()
		self.__description.setPlaceholderText("Ruleset description.")

		apply_button = QPushButton()
		apply_button.setText("Apply")
		apply_button.clicked.connect(self.__apply)
		
		layout.addWidget(self.__name)
		layout.addWidget(self.__description)
		layout.addWidget(apply_button)

		self.setLayout(layout)

	def __init__(self, parent: "MainWindow"):
		"""
		Metainfo editor window.

		:param parent: Parent window.
		:type parent: MainWindow
		"""

		super().__init__(parent)

		self.__window: MainWindow = parent
		
		self.setWindowTitle("Metainfo")
		self.setMinimumSize(480, 360)
		
		self.__build()

	def run_editor(self):
		"""Run editor."""

		self.__name.setText(self.__window.operator.name)
		self.__description.setText(self.__window.operator.description)
		self.exec()
		
