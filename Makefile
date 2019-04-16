.PHONY: lock

Pipfile.lock: Pipfile
	pipenv lock
	pipenv lock -r > requirements.txt
	pipenv lock -r -d > requirements-dev.txt

lock: Pipfile.lock
