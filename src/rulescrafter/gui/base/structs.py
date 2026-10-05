from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
	from pathlib import Path

@dataclass(frozen = True)
class SelectedFile:
	"""Selected file data."""

	path: "Path"
	filter: str | None

	@property
	def filter_suffixes(self) -> tuple[str, ...] | None:
		"""Filter extensions suffixes."""

		if not self.filter:
			return None

		parts: list[str] = self.filter.split("(", maxsplit = 1)
		extensions: list[str] = parts[-1].rstrip(")").lstrip("*").split(" ")

		return tuple(extensions)

