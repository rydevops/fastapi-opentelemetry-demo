VENV_FOLDER := venv
PYTHON_BIN := ./venv/bin/python
OTEL_BIN := ./venv/bin/opentelemetry-instrument
UVICORN_BIN := ./venv/bin/uvicorn
COVERAGE_BIN := ./venv/bin/coverage
APP_PATH := poc.application:app
LISTEN_ADDR := 0.0.0.0
UVICORN_WORKERS := 1

all: _clear_screen init

_clear_screen:
	clear

init: clean _config_pyenv _install_requirements
	$(info Initialization successfully completed!)

_config_pyenv:
	$(info Creating Virtual Environment...)
	@python3 -m venv $(VENV_FOLDER)

	$(info Upgrading PIP within Virtual Environment...)
	@$(PYTHON_BIN) -m pip install -U pip

_install_requirements: 
	@if [ -f requirements.txt ]; then \
		$(info Installing PIP dependencies...) \
		$(PYTHON_BIN) -m pip install -r requirements.txt; \
	fi

clean:
	$(info Removing Virtual Environment...)
	@rm -rf ./$(VENV_FOLDER)

freeze:
	$(info Updating dependency tree...)
	$(PYTHON_BIN) -m pip freeze > requirements.txt

run: _clear_screen
	$(OTEL_BIN) --traces_exporter=console --log_level=debug --metrics_exporter=console $(UVICORN_BIN) $(APP_PATH) --host=$(LISTEN_ADDR) --workers=$(UVICORN_WORKERS)

add_dep:
	$(PYTHON_BIN) -m pip install $(PACKAGES)

test:
	$(COVERAGE_BIN) run -m pytest ./
	$(COVERAGE_BIN) report

report:
	$(COVERAGE_BIN) run -m pytest ./
	$(COVERAGE_BIN) html