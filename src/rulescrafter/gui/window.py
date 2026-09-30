from typing import TYPE_CHECKING

from PyQt6.QtCore import QSize, Qt, QUrl
from PyQt6.QtGui import QAction, QDesktopServices
from PyQt6.QtWidgets import (
	QFileDialog,
	QHBoxLayout,
	QLabel,
	QMainWindow,
	QStackedWidget,
	QVBoxLayout,
	QWidget,
)

from ..core.operator import RulesOperator
from .editor import RuleEditor
from .list import RulesList

if TYPE_CHECKING:
	from collections.abc import Callable

class MainWindow(QMainWindow):
	"""Main window."""

	#==========================================================================================#
	# >>>>> PROPERTIES <<<<< #
	#==========================================================================================#

	@property
	def operator(self) -> RulesOperator:
		"""Rules operator."""

		assert self.__operator is not None

		return self.__operator

	#==========================================================================================#
	# >>>>> WIDGETS <<<<< #
	#==========================================================================================#

	@property
	def rule_editor(self) -> RuleEditor:
		"""Rule editor."""

		return self.__rule_editor

	@property
	def rules_list(self) -> RulesList:
		"""Rules list."""

		return self.__rules_list

	#==========================================================================================#
	# >>>>> PRIVATE METHODS <<<<< #
	#==========================================================================================#

	def __open_worker(self, file: str | None = None):
		"""
		Open worker.

		:param file: Rules file path.
		:type file: str | None
		"""

		if self.__operator:
			self.__rule_editor.close_editor()

		self.__operator = RulesOperator(file)
		self.rules_list.update_rules()
		self.__stacked_widget.setCurrentIndex(1)
		self.set_menu_file_interaction_state(True)

	#==========================================================================================#
	# >>>>> PRIVATE INTERFACE BUILDERS <<<<< #
	#==========================================================================================#

	def __build_hello(self) -> QWidget:
		"""
		Build hello.

		:return: Hello widget.
		:rtype: QWidget
		"""

		hello = QWidget(self)

		label = QLabel("Open rules file or connect to repository.")

		layout = QVBoxLayout()
		layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
		layout.addWidget(label, stretch = 10)

		hello.setLayout(layout)

		return hello

	def __build_worker(self) -> QWidget:
		"""
		Build worker.

		:return: Worker widget.
		:rtype: QWidget
		"""

		worker = QWidget(self)

		self.__rules_list = RulesList(self)
		self.__rule_editor = RuleEditor(self)

		layout = QHBoxLayout()
		layout.addWidget(self.__rules_list, stretch = 3)
		layout.addWidget(self.__rule_editor, stretch = 7)

		worker.setLayout(layout)

		return worker

	def __build_menu(self):
		"""Build menu."""

		self.__menu = self.menuBar()
		self.setMenuBar(self.__menu)
		assert self.__menu is not None

		file_menu = self.__menu.addMenu("File")
		assert file_menu is not None

		new_action = QAction("New", self)
		new_action.triggered.connect(lambda: self.__open_worker(None))

		open_action = QAction("Open", self)
		open_action.triggered.connect(self.open_file)

		self.__save_action = QAction("Save", self)
		self.__save_action.setShortcut("Ctrl+S")
		self.__save_action.setEnabled(False)
		self.__save_action.triggered.connect(self.save_file)
		
		self.__save_as_action = QAction("Save as", self)
		self.__save_as_action.setEnabled(False)
		self.__save_as_action.triggered.connect(self.save_file_as)

		close_action = QAction("Close", self)
		close_action.triggered.connect(self.close_file)

		file_menu.addAction(new_action)
		file_menu.addAction(open_action)
		file_menu.addSeparator()
		file_menu.addAction(self.__save_action)
		file_menu.addAction(self.__save_as_action)
		file_menu.addSeparator()
		file_menu.addAction(close_action)

		edit_menu = self.__menu.addMenu("Edit")
		assert edit_menu is not None

		dump_version_action = QAction("Dump version", self)
		dump_version_action.setEnabled(False)

		tags_action = QAction("Tags", self)
		tags_action.setEnabled(False)

		edit_menu.addAction(dump_version_action)
		edit_menu.addAction(tags_action)

		about_menu = self.__menu.addMenu("About")
		assert about_menu is not None

		github_action = QAction("GitHub", self)
		github_action.triggered.connect(lambda: self.open_link_in_browser("https://github.com/dub1401/RulesCrafter"))

		about_menu.addAction(github_action)

	def __build(self):
		"""Build interface."""

		self.__stacked_widget = QStackedWidget(self)

		self.__stacked_widget.addWidget(self.__build_hello())
		self.__stacked_widget.addWidget(self.__build_worker())

		self.setCentralWidget(self.__stacked_widget)

		self.__build_menu()

	#==========================================================================================#
	# >>>>> PUBLIC METHODS <<<<< #
	#==========================================================================================#

	def __init__(self):
		"""Main window."""

		super().__init__()
		
		self.__operator: RulesOperator | None = None

		self.setWindowTitle("RulesCrafter")
		self.setMinimumSize(QSize(1280, 720))

		self.__build()

	def close_file(self):
		"""Close file."""

		self.__operator = None

		self.set_menu_file_interaction_state(False)
		self.__stacked_widget.setCurrentIndex(0)

	def open_file(self):
		"""Open file."""

		file_path, _  = QFileDialog.getOpenFileName(filter = "JSON Files (*.json)")

		if file_path:
			self.__open_worker(file_path)

	def open_link_in_browser(self, link: str):
		"""Open link in browser."""
		
		QDesktopServices.openUrl(QUrl(link))

	def save_file(self):
		"""Save file."""
		
		if not self.__operator:
			return

		if not self.__operator.file:
			self.save_file_as()
		else:
			self.__operator.save()

	def save_file_as(self):
		"""Save file as."""

		if not self.__operator:
			return

		file_path, _  = QFileDialog.getSaveFileName(filter = "JSON Files (*.json)")
		
		if file_path:
			self.__operator.set_file_path(file_path)
			self.__operator.save()

	def set_menu_file_interaction_state(self, status: bool):
		"""
		Set menu file interaction state.

		:param status: Is file loaded.
		:type status: bool
		"""

		elements: tuple[Callable, ...] = (
			self.__save_action.setEnabled,
			self.__save_as_action.setEnabled,
		)

		for element in elements:
			element(status)
