from os import PathLike
from pathlib import Path
from typing import TYPE_CHECKING

from markdown_pdf import MarkdownPdf, Section

from .markdown import MarkdownBuilder

if TYPE_CHECKING:
	from ..core.operator import RulesOperator

class PDFBuilder:
	"""PDF builder."""

	def __init__(self, operator: "RulesOperator"):
		"""
		PDF builder.

		:param operator: Rules operator.
		:type operator: RulesOperator
		"""

		self.__operator: RulesOperator = operator

	def dump_to_file(self, file_path: PathLike[str] | str):
		"""
		Dump ruleset in YAML file.

		:param file_path: Path to Markdown file.
		:type file_path: PathLike[str] | str
		"""

		file_path = Path(file_path).with_suffix(".pdf")
		generator = MarkdownPdf(toc_level = 3)
		markdown = MarkdownBuilder(self.__operator)

		if self.__operator.name:
			generator.meta["title"] = self.__operator.name

		generator.add_section(Section(markdown.build()))
		generator.save(file_path)
	