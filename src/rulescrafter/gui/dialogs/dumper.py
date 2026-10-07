from typing import TYPE_CHECKING

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
	QDialog,
	QHBoxLayout,
	QLabel,
	QLineEdit,
	QPushButton,
	QVBoxLayout,
	QWidget,
)

if TYPE_CHECKING:
	from ..main_window import MainWindow

class VersionDumper(QDialog):
	"""Version dump window."""

	def __dump(self):
		"""Dump version."""

		version: str = self.__new_version.text()
		self.__window.operator.set_version(version)
		self.__window.set_unsaved_state(True)
		self.close()

	def __build_buttons(self) -> QWidget:
		"""
		Build buttons.

		:return: Versions widget.
		:rtype: QWidget
		"""

		buttons = QWidget()

		layout = QHBoxLayout()

		dump_button = QPushButton()
		dump_button.setText("Dump")
		dump_button.clicked.connect(self.__dump)

		cancel_button = QPushButton()
		cancel_button.setText("Cancel")
		cancel_button.clicked.connect(self.close)
		
		layout.addWidget(dump_button)
		layout.addWidget(cancel_button)

		buttons.setLayout(layout)

		return buttons

	def __build_versions(self) -> QWidget:
		"""
		Build versions.

		:return: Versions widget.
		:rtype: QWidget
		"""

		versions = QWidget()
		layout = QHBoxLayout()

		self.__old_version = QLineEdit()
		self.__old_version.setAlignment(Qt.AlignmentFlag.AlignCenter)
		self.__old_version.setEnabled(False)

		label = QLabel()
		label.setText("➔")

		self.__new_version = QLineEdit()
		self.__new_version.setAlignment(Qt.AlignmentFlag.AlignCenter)
		
		layout.addWidget(self.__old_version)
		layout.addWidget(label)
		layout.addWidget(self.__new_version)
		versions.setLayout(layout)

		return versions

	def __build(self):
		"""Build interface."""

		version = self.__build_versions()
		buttons = self.__build_buttons()

		layout = QVBoxLayout()

		layout.addWidget(version)
		layout.addWidget(buttons)
		
		self.setLayout(layout)

	def __init__(self, parent: "MainWindow"):
		"""
		Tags editor window.

		:param parent: Parent window.
		:type parent: MainWindow
		"""

		super().__init__(parent)

		self.__window: MainWindow = parent
		
		self.setWindowTitle("Dump version")
		self.setMinimumSize(480, 100)
		
		self.__build()

	def run_dumper(self):
		"""Run version dumper."""

		self.__old_version.setText(self.__window.operator.version)

		version: str = self.__window.operator.generate_version()
		self.__new_version.setText(version)

		self.exec()
		
