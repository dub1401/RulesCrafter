RUNTIME="org.kde.Sdk//6.11"

flatpak install "$RUNTIME" --user

flatpak_pip_generator \
	--pyproject-file pyproject.toml \
	--runtime "$RUNTIME" \
	--prefer-wheels $(paste -sd, flatpak/wheels.txt) \
	--ignore-pkg $(paste -sd, flatpak/ignore.txt) \
	--optdep-groups build \
	--output flatpak/python3-modules.json
