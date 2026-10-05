from typing import TYPE_CHECKING, cast

from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import (
	QHBoxLayout,
	QMainWindow,
	QMenu,
	QPushButton,
	QStackedWidget,
	QVBoxLayout,
	QWidget,
)

from .. import builders
from ..core.operator import RulesOperator
from . import icons
from .base.functions import open_link_in_browser, select_file
from .dialogs.dumper import VersionDumper
from .dialogs.metainfo import MetainfoEditor
from .dialogs.tagger import TagsEditor
from .editor import RuleEditor
from .list import RulesList

if TYPE_CHECKING:
	from collections.abc import Callable
	from pathlib import Path

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

		new_button = QPushButton()
		new_button.setIcon(icons.NEW)
		new_button.setText("Create new ruleset")
		new_button.clicked.connect(lambda: self.__open_worker(None))
		
		open_button = QPushButton()
		open_button.setIcon(icons.OPEN)
		open_button.setText("Open ruleset")
		open_button.clicked.connect(self.open_file)

		layout = QVBoxLayout()
		layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
		layout.addWidget(new_button)
		layout.addWidget(open_button)

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
		new_action.setIcon(icons.NEW)
		new_action.setShortcut("Ctrl+N")
		new_action.triggered.connect(lambda: self.__open_worker(None))

		open_action = QAction("Open", self)
		open_action.setIcon(icons.OPEN)
		open_action.setShortcut("Ctrl+O")
		open_action.triggered.connect(self.open_file)

		self.__save_action = QAction("Save", self)
		self.__save_action.setIcon(icons.SAVE)
		self.__save_action.setShortcut("Ctrl+S")
		self.__save_action.setEnabled(False)
		self.__save_action.triggered.connect(self.save_file)
		
		self.__save_as_action = QAction("Save as", self)
		self.__save_as_action.setIcon(icons.SAVE_AS)
		self.__save_as_action.setShortcut("Ctrl+Shift+S")
		self.__save_as_action.setEnabled(False)
		self.__save_as_action.triggered.connect(self.save_file_as)

		self.__close_action = QAction("Close", self)
		self.__close_action.setIcon(icons.CLOSE)
		self.__close_action.setShortcut("Ctrl+Q")
		self.__close_action.triggered.connect(self.close_file)
		self.__close_action.setEnabled(False)

		file_menu.addAction(new_action)
		file_menu.addAction(open_action)
		file_menu.addSeparator()
		file_menu.addAction(self.__save_action)
		file_menu.addAction(self.__save_as_action)
		file_menu.addSeparator()
		file_menu.addAction(self.__close_action)

		self.__edit_menu = cast("QMenu", self.__menu.addMenu("Edit"))
		self.__edit_menu.setEnabled(False)

		metainfo_editor = QAction("Metainfo", self)
		metainfo_editor.setIcon(icons.EDIT)
		metainfo_editor.setShortcut("Ctrl+E")
		metainfo_editor.triggered.connect(self.__metainfo_editor.run_editor)

		dump_version_action = QAction("Dump version", self)
		dump_version_action.setIcon(icons.DUMP)
		dump_version_action.setShortcut("Ctrl+D")
		dump_version_action.triggered.connect(self.__version_dumper.run_dumper)

		tags_action = QAction("Tags", self)
		tags_action.setIcon(icons.TAGS)
		tags_action.setShortcut("Ctrl+T")
		tags_action.triggered.connect(self.__tags_editor.run_editor)
		
		self.__edit_menu.addAction(metainfo_editor)
		self.__edit_menu.addAction(dump_version_action)
		self.__edit_menu.addAction(tags_action)

		about_menu = self.__menu.addMenu("About")
		assert about_menu is not None

		github_action = QAction("GitHub", self)
		github_action.setIcon(icons.GITHUB)
		github_action.triggered.connect(lambda: open_link_in_browser("https://github.com/dub1401/RulesCrafter"))

		about_menu.addAction(github_action)

	def __build(self):
		"""Build interface."""

		self.__stacked_widget = QStackedWidget(self)

		self.__stacked_widget.addWidget(self.__build_hello())
		self.__stacked_widget.addWidget(self.__build_worker())

		self.setCentralWidget(self.__stacked_widget)

		self.__metainfo_editor = MetainfoEditor(self)
		self.__tags_editor = TagsEditor(self)
		self.__version_dumper = VersionDumper(self)

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

		file = select_file("o", filters = "JSON (*.json)")

		if file:
			self.__open_worker(file.path.as_posix())

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

		filters: tuple[str, ...] = (
			"JSON (*.json)",
			"YAML (*.yml *.yaml)",
			"Markdown (*.md)",
			"PDF (*.pdf)",
		)
		file = select_file("s", filters)

		if not file:
			return

		file_path: Path = file.path
		suffixes = file.filter_suffixes

		if not file_path.suffix and suffixes:
			file_path = file_path.with_suffix(suffixes[0])

		match file_path.suffix:

			case ".md":
				builders.MarkdownBuilder(self.__operator).dump_to_file(file_path)

			case ".yml" | ".yaml":
				builders.YAMLBuilder(self.__operator).dump_to_file(file_path)

			case ".pdf":
				builders.PDFBuilder(self.__operator).dump_to_file(file_path)

			case _:
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
			self.__edit_menu.setEnabled,
			self.__close_action.setEnabled,
		)

		for element in elements:
			element(status)
