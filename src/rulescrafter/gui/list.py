from typing import TYPE_CHECKING

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
	QLineEdit,
	QListWidget,
	QListWidgetItem,
	QPushButton,
	QVBoxLayout,
	QWidget,
)

if TYPE_CHECKING:
	from .window import MainWindow

class RulesList(QWidget):
	"""Rules list."""

	#==========================================================================================#
	# >>>>> PRIVATE METHODS <<<<< #
	#==========================================================================================#

	def __create_rule(self):
		"""Create rule."""

		rule = self.__window.operator.create_rule()
		self.__window.rule_editor.select_rule(rule)
		self.update_rules()

	def __select_rule(self):
		"""Select rule."""
		
		current_row: int = self.__rules_list.currentRow()
		item = self.__rules_list.item(current_row)

		if item:
			rule_id: str = item.data(Qt.ItemDataRole.UserRole)
			rule = self.__window.operator.get_rule(rule_id)
			self.__window.rule_editor.select_rule(rule)

	#==========================================================================================#
	# >>>>> PRIVATE INTERFACE BUILDERS <<<<< #
	#==========================================================================================#

	def __build(self):
		"""Build interface."""

		search_input = QLineEdit()
		search_input.setPlaceholderText("Search…")
		search_input.textChanged.connect(lambda: self.update_rules(search_input.text()))

		self.__rules_list = QListWidget(self)
		self.__rules_list.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
		self.__rules_list.itemClicked.connect(self.__select_rule)

		new_rule_button = QPushButton(self)
		new_rule_button.setText("Create")
		new_rule_button.clicked.connect(self.__create_rule)

		layout = QVBoxLayout()
		layout.addWidget(search_input)
		layout.addWidget(self.__rules_list)
		layout.addWidget(new_rule_button)
		
		self.setLayout(layout)

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

		self.__build()

	def remove_rule(self, rule_id: str):
		"""
		Remove rule.

		:param rule_id: Rule ID.
		:type rule_id: str
		"""

		self.__window.operator.remove_rule(rule_id)
		self.update_rules()
		
	def update_rules(self, search: str | None = None):
		"""
		Update rules list.

		:param search: Seqarch query.
		:type search: str | None
		"""

		self.__rules_list.clear()

		for rule in self.__window.operator.rules:
			if search and search not in rule.indexable_string:
				continue
			
			item = QListWidgetItem(rule.title)
			item.setData(Qt.ItemDataRole.UserRole, rule.id)
			self.__rules_list.addItem(item)