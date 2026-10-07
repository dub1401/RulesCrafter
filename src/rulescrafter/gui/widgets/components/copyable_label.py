from typing import override

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
	QApplication,
	QLabel,
)

class CopyableLabel(QLabel):
	"""Copyable label."""

	def __init__(self, *args, **kargs):
		"""Copyable label."""

		super().__init__(*args, **kargs)

		self.setCursor(Qt.CursorShape.PointingHandCursor)

	@override
	def mousePressEvent(self, ev):
		"""Set label text in clipboard after click by LMB."""

		if ev and ev.button() == Qt.MouseButton.LeftButton:
			clipboard = QApplication.clipboard()
			
			if clipboard:
				clipboard.setText(self.text())
			
		super().mousePressEvent(ev)