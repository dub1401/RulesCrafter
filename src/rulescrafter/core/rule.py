from typing import TYPE_CHECKING

from packaging.version import Version

from .models import RuleModel

if TYPE_CHECKING:
	from collections.abc import Sequence

	from .operator import RulesOperator

_Number = Version

class Rule:
	"""Rule."""

	@property
	def description(self) -> str | None:
		"""Rule description."""

		return self.__model.description

	@property
	def header(self) -> str | None:
		"""Rule header."""

		return self.__model.header

	@property
	def id(self) -> str:
		"""Rule ID."""

		return self.__model.id

	@property
	def indexable_string(self) -> str:
		"""Indexable rule string: number, header and description in one."""

		number: str = self.__model.number or ""
		header: str = self.__model.header or ""
		description: str = self.__model.description or ""

		return " ".join((number, header, description))

	@property
	def model(self) -> RuleModel:
		"""Rule data model."""

		return self.__model

	@property
	def number(self) -> str | None:
		"""Rule number."""

		return self.__model.number

	@property
	def parsed_number(self) -> _Number | None:
		"""Rule parsed number."""

		return _Number(self.__model.number) if self.__model.number else None

	@property
	def tags(self) -> tuple[str, ...]:
		"""Rule tags."""

		return tuple(self.__model.tags)

	@property
	def title(self) -> str:
		"""Rule title."""

		number: str = self.__model.number or ""
		header: str = self.__model.header or ""

		if not number and not header:
			return self.__model.id

		separator: str = ". " if number and header else ""

		return f"{number}{separator}{header}"

	def __init__(self, operator: "RulesOperator", model: RuleModel):
		"""
		Rule.

		:param operator: Rules operator.
		:type operator: RulesOperator
		:param model: Rule model.
		:type model: RuleModel
		"""

		self.__operator: RulesOperator = operator
		self.__model: RuleModel = model

	def set_description(self, description: str | None):
		"""
		Set rule description.

		:param description: Rule description.
		:type description: str | None
		"""

		self.__model.description = description

	def set_header(self, header: str | None):
		"""
		Set rule header.

		:param header: Rule header.
		:type header: str | None
		"""

		self.__model.header = header

	def set_number(self, number: str | None):
		"""
		Set rule number.

		:param number: Rule number. Must be in `x.y.z` format with optional parts.
		:type number: str | None
		"""

		if number == self.__model.number:
			return

		if not number:
			self.__model.number = number
			return

		if not self.__operator.is_number_correct(number):
			raise ValueError("Rule number must be unique in `x.y.z` format with optional parts.")

		self.__model.number = number

	def set_tags(self, tags: "Sequence[str]"):
		"""
		Set tags.

		:param tags: Tags sequence.
		:type tags: str
		:raises ValueError: Unknown tag.
		"""

		for tag in tags:
			if tag not in self.__operator.allowed_tags:
				raise ValueError(tag)

		self.__model.tags = tags
