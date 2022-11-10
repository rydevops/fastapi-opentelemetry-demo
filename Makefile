VENV_FOLDER := venv
PYTHON_BIN := ./venv/bin/python
ASYNC_SERVER := uvicorn
APP_PATH := poc.application:app

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
	$(PYTHON_BIN) -m $(ASYNC_SERVER) $(APP_PATH) --reload

add_dep:
	$(PYTHON_BIN) -m pip install $(PACKAGES)

test:
	$(PYTHON_BIN) -m pytest ./