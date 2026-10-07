from pathlib import Path
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

from ... import builders
from ...core import exceptions
from ...core.operator import RulesOperator
from .. import icons
from ..base.functions import open_link_in_browser, select_file
from ..dialogs.dumper import VersionDumper
from ..dialogs.groups import GroupsEditor
from ..dialogs.metainfo import MetainfoEditor
from ..dialogs.tagger import TagsEditor
from ..editor import RuleEditor
from ..list import RulesList
from .enums import StacksIndexes

if TYPE_CHECKING:
	from os import PathLike

	from PyQt6.QtWidgets import QMenuBar
	
class MainWindow(QMainWindow):
	"""Main window."""

	#==========================================================================================#
	# >>>>> PROPERTIES <<<<< #
	#==========================================================================================#

	@property
	def operator(self) -> RulesOperator:
		"""
		Rules operator.
		
		:raises NoRulesetError: Ruleset not opened.
		"""

		if self.__operator is None:
			raise exceptions.NoRulesetError()

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

	def __switch_widget(self, index: StacksIndexes):
		"""
		Switch to main window widget with index.

		:param index: Main windows stacked widgets indexes.
		:type index: StacksIndexes
		"""

		self.__stacked_widget.setCurrentIndex(index.value)

	#==========================================================================================#
	# >>>>> PRIVATE MENU BUILDERS <<<<< #
	#==========================================================================================#

	def __build_menu_about(self, menu_bar: "QMenuBar"):
		"""
		Build menu: **About**.

		:param menu_bar: Menu bar.
		:type menu_bar: QMenuBar
		"""

		menu: QMenu = cast("QMenu", menu_bar.addMenu("About"))

		github_action = QAction("GitHub", self)
		github_action.setIcon(icons.GITHUB)
		github_action.triggered.connect(lambda: open_link_in_browser("https://github.com/dub1401/RulesCrafter"))

		menu.addAction(github_action)

	def __build_menu_edit(self, menu_bar: "QMenuBar"):
		"""
		Build menu: **Edit**.

		:param menu_bar: Menu bar.
		:type menu_bar: QMenuBar
		"""

		menu: QMenu = cast("QMenu", menu_bar.addMenu("Edit"))
		menu.setEnabled(False)
		self.__menu_file_interactors.append(menu)

		metainfo_action: QAction = QAction("Metainfo", self)
		metainfo_action.setIcon(icons.EDIT)
		metainfo_action.setShortcut("Ctrl+E")
		metainfo_action.triggered.connect(self.__metainfo_editor.run_editor)

		groups_action: QAction = QAction("Groups", self)
		groups_action.setIcon(icons.GROUPS)
		groups_action.setShortcut("Ctrl+G")
		groups_action.triggered.connect(self.__groups_editor.run_editor)

		dump_version_action: QAction = QAction("Dump version", self)
		dump_version_action.setIcon(icons.DUMP)
		dump_version_action.setShortcut("Ctrl+D")
		dump_version_action.triggered.connect(self.__version_dumper.run_dumper)

		tags_action: QAction = QAction("Tags", self)
		tags_action.setIcon(icons.TAGS)
		tags_action.setShortcut("Ctrl+T")
		tags_action.triggered.connect(self.__tags_editor.run_editor)

		menu.addAction(metainfo_action)
		menu.addAction(groups_action)
		menu.addAction(dump_version_action)
		menu.addAction(tags_action)

	def __build_menu_file(self, menu_bar: "QMenuBar"):
		"""
		Build menu: **File**.

		:param menu_bar: Menu bar.
		:type menu_bar: QMenuBar
		"""

		menu: QMenu = cast("QMenu", menu_bar.addMenu("File"))

		new_action: QAction = QAction("New", self)
		new_action.setIcon(icons.NEW)
		new_action.setShortcut("Ctrl+N")
		new_action.triggered.connect(lambda: self.open_file(True))

		open_action: QAction = QAction("Open", self)
		open_action.setIcon(icons.OPEN)
		open_action.setShortcut("Ctrl+O")
		open_action.triggered.connect(self.open_file)

		save_action: QAction = QAction("Save", self)
		save_action.setEnabled(False)
		save_action.setIcon(icons.SAVE)
		save_action.setShortcut("Ctrl+S")
		save_action.triggered.connect(self.save_file)
		self.__menu_file_interactors.append(save_action)

		save_as_action: QAction = QAction("Save as", self)
		save_as_action.setEnabled(False)
		save_as_action.setIcon(icons.SAVE_AS)
		save_as_action.setShortcut("Ctrl+Shift+S")
		save_as_action.triggered.connect(self.save_file_as)
		self.__menu_file_interactors.append(save_as_action)

		close_action: QAction = QAction("Close", self)
		close_action.setEnabled(False)
		close_action.setIcon(icons.CLOSE)
		close_action.setShortcut("Ctrl+Q")
		close_action.triggered.connect(self.close_file)
		self.__menu_file_interactors.append(close_action)

		menu.addAction(new_action)
		menu.addAction(open_action)
		menu.addSeparator()
		menu.addAction(save_action)
		menu.addAction(save_as_action)
		menu.addSeparator()
		menu.addAction(close_action)

	def __build_menu_tools(self, menu_bar: "QMenuBar"):
		"""
		Build menu: **Tools**.

		:param menu_bar: Menu bar.
		:type menu_bar: QMenuBar
		"""

		menu: QMenu = cast("QMenu", menu_bar.addMenu("Tools"))

		auto_numbering_action: QAction = QAction("Auto-numbering", self)
		auto_numbering_action.setCheckable(True)
		auto_numbering_action.setChecked(True)

		menu.addAction(auto_numbering_action)

	def __build_menu(self):
		"""Build menu."""

		menu_bar: QMenuBar = cast("QMenuBar", self.menuBar())
		self.setMenuBar(menu_bar)

		self.__build_menu_file(menu_bar)
		self.__build_menu_edit(menu_bar)
		self.__build_menu_tools(menu_bar)
		self.__build_menu_about(menu_bar)

	#==========================================================================================#
	# >>>>> PRIVATE INTERFACE BUILDERS <<<<< #
	#==========================================================================================#

	def __build_hello(self) -> QWidget:
		"""
		Build hello.

		:return: Hello widget.
		:rtype: QWidget
		"""

		hello: QWidget = QWidget(self)

		new_button = QPushButton()
		new_button.setIcon(icons.NEW)
		new_button.setText("Create new ruleset")
		new_button.clicked.connect(lambda: self.open_file(True))
		
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

		worker: QWidget = QWidget(self)

		self.__rules_list = RulesList(self)
		self.__rule_editor = RuleEditor(self)

		layout = QHBoxLayout()
		layout.addWidget(self.__rules_list, stretch = 3)
		layout.addWidget(self.__rule_editor, stretch = 7)

		worker.setLayout(layout)

		return worker

	def __build(self):
		"""Build interface."""

		self.__stacked_widget: QStackedWidget = QStackedWidget(self)
		self.__stacked_widget.addWidget(self.__build_hello())
		self.__stacked_widget.addWidget(self.__build_worker())

		self.setCentralWidget(self.__stacked_widget)

		self.__metainfo_editor = MetainfoEditor(self)
		self.__groups_editor = GroupsEditor(self)
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
		self.__window_title: str = "RulesCrafter"
		self.__menu_file_interactors: list[QAction | QMenu] = []

		self.setWindowTitle(self.__window_title)
		self.setMinimumSize(QSize(640, 480))
		self.resize(1280, 720)
		
		self.__build()

	def close_file(self):
		"""Close file."""

		self.__operator = None
		self.set_menu_file_interaction_state(False)
		self.__switch_widget(StacksIndexes.Hello)

	def open_file(self, create_new: bool = False):
		"""
		Open file.

		:param create_new: Create new file.
		:type create_new: bool
		"""

		file_path: PathLike[str] | str | None = None

		if not create_new:
			buffer = select_file("o", filters = "JSON (*.json)")

			if not buffer:
				return

			file_path = buffer.path.as_posix()

		# Close current operator and editor if opened.
		if self.__operator:
			self.__operator = None
			self.__rule_editor.close_editor()

		if not file_path:
			self.set_unsaved_state(True)

		self.__operator = RulesOperator(file_path)
		self.__rules_list.update_rules()
		self.__switch_widget(StacksIndexes.Worker)
		self.set_menu_file_interaction_state(True)

	def save_file(self):
		"""Save file."""
		
		if not self.__operator:
			raise exceptions.NoRulesetError()

		if not self.__operator.file:
			self.save_file_as()
		else:
			self.__operator.save()
			self.set_unsaved_state(False)

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
		file = select_file("s", filters, self.__operator.version)

		if not file:
			return

		file_path: Path = file.path
		suffixes = file.filter_suffixes

		if suffixes and file_path.suffix not in suffixes:
			path_string: str = file_path.as_posix().rstrip(".")
			file_path = Path(path_string + suffixes[0])

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
				self.set_unsaved_state(False)

	def set_menu_file_interaction_state(self, status: bool):
		"""
		Set menu file interaction state.

		:param status: Is file loaded.
		:type status: bool
		"""

		for element in self.__menu_file_interactors:
			element.setEnabled(status)

	def set_unsaved_state(self, status: bool):
		"""
		Set condition: is data has unsaved changes.

		:param status: Condition value.
		:type status: bool
		"""

		if status:
			self.setWindowTitle("* " + self.__window_title)
		else:
			self.setWindowTitle(self.__window_title)
