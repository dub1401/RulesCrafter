from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QAction
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
		new_action.triggered.connect(self.new_file)

		open_action = QAction("Open", self)
		open_action.triggered.connect(self.open_file)

		self.__save_action = QAction("Save", self)
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
		
		

		about_menu = self.__menu.addMenu("About")
		assert about_menu is not None

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

		self.__save_action.setEnabled(False)
		self.__save_as_action.setEnabled(False)

		self.show_hello()

	def new_file(self):
		"""Create file."""

		self.__operator = RulesOperator()
		self.show_rules_list()

		self.__save_action.setEnabled(True)
		self.__save_as_action.setEnabled(True)

	def open_file(self):
		"""Open file."""

		file_path, _  = QFileDialog.getOpenFileName(filter = "JSON Files (*.json)")

		if file_path:
			
			if self.__operator:
				self.__rule_editor.close_editor()

			self.__operator = RulesOperator(file_path)
			self.show_rules_list()

			self.__save_action.setEnabled(True)
			self.__save_as_action.setEnabled(True)

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

	def show_hello(self):
		"""Show hello page."""

		self.__stacked_widget.setCurrentIndex(0)

	def show_rules_list(self):
		"""Show rules_list."""

		self.rules_list.update_rules()
		self.__stacked_widget.setCurrentIndex(1)
