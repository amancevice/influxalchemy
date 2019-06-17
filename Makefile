.PHONY: clean

Pipfile.lock: Pipfile
	pipenv lock -r

clean:
	-pipenv --rm
	-rm Pipfile.lock
