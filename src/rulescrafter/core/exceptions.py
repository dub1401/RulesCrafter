class NoRulesetError(Exception):
	"""Exception: ruleset not opened."""

	def __init__(self):
		"""Exception: ruleset not opened."""

		super().__init__("Ruleset required, but not opened.")