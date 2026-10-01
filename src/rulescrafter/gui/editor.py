from typing import TYPE_CHECKING

from PyQt6.QtCore import QRegularExpression
from PyQt6.QtGui import QRegularExpressionValidator
from PyQt6.QtWidgets import (
	QHBoxLayout,
	QLineEdit,
	QPushButton,
	QTextEdit,
	QVBoxLayout,
	QWidget,
)
from pyqt6_multiselect_combobox import MultiSelectComboBox

from .copyable_label import CopyableLabel

if TYPE_CHECKING:
	from ..core.rule import Rule
	from .window import MainWindow

class RuleEditor(QWidget):
	"""Rules list."""

	#==========================================================================================#
	# >>>>> PRIVATE METHODS <<<<< #
	#==========================================================================================#

	def __check_number(self):
		"""Check number format."""

		if not self.__rule:
			return

		number: str = self.__number.text().rstrip()

		if not number or number == self.__rule.number or self.__window.operator.is_number_correct(number):
			self.__number.setStyleSheet(None)
			self.__number.setToolTip(None)

		else:
			self.__number.setStyleSheet("color: red;")
			self.__number.setToolTip("Номер должен иметь формат x.y.z с опциональными частями и быть уникальным.")

	def __remove_rule(self):
		"""Remove rule."""

		if not self.__rule:
			return

		self.__window.rules_list.remove_rule(self.__rule.id)
		self.close_editor()

	def __update(self):
		"""Update editor."""

		if self.__rule:
			self.__number.setText(self.__rule.number)
			self.__header.setText(self.__rule.header)
			self.__description.setText(self.__rule.description)
			self.__identifier.setText(self.__rule.id)
			self.show()

		else:
			self.hide()

	def __update_save_button_state(self):
		"""Update save button state."""

		checkers: dict[str, str] = {
			"Missing number.": self.__number.text().rstrip(),
			"Missing header.": self.__header.text(),
			"Missing description.": self.__description.toPlainText(),
		}

		for tooltip, value in checkers.items():
			if not value:
				self.__save_button.setToolTip(tooltip)
				self.__save_button.setEnabled(False)
				return

		self.__save_button.setEnabled(True)

	#==========================================================================================#
	# >>>>> PRIVATE INTERFACE BUILDERS <<<<< #
	#==========================================================================================#

	def __build_footer(self) -> QWidget:
		"""
		Build editor footer.

		:return: Rule editor footer widget.
		:rtype: QWidget
		"""

		footer = QWidget(self)

		self.__identifier = CopyableLabel("")
		self.__identifier.setToolTip("Press to copy.")

		self.__save_button = QPushButton(self)
		self.__save_button.setText("Apply")
		self.__save_button.clicked.connect(self.save)

		remove_button = QPushButton(self)
		remove_button.setText("Delete")
		remove_button.clicked.connect(self.__remove_rule)

		close_button = QPushButton(self)
		close_button.setText("Close")
		close_button.clicked.connect(self.close_editor)

		footer_layout = QHBoxLayout()
		footer_layout.setContentsMargins(0, 0, 0, 0)
		footer_layout.addWidget(self.__identifier)
		footer_layout.addWidget(self.__save_button)
		footer_layout.addWidget(remove_button)
		footer_layout.addWidget(close_button)
		
		footer.setLayout(footer_layout)

		return footer

	def __build_header(self) -> QWidget:
		"""
		Build editor footer.

		:return: Rule editor footer widget.
		:rtype: QWidget
		"""

		header = QWidget(self)

		self.__tags = MultiSelectComboBox()

		self.__number = QLineEdit(self)
		self.__number.setPlaceholderText("Number x.y.z")
		self.__number.textChanged.connect(self.__update_save_button_state)
		self.__number.textChanged.connect(self.__check_number)

		regex = QRegularExpression(r"^\d+(?:\.\d*){0,2}$")
		validator = QRegularExpressionValidator(regex, self)
		self.__number.setValidator(validator)

		self.__header = QLineEdit()
		self.__header.setPlaceholderText("Header")
		self.__header.textChanged.connect(self.__update_save_button_state)

		footer_layout = QHBoxLayout()
		footer_layout.setContentsMargins(0, 0, 0, 0)
		
		footer_layout.addWidget(self.__number, stretch = 2)
		footer_layout.addWidget(self.__header, stretch = 6)
		footer_layout.addWidget(self.__tags, stretch = 2)

		header.setLayout(footer_layout)

		return header

	def __build(self):
		"""Build interface."""

		self.__description = QTextEdit()
		self.__description.setPlaceholderText("Description")
		self.__description.textChanged.connect(self.__update_save_button_state)

		rule_editor_layout = QVBoxLayout()
		rule_editor_layout.addWidget(self.__build_header())
		rule_editor_layout.addWidget(self.__description)
		rule_editor_layout.addWidget(self.__build_footer())

		self.setLayout(rule_editor_layout)

	#==========================================================================================#
	# >>>>> PUBLIC METHODS <<<<< #
	#==========================================================================================#

	def __init__(self, parent: "MainWindow"):
		"""
		Rules list.

		:param parent: Parent widget.
		:type parent: MainWindow
		"""

		super().__init__(parent)

		self.__window: MainWindow = parent
		self.__rule: Rule | None = None

		self.hide()
		self.__build()

	def close_editor(self):
		"""Close editor."""

		self.__rule = None
		self.__update()

	def save(self):
		"""Save rule data."""

		if not self.__rule:
			return

		self.__rule.set_number(self.__number.text().rstrip("."))
		self.__rule.set_header(self.__header.text())
		self.__rule.set_description(self.__description.toPlainText())
		self.__rule.set_tags(self.__tags.currentData())

		self.__window.rules_list.update_rules()

	def select_rule(self, rule: "Rule"):
		"""
		Pass rule in editor.

		:param rule: Rule.
		:type rule: Rule
		"""

		self.__rule = rule
		self.update_tags()
		self.__update()
		
	def update_tags(self):
		"""Update tags selector."""

		if self.__window.operator is None:
			return

		tags: list[str] = list(self.__window.operator.allowed_tags)

		if tags:
			self.__tags.setEnabled(True)
			self.__tags.setToolTip(None)
			self.__tags.clear()
			self.__tags.addItems(tags)
		else:
			self.__tags.setEnabled(False)
			self.__tags.setToolTip("No allowed tags.")
