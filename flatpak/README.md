# Build Flatpak modules
1. Install [uv](https://docs.astral.sh/uv/) project manager on your system.
2. Clone this repository.
```Bash
git clone https://github.com/dub1401/RulesCrafter
cd RulesCrafter
```
3. Install dependencies.
```Bash
uv venv .venv --prompt rulescrafter
uv pip install .[flatpak]
```
4. Run modules building script.
```Bash
flatpak/modules.sh
```
