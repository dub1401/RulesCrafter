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
		Generate pragraph string from rule data.

		:param rule: Rule.
		:type rule: Rule
		:return: Paragraph string in Markdown.
		:rtype: str
		"""

		tags: str = ", ".join(f"`{tag}`" for tag in rule.tags)
		if tags: tags += "\n\n"

		return f"## <a id=\"{rule.id}\"></a>{rule.number}. {rule.header}\n{tags}{rule.description}\n"

	def __init__(self, operator: "RulesOperator"):
		"""
		Markdown builder.

		:param operator: Rules operator.
		:type operator: RulesOperator
		"""
		self.__operator: RulesOperator = operator

	def dump_to_file(self, file_path: PathLike[str] | str):
		"""
		Dump ruleset in Markdown file.

		:param file_path: Path to Markdown file.
		:type file_path: PathLike[str] | str
		"""

		file_path = Path(file_path).with_suffix(".md")
		
		rules: tuple[Rule, ...] = tuple(sorted(
			self.__operator.rules, 
			key = lambda rule: (rule.number is None, rule.number),
		))
		paragraphs: tuple[str, ...] = tuple(self.__rule_to_paragraph(rule) for rule in rules)

		text.write(file_path, paragraphs)


	
