# Variablen
PYTHON_FILES := $(shell find . -type f -name "*.py" -not -path "./venv/*")
YAML_FILES := $(shell find . -type f -name "*.yml" -o -name "*.yaml")

# Projekt vorbereiten
prepare:
	@if [ "$(word 2,$(MAKECMDGOALS))" = "" ]; then \
		echo "Bitte Python-Version angeben: make prepare 3.12.4"; \
		exit 1; \
	fi
	@echo "Erstelle pyenv-Umgebung mit Python $(word 2,$(MAKECMDGOALS))..."
	pyenv virtualenv $(word 2,$(MAKECMDGOALS)) study-env
	~/.pyenv/versions/study-env/bin/pip install pip-tools
	~/.pyenv/versions/study-env/bin/pip-compile requirements.in
	~/.pyenv/versions/study-env/bin/pip install -r requirements.txt
	sudo docker-compose up -d

# make pre-commit Befehl erstellen
.PHONY: pre-commit
pre-commit: format-python fix-python fix-yaml update-requirements sync-dependencies
	@echo "Pre-commit erfolgreich!"

# Automatisch python Probleme fixen (flake8 mit autoflake + black + isort)
.PHONY: fix-python
fix-python:
	@echo "Python Probleme lösen..."
	autoflake --in-place --remove-unused-variables --remove-all-unused-imports --recursive $(PYTHON_FILES)
	black $(PYTHON_FILES)
	isort $(PYTHON_FILES)

# Automatisch yaml Probleme fixen
.PHONY: fix-yaml
fix-yaml:
	@echo "Yaml Probleme lösen..."
	yamlfmt -w $(YAML_FILES)

# Update requirements.txt
.PHONY: update-requirements
update-requirements:
	@echo "Updating requirements.txt mit der aktuellen requirements.in..."
	pip-compile requirements.in

# Synchronisierung mit der requirements.txt
.PHONY: sync-dependencies
sync-dependencies:
	@echo "Synchronisierung der Abhängigkeiten aus der requirements.txt..."
	pip-sync requirements.txt

# Alle Formatter und Prüfungen laufen lassen
.PHONY: format-python
format-python:
	@echo "Ausführung der Python Formatter (black + isort)..."
	black $(PYTHON_FILES)
	isort $(PYTHON_FILES)

# Optional
.PHONY: check-python
check-python:
	@echo "Ausführung des Pyhton Syntax-Prüfers (flake8)..."
	flake8 $(PYTHON_FILES)

.PHONY: check-yaml
check-yaml:
	@echo "Ausführung des YAML Syntax-Prüfers(yamllint)..."
	yamllint $(YAML_FILES)
