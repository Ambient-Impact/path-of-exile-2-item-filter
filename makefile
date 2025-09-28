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
sounds-dir ?= "sounds"
template-dir ?= "templates"
template-extension ?= "filter.j2"
template ?= "$(template-dir)/main.$(template-extension)"
config-file ?= "config.json"

build-dir ?= "build"

values-root-key ?= "itemFilter"
values-file = "$(build-dir)/values.json"

sounds-build-file ?= "$(build-dir)/sounds.json"

sound-packs-raw-build-file ?= "$(build-dir)/sound-packs-raw.json"
sound-packs-build-file ?= "$(build-dir)/sound-packs.json"

sound-mix-build-file ?= "$(build-dir)/sound-mix.json"

tiered-schemes-key ?= "tieredSchemes"
tiered-schemes-file ?= "$(build-dir)/tiered-schemes.json"

watchlist-file ?= "watchlist.json"
watchlist-exists = $(shell test -f $(watchlist-file) && echo 1 || echo 0)

venv-dir = ".venv"
venv-exists = $(shell test -d $(venv-dir) && echo 1 || echo 0)
bin-dir = "$(venv-dir)/bin"
jinja = "$(bin-dir)/jinja2"
jinja-installed = $(shell test -f "$(jinja)" && echo 1 || echo 0)

poetry-venv-dir = ".poetry-venv"
poetry-venv-exists = $(shell test -d $(poetry-venv-dir) && echo 1 || echo 0)
poetry = "$(poetry-venv-dir)/bin/poetry"
poetry-installed = $(shell test -f "$(poetry)" && echo 1 || echo 0)

suppress-existing-venv ?= 0
suppress-existing-poetry ?= 0
suppress-existing-poetry-venv ?= 0
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

BREAK		= \n

# Commands.
ECHO    = @printf
ZIP     = @zip -9

.PHONY: venv-create
venv-create:
ifeq ($(venv-exists),0)
	$(ECHO) "⏳ Creating Python virtual environment...$(BREAK)"
	@python3 -m venv $(venv-dir)
	$(ECHO) "$(GREEN)✅ Created Python virtual environment.$(RESET)$(BREAK)"
else
ifneq ($(suppress-existing-venv),1)
	$(ECHO) "$(YELLOW)⚠️ Python virtual environment already exists.$(RESET)$(BREAK)"
endif
endif

.PHONY: venv-delete
venv-delete:
ifeq ($(venv-exists),1)
	@rm -rf $(venv-dir)
	$(ECHO) "$(GREEN)✅ Python virtual environment deleted.$(RESET)$(BREAK)"
else
	$(ECHO) "$(YELLOW)⚠️ Python virtual environment does not exist; nothing to delete.$(RESET)$(BREAK)"
endif

# Poetry stresses the importance of installing it to its own dedicated virtual
# environment so that there's no risk of a project that it manages upgrading or
# uninstalling one of Poetry's own dependencies.
#
# @see https://python-poetry.org/docs/#installation
.PHONY: install-poetry
install-poetry:
ifeq ($(poetry-installed),0)
	$(ECHO) "⏳ Creating Poetry virtual environment...$(BREAK)"
	@python3 -m venv $(poetry-venv-dir)
	$(ECHO) "$(GREEN)✅ Created Poetry virtual environment.$(RESET)$(BREAK)"
	$(ECHO) "⏳ Installing Poetry into virtual environment...$(BREAK)"
	@$(poetry-venv-dir)/bin/pip install --upgrade pip setuptools --quiet --quiet
	@$(poetry-venv-dir)/bin/pip install poetry --quiet --quiet
	$(ECHO) "$(GREEN)✅ Poetry installed into virtual environment.$(RESET)$(BREAK)"
else
ifneq ($(suppress-existing-poetry),1)
	$(ECHO) "$(YELLOW)⚠️ Poetry is already installed.$(RESET)$(BREAK)"
endif
endif

.PHONY: uninstall-poetry
uninstall-poetry:
ifeq ($(poetry-venv-exists),1)
	@rm -rf $(poetry-venv-dir)
	$(ECHO) "$(GREEN)✅ Poetry virtual environment deleted.$(RESET)$(BREAK)"
else
ifneq ($(suppress-existing-poetry-venv),1)
	$(ECHO) "$(YELLOW)⚠️ Poetry virtual environment does not exist; nothing to delete.$(RESET)$(BREAK)"
endif
endif

.PHONY: install-dependencies
install-dependencies:
	@$(MAKE) -s suppress-existing-poetry=1 install-poetry
	@$(MAKE) -s suppress-existing-venv=1 venv-create
ifeq ($(jinja-installed),0)
	$(ECHO) "⏳ Installing dependencies into virtual environment...$(BREAK)"
	@$(MAKE) -s poetry-install
	$(ECHO) "$(GREEN)✅ Dependencies installed into virtual environment.$(RESET)$(BREAK)"
else
ifneq ($(suppress-existing-jinja),1)
	$(ECHO) "$(YELLOW)⚠️ Dependencies are already installed.$(RESET)$(BREAK)"
endif
endif

# We have to activate the virtual environment to get Poetry to use it without
# messing with global configuration, etc.
#
# @see https://stackoverflow.com/questions/13702425/source-command-not-found-in-sh-shell
#   Don't use 'source' because it'll fail in our CI image.
.PHONY: poetry-install
poetry-install:
	@. $(bin-dir)/activate && $(poetry) install

.PHONY: poetry-update
poetry-update:
	@. $(bin-dir)/activate && $(poetry) update

.PHONY: poetry-lock
poetry-lock:
	@. $(bin-dir)/activate && $(poetry) lock

.PHONY: install
install: install-dependencies

.PHONY: uninstall
uninstall: venv-delete uninstall-poetry

.PHONY: debug-tiered-schemes
debug-tiered-schemes:
	@$(bin-dir)/generate-poe-tiered-scheme "$(shell jq --compact-output '.$(tiered-schemes-key) | @base64' $(config-file))" --debug

.PHONY: build-sound-packs
build-sound-packs:
	@# This loads all sounds.json files it finds, merging in the directory path
	@# for each sound pack.
	@find "$(shell echo $(sounds-dir))" -type f -name "sounds.json" -print0 | xargs -0 dirname -z | xargs -0 --replace jq --arg path {} '. * {"path": $(shell echo $)path}' {}/sounds.json > "$(shell echo $(sound-packs-raw-build-file))"
	@# This merges all the objects in the previous file into a single object
	@# containing each object keyed by its pack ID. The reason that we need to
	@# generate a second file is that reading and directing output to the same
	@# file usually results in that file being empty.
	@#
	@# @see https://github.com/jqlang/jq/issues/2152#issuecomment-653634999
	@jq --slurp '. | with_entries(.key = .value.id)' "$(shell echo $(sound-packs-raw-build-file))" > "$(shell echo $(sound-packs-build-file))"

# This is a separate target from build-sound-packs to fix headaches with
# sub-shells where this would not have sound-packs-build-file created by the
# time we call the Python script. Having it as a separate target that's a
# dependency of this one ensures that's run in full before we pass it off to
# Python.
.PHONY: build-sound-mix
build-sound-mix: build-sound-packs
	@$(bin-dir)/generate-poe-sound-mix "$(shell jq --slurp '. | {"soundPacks": .[0], "$(shell echo $(tiered-schemes-key))": .[1].$(shell echo $(tiered-schemes-key)), "destinationDir": "$(shell echo $(filter-dir))"} | @base64' "$(shell echo $(sound-packs-build-file))" "$(shell echo $(config-file))")" > "$(shell echo $(sound-mix-build-file))"

# This complicated invocation of jq merges the sounds.json (nesting it under
# "sounds" automatically), config.json (as-is), and a few more values from our
# make variables.
#
# @see https://stackoverflow.com/questions/10424645/how-to-convert-a-quoted-string-to-a-normal-one-in-makefile
#   The $(shell echo $(...)) is necessary to unquote all quoted strings, which
#   will be nested in ways that would not be valid JSON.
.PHONY: build-values
build-values: build-sound-mix
# Creates an empty watchlist file if one doesn't exist so jq doesn't fail.
ifeq ($(watchlist-exists),0)
	@echo "[]" > "$(watchlist-file)"
endif
	@ # Note that we're base64 encoding here to avoid having to account for shell
	@ # escaping double quotes and thus passing invalid JSON to Python. I'm tired.
	@$(bin-dir)/generate-poe-tiered-scheme "$(shell jq --compact-output '.$(tiered-schemes-key) | @base64' $(config-file))" > "$(shell echo $(tiered-schemes-file))"
	@jq --slurp '. | {"$(shell echo $(values-root-key))": {"watchlist": .[0]}} * {"$(shell echo $(values-root-key))": .[1]} * {"$(shell echo $(values-root-key))": {"$(shell echo $(tiered-schemes-key))": .[2], "filterDir": "$(shell echo $(filter-dir))", "templateExtension": "$(shell echo $(template-extension))"}} * {"$(shell echo $(values-root-key))": {"$(shell echo $(tiered-schemes-key))": .[3]}}' "$(watchlist-file)" "$(config-file)" "$(shell echo $(sound-mix-build-file))" "$(shell echo $(tiered-schemes-file))" > "$(values-file)"

.PHONY: build
build:
	@$(MAKE) -s suppress-existing-venv=1 suppress-existing-jinja=1 install
	@$(MAKE) -s build-values
	@$(jinja) --outfile="$(build-dir)/$(filter-file)" "$(template)" "$(values-file)" --format=json
	$(ECHO) "$(GREEN)✅ Item filter built:$(RESET) $(filter-file)$(BREAK)"

.PHONY: package
package:
	$(ZIP) $(archive-file) $(filter-file) license.md readme.md
	$(ZIP) $(archive-file) `find "$(sounds-dir)" \( -name "*.mp3" -o -name "*.md" \) -print`
	$(ECHO) "$(GREEN)✅ Package built:$(RESET) $(archive-file)$(BREAK)"

# If invoked without a goal, default to build.
.DEFAULT_GOAL := build
