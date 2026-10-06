from typing import TYPE_CHECKING, cast

from PyQt6.QtWidgets import (
	QDialog,
	QLineEdit,
	QPushButton,
	QScrollArea,
	QVBoxLayout,
	QWidget,
)

from dublib.functions.data import zerotify

if TYPE_CHECKING:
	from ..window import MainWindow

class GroupsEditor(QDialog):
	"""Groups editor window."""

	def __apply(self):
		"""Apply groups."""

		scroll_widget = self.__scroll_area.widget()
		assert scroll_widget is not None
		layout = scroll_widget.layout()
		assert layout is not None

		for index in range(layout.count()):
			item = layout.itemAt(index)
			if not item: continue
			widget = cast("QLineEdit | None", item.widget())
			if not widget: continue

			group: int = int(widget.placeholderText())
			name: str | None = zerotify(widget.text())
			
			self.__window.operator.set_group_name(group, name)

		self.__window.set_unsaved_state(True)
		self.close()

	def __build(self):
		"""Build interface."""

		layout = QVBoxLayout()

		apply_button = QPushButton()
		apply_button.setText("Apply")
		apply_button.clicked.connect(self.__apply)
		
		self.__scroll_area = QScrollArea()
		self.__scroll_area.setWidgetResizable(True)

		layout.addWidget(self.__scroll_area)
		layout.addWidget(apply_button)

		self.setLayout(layout)

	def __update_editors(self):
		"""Update editors."""

		editors = QWidget()
		layout = QVBoxLayout()
		editors.setLayout(layout)

		for group in self.__window.operator.groups:
			group_string: str = str(group)
			name: str | None = self.__window.operator.get_group_name(group)

			editor = QLineEdit()
			editor.setPlaceholderText(group_string)
			editor.setText(name)
			editor.setToolTip(group_string)

			layout.addWidget(editor)

		layout.addStretch()
		self.__scroll_area.setWidget(editors)

	def __init__(self, parent: "MainWindow"):
		"""
		Groups editor window.

		:param parent: Parent window.
		:type parent: MainWindow
		"""

		super().__init__(parent)

		self.__window: MainWindow = parent
		
		self.setWindowTitle("Groups")
		self.setMinimumSize(480, 360)
		
		self.__build()

	def run_editor(self):
		"""Run editor."""

		self.__update_editors()
		self.exec()
		
