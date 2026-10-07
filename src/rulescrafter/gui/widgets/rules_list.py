from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
	QLineEdit,
	QListWidget,
	QListWidgetItem,
	QPushButton,
	QVBoxLayout,
)

from ..base.main_widget import BaseMainWidget

class RulesList(BaseMainWidget):
	"""Rules list."""

	#==========================================================================================#
	# >>>>> PRIVATE METHODS <<<<< #
	#==========================================================================================#

	def __create_rule(self):
		"""Create rule."""

		rule = self.main_window.operator.create_rule()
		self.main_window.widgets.rule_editor.select_rule(rule)
		self.update_rules()

	def __create_rules_section(self, name: str):
		"""
		Crate rule section and add it to list.

		:param name: Section name.
		:type name: str
		"""

		section = QListWidgetItem(name)
		section.setBackground(Qt.GlobalColor.lightGray)
		section.setFlags(section.flags() & ~Qt.ItemFlag.ItemIsSelectable & ~Qt.ItemFlag.ItemIsEnabled)

		self.__rules_list.addItem(section)

	def __select_rule(self):
		"""Select rule."""
		
		current_row: int = self.__rules_list.currentRow()
		item = self.__rules_list.item(current_row)

		if item:
			rule_id: str = item.data(Qt.ItemDataRole.UserRole)
			rule = self.main_window.operator.get_rule(rule_id)
			self.main_window.widgets.rule_editor.select_rule(rule)

	#==========================================================================================#
	# >>>>> OVERRIDABLE METHODS <<<<< #
	#==========================================================================================#

	def _build(self):
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

	def remove_rule(self, rule_id: str):
		"""
		Remove rule.

		:param rule_id: Rule ID.
		:type rule_id: str
		"""

		self.main_window.operator.remove_rule(rule_id)
		self.update_rules()
		
	def update_rules(self, search: str | None = None):
		"""
		Update rules list.

		:param search: Seqarch query.
		:type search: str | None
		"""

		self.__rules_list.clear()
		section: str | None = None

		for rule in self.main_window.operator.rules:
			if search and search not in rule.indexable_string:
				continue

			new_section: str | None = self.main_window.operator.build_group_name_with_number(rule.number)

			if new_section and new_section != section:
				self.__create_rules_section(new_section)
				section = new_section

			item = QListWidgetItem(rule.title)
			item.setData(Qt.ItemDataRole.UserRole, rule.id)
			self.__rules_list.addItem(item)