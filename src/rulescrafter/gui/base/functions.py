from pathlib import Path
from typing import TYPE_CHECKING, Literal

from PyQt6.QtCore import QUrl
from PyQt6.QtGui import QDesktopServices
from PyQt6.QtWidgets import QFileDialog

from dublib.functions.data import to_sequence

from .structs import SelectedFile

if TYPE_CHECKING:
	from collections.abc import Sequence

def open_link_in_browser(link: str):
	"""Open link in browser."""
	
	QDesktopServices.openUrl(QUrl(link))

def select_file(mode: Literal["o", "s"], filters: "Sequence[str] | None" = None) -> SelectedFile | None:
	"""
	Select file to interaction.

	:param mode: Interaction mode: **o** – open, **s** – save.
	:type mode: Literal["o", "s"]
	:param filters: Files filters sequence.
	:type filters: Sequence[str] | None
	:return: Selected file data or `None` if cancelled.
	:rtype: SelectedFile | None
	"""

	filters_query: str | None = ";;".join(to_sequence(filters)) if filters else None
	selected_file: str | None = None
	used_filter: str | None = None

	match mode:
		case "o":
			selected_file, used_filter  = QFileDialog.getOpenFileName(filter = filters_query)
		case "s":
			selected_file, used_filter = QFileDialog.getSaveFileName(filter = filters_query)

	file_path: Path = Path(selected_file)

	if file_path.as_posix() == ".":
		return None

	return SelectedFile(file_path, used_filter)
