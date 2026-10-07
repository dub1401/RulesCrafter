from abc import ABCMeta, abstractmethod
from typing import TYPE_CHECKING

from PyQt6.QtWidgets import QWidget

if TYPE_CHECKING:
	from ..main_window import MainWindow

class ABCQWidgetMeta(ABCMeta, type(QWidget)):
	pass

class BaseMainWidget(QWidget, metaclass = ABCQWidgetMeta):
	"""Base main window widget."""

	#==========================================================================================#
	# >>>>> PROPERTIES <<<<< #
	#==========================================================================================#

	@property
	def main_window(self) -> "MainWindow":
		"""Main window."""

		return self._window

	#==========================================================================================#
	# >>>>> OVERRIDABLE METHODS <<<<< #
	#==========================================================================================#

	@abstractmethod
	def _build(self):
		"""Build interface."""

		pass

	def _post_init(self):
		"""Execute after instance initialization."""

		pass

	#==========================================================================================#
	# >>>>> SPECIAL METHODS <<<<< #
	#==========================================================================================#

	def __init__(self, parent: "MainWindow"):
		"""
		Base main window widget.

		:param parent: Parent window.
		:type parent: MainWindow
		"""

		super().__init__(parent)

		self._window: MainWindow = parent

		self._post_init()
		self._build()
