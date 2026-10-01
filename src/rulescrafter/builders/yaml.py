from os import PathLike
from pathlib import Path
from typing import TYPE_CHECKING

from dublib.functions.filesystem import yaml

if TYPE_CHECKING:
	from ..core.operator import RulesOperator

class YAMLBuilder:
	"""YAML builder."""

	def __init__(self, operator: "RulesOperator"):
		"""
		YAML builder.

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

		file_path = Path(file_path).with_suffix(".yml")

		data: dict = self.__operator.to_dict()
		data["allowed_tags"] = list(data["allowed_tags"])
		data["rules"] = list(data["rules"])

		for rule in data["rules"]:
			rule["tags"] = list(rule["tags"])

		yaml.write(file_path, data)
	