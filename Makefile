SYSTEMPYTHON = `which python2.7 python2 python | head -n 1`
VIRTUALENV = virtualenv --python=$(SYSTEMPYTHON)
ENV = ./local
INSTALL = $(ENV)/bin/pip install

.PHONY: all
all: build

.PHONY: build
build: | $(ENV)/COMPLETE
$(ENV)/COMPLETE: requirements.txt
	$(VIRTUALENV) --no-site-packages $(ENV)
	$(INSTALL) -r requirements.txt
	$(ENV)/bin/python ./setup.py develop
	touch $(ENV)/COMPLETE

.PHONY: serve
serve: | $(ENV)/COMPLETE
        $(ENV)/bin/python ./manage.py runserver 0.0.0.0:3141

.PHONY: clean
clean:
	rm -rf $(ENV)
