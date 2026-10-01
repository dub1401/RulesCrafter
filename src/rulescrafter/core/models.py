from collections.abc import Sequence

from pydantic import BaseModel

class RuleModel(BaseModel):
	"""Rule data."""

	id: str
	number: str | None = None
	header: str | None = None
	description: str | None = None
	tags: Sequence[str] = ()

class RulesFileModel(BaseModel):
	"""Rules file model."""

	version: str | None = None
	name: str | None = None
	description: str | None = None
	allowed_tags: Sequence[str] = ()
	rules: Sequence[RuleModel] = ()
