.PHONY: lock clean

Pipfile.lock: Pipfile
	pipenv lock

requirements.txt: Pipfile.lock
	pipenv lock -r > $@

requirements-dev.txt: Pipfile.lock
	pipenv lock -r -d > $@

lock: requirements.txt requirements-dev.txt

clean:
	touch Pipfile
