import re
import uuid
from datetime import datetime
from os import PathLike
from pathlib import Path
from typing import TYPE_CHECKING

from pydantic import TypeAdapter

from dublib.functions.data import zerotify
from dublib.functions.filesystem import json

from .models import RuleModel, RulesFileModel
from .rule import Rule

if TYPE_CHECKING:
	from collections.abc import Sequence

class RulesOperator:
	"""Rules operator."""

	@property
	def allowed_tags(self) -> tuple[str, ...]:
		"""Allowed tags."""

		return tuple(self.__data.allowed_tags)

	@property
	def description(self) -> str | None:
		"""Ruleset description."""

		return self.__data.description

	@property
	def name(self) -> str | None:
		"""Ruleset name."""

		return self.__data.name

	@property
	def file(self) -> Path | None:
		"""Rules file path."""

		return self.__file

	@property
	def rules(self) -> tuple[Rule, ...]:
		"""Rules."""

		return tuple(self.__rules.values())

	@property
	def version(self) -> str | None:
		"""Ruleset version."""

		return self.__data.version

	def __generate_uuid(self) -> str:
		"""
		Generate unique UUIDv4.

		:return: Unique UUIDv4.
		:rtype: str
		"""

		value: str | None = None

		while value is None or value in self.__rules:
			value = str(uuid.uuid4())

		return value

	def __init__(self, file: PathLike[str] | str | None = None):
		"""
		Rules operator.

		:param file: Rules file path.
		:type file: PathLike[str] | str | None
		"""

		self.__file: Path | None = Path(file).with_suffix(".json") if file else None

		self.__rules: dict[str, Rule] = {}
		self.__regex: re.Pattern = re.compile(r"^\d+(?:\.\d+)?(?:\.\d+)?$")

		self.__data_adapter: TypeAdapter[RulesFileModel] = TypeAdapter(RulesFileModel)
		self.__data: RulesFileModel = self.load()

	def create_rule(self) -> Rule:
		"""
		Create rule.

		:return: Created rule.
		:rtype: Rule
		"""

		identifier: str = self.__generate_uuid()
		rule = Rule(self, RuleModel(id = identifier))
		self.__rules[identifier] = rule

		return rule

	def generate_version(self) -> str:
		"""
		Generate today string for version.

		:return: Version string from date
		:rtype: str
		"""

		version: str | None = self.__data.version

		if not version:
			return datetime.now().strftime("%Y.%m.%d")

		points_count: int = version.count(".")

		match points_count:

			case 2:
				version += ".1"
				
			case 3:
				parts: list[str] = version.split(".")
				index: int = int(parts[-1])
				index += 1
				parts[-1] = str(index)
				version = ".".join(parts)

		return version

	def get_rule(self, rule_id: str) -> Rule:
		"""
		Search rule by ID.

		:param rule_id: Rule ID.
		:type rule_id: str
		:return: Rule.
		:rtype: Rule
		:raises KeyError: Rule not found.
		"""

		return self.__rules[rule_id]

	def is_number_correct(self, number: str) -> bool:
		"""
		Check if rule number correct and unique.

		:param number: Rule number. Must be in `x.y.z` format with optional parts.
		:type number: str
		:return: `True` if number correct and unique.
		:rtype: bool
		"""

		if not re.fullmatch(self.__regex, number):
			return False

		if number in tuple(rule.number for rule in self.__rules.values() if rule.number):
			return False

		return True

	def load(self) -> RulesFileModel:
		"""
		Load rules from file. If file not selected create empty struct.

		:return: Rules data.
		:rtype: RulesFileModel
		"""

		rules_data: RulesFileModel = RulesFileModel()

		if self.__file and self.__file.exists():
			data: dict = json.read(self.__file)
			rules_data = self.__data_adapter.validate_python(data)

		self.__rules: dict[str, Rule] = {model.id: Rule(self, model) for model in rules_data.rules}

		return rules_data

	def remove_rule(self, rule_id: str):
		"""
		Remove rule and save file.

		:param rule_id: Rule ID.
		:type rule_id: str
		:raises KeyError: Rule not found.
		"""

		del self.__rules[rule_id]
		self.save()
	
	def rename(self, name: str | None):
		"""
		Rename ruleset.

		:param name: Ruleset name.
		:type name: str | None
		"""

		self.__data.name = name

	def save(self):
		"""Save rules to file."""

		if not self.__file:
			return

		self.__data.rules = tuple(rule.model for rule in self.__rules.values())
		data: dict = self.__data_adapter.dump_python(self.__data)
		
		json.write(self.__file, data)

	def set_allowed_tags(self, tags: "Sequence[str]"):
		"""
		Set allowed tags.

		:param tags: Allowed tags.
		:type tags: Sequence[str]
		"""

		self.__data.allowed_tags = tags

	def set_description(self, description: str | None):
		"""
		Set ruleset description.

		:param description: Ruleset description.
		:type description: str | None
		"""

		self.__data.description = zerotify(description)

	def set_file_path(self, file: PathLike[str] | str):
		"""
		Set file path.

		:param file: Rules file path.
		:type file: PathLike[str] | str
		"""

		self.__file = Path(file).with_suffix(".json")
		
	def set_version(self, version: str):
		"""
		Set ruleset version.

		:param version: Ruleset version.
		:type version: str
		"""

		self.__data.version = version

	def to_dict(self) -> dict:
		"""
		Build dictionary representation of the instance.

		:return: Dictionary representation of the instance.
		:rtype: dict
		"""

		return self.__data_adapter.dump_python(self.__data)