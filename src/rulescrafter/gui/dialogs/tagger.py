from typing import TYPE_CHECKING

from PyQt6.QtWidgets import (
	QDialog,
	QPushButton,
	QTextEdit,
	QVBoxLayout,
)

if TYPE_CHECKING:
	from ..window import MainWindow

class TagsEditor(QDialog):
	"""Tags editor window."""

	def __apply(self):
		"""Apply tags."""

		tags: tuple[str, ...] = tuple(tag.strip() for tag in self.__tags_editor.toPlainText().split(","))
		self.__window.operator.set_allowed_tags(tags)
		self.close()
		self.__window.rule_editor.update_tags()

	def __build(self):
		"""Build interface."""

		layout = QVBoxLayout()

		self.__tags_editor = QTextEdit()
		self.__tags_editor.setPlaceholderText("Separated by comma tags.")

		apply_button = QPushButton()
		apply_button.setText("Apply")
		apply_button.clicked.connect(self.__apply)
		
		layout.addWidget(self.__tags_editor)
		layout.addWidget(apply_button)
		self.setLayout(layout)

	def __init__(self, parent: "MainWindow"):
		"""
		Tags editor window.

		:param parent: Parent window.
		:type parent: MainWindow
		"""

		super().__init__(parent)

		self.__window: MainWindow = parent
		
		self.setWindowTitle("Tags")
		self.setMinimumSize(480, 360)
		
		self.__build()

	def run_editor(self):
		"""Run editor."""

		tags: str = ", ".join(self.__window.operator.allowed_tags)
		self.__tags_editor.setText(tags)
		self.exec()
		
