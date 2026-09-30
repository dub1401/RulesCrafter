flatpak_pip_generator \
	--pyproject-file pyproject.toml \
	--runtime org.kde.Sdk//6.11 \
	--prefer-wheels $(paste -sd, flatpak/wheels.txt) \
	--ignore-pkg flatpak_pip_generator,pyqt6 \
	--optdep-groups flatpak \
	--output flatpak/python3-modules.json
