# Makefile for Odoo module development
# Adjust variables below to match your environment and module technical name.

MODULE ?= library_management                   # change to your module's technical name
VENV_DIR ?= .venv
PY ?= python3
ODOO_BIN ?= $(VENV_DIR)/bin/odoo-bin
REQ_FILE ?= requirements.txt
CONFIG ?= odoo.conf
DB ?= odoo_db
ADDONS_PATH ?= addons,.
PORT ?= 8069

.PHONY: help init venv install-deps run upgrade test lint fmt clean

help:
	@echo "Makefile for Odoo module development"
	@echo ""
	@echo "Usage: make <target> [VAR=value]"
	@echo ""
	@echo "Common targets:"
	@echo "  init               Create virtualenv and install requirements"
	@echo "  venv               Create virtualenv only"
	@echo "  install-deps       Install pip deps from $(REQ_FILE)"
	@echo "  run                Run Odoo server (use CONFIG/ADDONS_PATH/DB)"
	@echo "  upgrade            Upgrade MODULE (make upgrade MODULE=your_module)"
	@echo "  test               Run module tests (make test MODULE=your_module)"
	@echo "  lint               Run linters (flake8 and pylint if installed)"
	@echo "  fmt                Format code with black"
	@echo "  clean              Remove python caches and build artifacts"
	@echo ""
	@echo "Environment overrides: MODULE, VENV_DIR, ODOO_BIN, CONFIG, DB, ADDONS_PATH, PORT"

venv:
	@test -d $(VENV_DIR) || $(PY) -m venv $(VENV_DIR)
	@echo "Virtualenv created at $(VENV_DIR)"

install-deps: venv
	@echo "Installing pip requirements from $(REQ_FILE) (if present)"
	@test -f $(REQ_FILE) && $(VENV_DIR)/bin/pip install -r $(REQ_FILE) || echo "no requirements.txt found, skipping"

init: venv install-deps
	@echo "Initialization complete. Activate with: . $(VENV_DIR)/bin/activate"

run:
	@echo "Starting Odoo (port=$(PORT), db=$(DB))"
	$(ODOO_BIN) -c $(CONFIG) --db_host= --db_port= --db_user= --db_password= --addons-path=$(ADDONS_PATH) -d $(DB) --http-port=$(PORT)

upgrade:
ifndef MODULE
	$(error MODULE is not set. Usage: make upgrade MODULE=your_module)
endif
	@echo "Upgrading module $(MODULE) on DB=$(DB)"
	$(ODOO_BIN) -c $(CONFIG) --addons-path=$(ADDONS_PATH) -d $(DB) -u $(MODULE) --stop-after-init

test:
ifndef MODULE
	$(error MODULE is not set. Usage: make test MODULE=your_module)
endif
	@echo "Running Odoo tests for $(MODULE) (DB=$(DB))"
	$(ODOO_BIN) -c $(CONFIG) --addons-path=$(ADDONS_PATH) -d $(DB) -u $(MODULE) --test-enable --stop-after-init

lint:
	@echo "Running linters (if available)"
	@test -x $(VENV_DIR)/bin/flake8 && $(VENV_DIR)/bin/flake8 $(MODULE) || echo "flake8 not installed or no flake8 configuration"
	@test -x $(VENV_DIR)/bin/pylint && $(VENV_DIR)/bin/pylint $(MODULE) || echo "pylint not installed or no pylint configuration"

fmt:
	@echo "Formatting module with black (if available)"
	@test -x $(VENV_DIR)/bin/black && $(VENV_DIR)/bin/black $(MODULE) || echo "black not installed, skipping"

clean:
	@echo "Cleaning python caches and build artifacts"
	-find . -type f -name "*.pyc" -delete || true
	-find . -type d -name "__pycache__" -exec rm -rf {} + || true
	-rm -rf build dist *.egg-info || true
