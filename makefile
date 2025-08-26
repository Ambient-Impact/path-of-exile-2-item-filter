# ------------------------------------------------------------------------------
#   A custom Path of Exile 2 item filter for cool and attractive people.
# ------------------------------------------------------------------------------
#
# @see https://jinja.palletsprojects.com/en/stable/
#
# @see https://packaging.python.org/en/latest/tutorials/installing-packages/#creating-virtual-environments

filter-dir ?= "AmbientImpactItemFilter"
filter-file ?= "Ambient.Impact.filter"
archive-file ?= "$(filter-file).zip"
sounds-dir ?= "$(filter-dir)/sounds/BexBloopers"
template-dir ?= "$(filter-dir)/templates"
template-extension ?= "filter.j2"
template ?= "$(template-dir)/main.$(template-extension)"
config-file ?= "$(template-dir)/config.json"

values-root-key ?= "itemFilter"
values-file = "$(template-dir)/values.json"

tiered-schemes-key ?= "tieredSchemes"
tiered-schemes-file ?= "$(template-dir)/tiered-schemes.json"

watchlist-file ?= "$(template-dir)/watchlist.json"
watchlist-exists = $(shell test -f $(watchlist-file) && echo 1 || echo 0)

venv-dir = "$(filter-dir)/.venv"
venv-exists = $(shell test -d $(venv-dir) && echo 1 || echo 0)
bin-dir = "$(venv-dir)/bin"
jinja = "$(bin-dir)/jinja2"
jinja-installed = $(shell test -f "$(bin-dir)/jinja2" && echo 1 || echo 0)
poetry = "$(bin-dir)/poetry"
poetry-installed = $(shell test -f "$(bin-dir)/poetry" && echo 1 || echo 0)
suppress-existing-venv ?= 0
suppress-existing-poetry ?= 0
suppress-existing-jinja ?= 0

# Colour and text format output.
#
# @see https://superuser.com/questions/270214/how-can-i-change-the-colors-of-my-xterm-using-ansi-escape-sequences
#
# @see https://gitlab.com/consensus.enterprises/drumkit/-/blob/main/mk/tasks/variables.mk
#   Also inspired by Drumkit.
BOLD    = \033[1m
RED     = \033[31m
GREEN   = \033[32m
YELLOW  = \033[33m
BLUE    = \033[34m
MAGENTA = \033[35m
CYAN    = \033[36m
RESET   = \033[0m

# Commands.
ECHO    = @echo -e
ZIP     = @zip -9

.PHONY: venv-create venv-delete install-poetry install-dependencies install uninstall poetry-install poetry-lock poetry-update build-values build package

venv-create:
ifeq ($(venv-exists),0)
	$(ECHO) "▶️ Creating Python virtual environment..."
	@python3 -m venv $(venv-dir)
	$(ECHO) "$(GREEN)✅ Created Python virtual environment.$(RESET)"
else
ifneq ($(suppress-existing-venv),1)
	$(ECHO) "$(YELLOW)⚠️ Python virtual environment already exists.$(RESET)"
endif
endif

venv-delete:
ifeq ($(venv-exists),1)
	@rm -rf $(venv-dir)
	$(ECHO) "$(GREEN)✅ Python virtual environment deleted.$(RESET)"
else
	$(ECHO) "$(YELLOW)⚠️ Python virtual environment does not exist; nothing to delete.$(RESET)"
endif

install-poetry:
ifeq ($(poetry-installed),0)
	@$(MAKE) -s suppress-existing-venv=1 venv-create
	$(ECHO) "▶️ Installing Poetry into virtual environment..."
	@$(bin-dir)/pip install --upgrade pip setuptools --quiet --quiet
	@$(bin-dir)/pip install poetry --quiet --quiet
	$(ECHO) "$(GREEN)✅ Poetry installed into virtual environment.$(RESET)"
else
ifneq ($(suppress-existing-poetry),1)
	$(ECHO) "$(YELLOW)⚠️ Poetry is already installed.$(RESET)"
endif
endif

install-dependencies:
	@$(MAKE) -s suppress-existing-poetry=1 install-poetry
ifeq ($(jinja-installed),0)
	$(ECHO) "▶️ Installing dependencies into virtual environment..."
	@$(MAKE) -s poetry-install
	$(ECHO) "$(GREEN)✅ Dependencies installed into virtual environment.$(RESET)"
else
ifneq ($(suppress-existing-jinja),1)
	$(ECHO) "$(YELLOW)⚠️ Dependencies are already installed.$(RESET)"
endif
endif

# We have to activate the virtual environment to get Poetry to use it without
# messing with global configuration, etc.
#
# @see https://stackoverflow.com/questions/13702425/source-command-not-found-in-sh-shell
#   Don't use 'source' because it'll fail in our CI image.
poetry-install:
	@. $(bin-dir)/activate && $(poetry) install

poetry-update:
	@. $(bin-dir)/activate && $(poetry) update

poetry-lock:
	@. $(bin-dir)/activate && $(poetry) lock

install: install-dependencies

uninstall: venv-delete

debug-tiered-schemes:
	@$(bin-dir)/generate-poe-tiered-scheme "$(shell jq --compact-output '.$(tiered-schemes-key) | @base64' $(config-file))" --debug

# This complicated invocation of jq merges the sounds.json (nesting it under
# "sounds" automatically), config.json (as-is), and a few more values from our
# make variables.
#
# @see https://stackoverflow.com/questions/10424645/how-to-convert-a-quoted-string-to-a-normal-one-in-makefile
#   The $(shell echo $(...)) is necessary to unquote all quoted strings, which
#   will be nested in ways that would not be valid JSON.
build-values:
# Creates an empty watchlist file if one doesn't exist so jq doesn't fail.
ifeq ($(watchlist-exists),0)
	@echo "[]" > "$(watchlist-file)"
endif
	# Note that we're base64 encoding here to avoid having to account for shell
	# escaping double quotes and thus passing invalid JSON to Python. I'm tired.
	@$(bin-dir)/generate-poe-tiered-scheme "$(shell jq --compact-output '.$(tiered-schemes-key) | @base64' $(config-file))" > "$(shell echo $(tiered-schemes-file))"
	@jq --slurp '. | {"$(shell echo $(values-root-key))": {"sounds": .[0], "watchlist": .[1]}} * {"$(shell echo $(values-root-key))": .[2]} * {"$(shell echo $(values-root-key))": {"$(shell echo $(tiered-schemes-key))": .[3], "filterDir": "$(shell echo $(filter-dir))", "soundsDir": "$(shell echo $(sounds-dir))", "templateExtension": "$(shell echo $(template-extension))"}}' "$(sounds-dir)/sounds.json" "$(watchlist-file)" "$(config-file)" "$(shell echo $(tiered-schemes-file))" > "$(values-file)"

build:
	@$(MAKE) -s suppress-existing-venv=1 suppress-existing-jinja=1 install
	@$(MAKE) -s build-values
	@$(jinja) --outfile="$(filter-file)" "$(template)" "$(values-file)" --format=json
	$(ECHO) "$(GREEN)✅ Item filter built:$(RESET) $(filter-file)"

package:
	$(ZIP) $(archive-file) $(filter-file) license.md readme.md
	$(ZIP) $(archive-file) `find "$(sounds-dir)" \( -name "*.mp3" -o -name "*.md" \) -print`
	$(ECHO) "$(GREEN)✅ Package built:$(RESET) $(archive-file)"

# If invoked without a goal, default to build.
.DEFAULT_GOAL := build
