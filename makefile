# ------------------------------------------------------------------------------
#   Ambient.Impact's Path of Exile 2 item filter for cool and attractive people.
# ------------------------------------------------------------------------------
#
# @see https://jinja.palletsprojects.com/en/stable/
#
# @see https://packaging.python.org/en/latest/tutorials/installing-packages/#creating-virtual-environments

filter-dir ?= "AmbientImpactItemFilter"
outfile ?= "Ambient.Impact.filter"
sounds-dir ?= "$(filter-dir)/sounds/BexBloopers"
template-dir ?= "$(filter-dir)/templates"
template ?= "$(template-dir)/main.j2"

venv-dir = "$(filter-dir)/.venv"
venv-exists = $(shell test -d $(venv-dir) && echo 1 || echo 0)
bin-dir = "$(venv-dir)/bin"
jinja = "$(bin-dir)/jinja2"
jinja-installed = $(shell test -f "$(bin-dir)/jinja2" && echo 1 || echo 0)
suppress-existing-venv ?= 0
suppress-existing-jinja ?= 0

# Colour output. Copied from Drumkit:
#
# @see https://superuser.com/questions/270214/how-can-i-change-the-colors-of-my-xterm-using-ansi-escape-sequences
#
# @see https://gitlab.com/consensus.enterprises/drumkit/-/blob/main/mk/tasks/variables.mk
#   Also inspired by Drumkit.
ECHO    = @echo -e
BOLD    = \033[1m
RED     = \033[31m
GREEN   = \033[32m
YELLOW  = \033[33m
BLUE    = \033[34m
MAGENTA = \033[35m
CYAN    = \033[36m
RESET   = \033[0m

.PHONY: venv-create venv-delete jinja-install install uninstall build

venv-create:
ifeq ($(venv-exists),0)
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

jinja-install:
	@$(MAKE) -s suppress-existing-venv=1 venv-create
ifeq ($(jinja-installed),0)
	@$(bin-dir)/pip install jinja2-cli --quiet --quiet
	$(ECHO) "$(GREEN)✅ Jinja installed into virtual environment.$(RESET)"
else
ifneq ($(suppress-existing-jinja),1)
	$(ECHO) "$(YELLOW)⚠️ Jinja is already installed.$(RESET)"
endif
endif

install: jinja-install

uninstall: venv-delete

build:
	@$(MAKE) -s suppress-existing-venv=1 suppress-existing-jinja=1 install
	@$(jinja) --outfile=$(outfile) $(template) -D filterDir=$(filter-dir) -D soundsDir=$(sounds-dir) $(sounds-dir)/sounds.json --format=json
	$(ECHO) "$(GREEN)✅ Item filter built:$(RESET) $(outfile)"

# @see https://stackoverflow.com/a/30176470
.DEFAULT_GOAL := build
