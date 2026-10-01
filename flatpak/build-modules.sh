flatpak_pip_generator \
	--pyproject-file pyproject.toml \
	--runtime org.kde.Sdk//6.11 \
	--prefer-wheels $(paste -sd, flatpak/wheels.txt) \
	--ignore-pkg $(paste -sd, flatpak/ignore.txt) \
	--optdep-groups flatpak \
	--output flatpak/python3-modules.json
