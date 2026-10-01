from importlib import resources

from PyQt6.QtGui import QIcon

CLOSE = QIcon(str(resources.files("rulescrafter.gui.icons") / "close.svg"))
DUMP = QIcon(str(resources.files("rulescrafter.gui.icons") / "dump.svg"))
GITHUB = QIcon(str(resources.files("rulescrafter.gui.icons") / "github.svg"))
NEW = QIcon(str(resources.files("rulescrafter.gui.icons") / "new.svg"))
OPEN = QIcon(str(resources.files("rulescrafter.gui.icons") / "open.svg"))
SAVE = QIcon(str(resources.files("rulescrafter.gui.icons") / "save.svg"))
SAVE_AS = QIcon(str(resources.files("rulescrafter.gui.icons") / "save_as.svg"))
TAGS = QIcon(str(resources.files("rulescrafter.gui.icons") / "tags.svg"))
