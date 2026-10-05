from os import PathLike
from pathlib import Path
from typing import TYPE_CHECKING

from dublib.functions.filesystem import text

if TYPE_CHECKING:
	from ..core.operator import RulesOperator
	from ..core.rule import Rule

class MarkdownBuilder:
	"""Markdown builder."""

	def __rule_to_paragraph(self, rule: "Rule") -> str:
		"""
		Generate paragraph string from rule data.

		:param rule: Rule.
		:type rule: Rule
		:return: Paragraph string in Markdown.
		:rtype: str
		"""

		tags: str = ", ".join(f"`{tag}`" for tag in rule.tags)
		if tags: tags += "\n\n"

		return f"### <a id=\"{rule.id}\">{rule.number}</a>. {rule.header}\n{tags}{rule.description}\n"

	def __init__(self, operator: "RulesOperator"):
		"""
		Markdown builder.

		:param operator: Rules operator.
		:type operator: RulesOperator
		"""
		self.__operator: RulesOperator = operator

	def build(self) -> str:
		"""
		Build Markdown text.

		:return: Markdown text.
		:rtype: str
		"""

		content: list[str] = []
		paragraphs: list[str] = []
		section: str | None = None

		for rule in self.__operator.rules:
			new_section: str | None = self.__operator.get_group_name(rule.number)

			if new_section and new_section != section:
				section = new_section
				paragraphs.append(f"## {section}\n")

			paragraphs.append(self.__rule_to_paragraph(rule))

		if self.__operator.name:
			content.append(f"# {self.__operator.name}")

		if self.__operator.description:
			content.append(f"{self.__operator.description}\n")

		content += paragraphs

		return "\n".join(content)

	def dump_to_file(self, file_path: PathLike[str] | str):
		"""
		Dump ruleset in Markdown file.

		:param file_path: Path to Markdown file.
		:type file_path: PathLike[str] | str
		"""

		file_path = Path(file_path).with_suffix(".md")
		text.write(file_path, self.build())
