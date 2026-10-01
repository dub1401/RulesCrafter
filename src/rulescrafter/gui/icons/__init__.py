from importlib import resources

from PyQt6.QtGui import QIcon

with resources.path("rulescrafter.gui.icons", "close.svg") as image:
	CLOSE = QIcon(str(image))

with resources.path("rulescrafter.gui.icons", "dump.svg") as image:
	DUMP = QIcon(str(image))

with resources.path("rulescrafter.gui.icons", "github.svg") as image:
	GITHUB = QIcon(str(image))

with resources.path("rulescrafter.gui.icons", "new.svg") as image:
	NEW = QIcon(str(image))

with resources.path("rulescrafter.gui.icons", "open.svg") as image:
	OPEN = QIcon(str(image))

with resources.path("rulescrafter.gui.icons", "save.svg") as image:
	SAVE = QIcon(str(image))

with resources.path("rulescrafter.gui.icons", "save_as.svg") as image:
	SAVE_AS = QIcon(str(image))

with resources.path("rulescrafter.gui.icons", "tags.svg") as image:
	TAGS = QIcon(str(image))
