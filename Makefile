SDIST := dist/$(shell python setup.py --fullname).tar.gz

.PHONY: default clean upload

default: $(SDIST)

clean:
	rm -rf dist

upload: $(SDIST)
	twine upload $<

$(SDIST):
	python setup.py sdist
