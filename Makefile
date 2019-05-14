default: install test run-local

activate:
	virtualenv venv && source venv/bin/activate

install: activate
	pip3 install -r requirements.txt

test:
	python3 -m unittest discover

run-tests: install
	python3 -m unittest discover

clean:
	rm -rf venv

update: install
	zappa update

deploy: install
	zappa deploy

run-local:
	python3 api.py