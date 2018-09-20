VENV ?= ./.virtualenv

install:
	python3 -m venv $(VENV) && \
	$(VENV)/bin/pip install -r requirements.txt

run:
	$(VENV)/bin/python3 ./run_asyncio_import.py

run-sync:
	$(VENV)/bin/python3 ./run_asyncio_import.py --sync
