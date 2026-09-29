import re
import uuid
from datetime import datetime
from os import PathLike
from pathlib import Path

from pydantic import TypeAdapter

from dublib.functions.filesystem import json

from .models import RuleModel, RulesFileModel
from .rule import Rule

class RulesOperator:
	"""Rules operator."""

	@property
	def allowed_tags(self) -> list[str]:
		"""Allowed tags."""

		return self.__data.allowed_tags.copy()

	@property
	def file(self) -> Path | None:
		"""Rules file path."""

		return self.__file

	@property
	def rules(self) -> tuple[Rule, ...]:
		"""Rules."""

		return tuple(self.__rules.values())

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

	def __get_version_string(self) -> str:
		"""
		Generate today string for version.

		:return: Version string from date
		:rtype: str
		"""

		return datetime.now().strftime("%Y.%m.%d")

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
	
	def save(self):
		"""Save rules to file."""

		if not self.__file:
			return

		self.__data.rules = tuple(rule.model for rule in self.__rules.values())
		data: dict = self.__data_adapter.dump_python(self.__data)
		
		json.write(self.__file, data)

	def set_file_path(self, file: PathLike[str] | str):
		"""
		Set file path.

		:param file: Rules file path.
		:type file: PathLike[str] | str
		"""

		self.__file = Path(file).with_suffix(".json")

		