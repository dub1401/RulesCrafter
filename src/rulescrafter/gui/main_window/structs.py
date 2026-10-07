from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
	from ..widgets.rule_editor import RuleEditor
	from ..widgets.rules_list import RulesList

@dataclass(frozen = True)
class MainWindowWidgets:
	"""Main window widgets."""

	rules_list: "RulesList"
	rule_editor: "RuleEditor"

