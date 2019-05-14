default: test run-local

test:
	virtualenv venv && source venv/bin/activate
	pip3 install -r requirements.txt && python3 -m unittest discover

clean:
	rm -rf venv

update:
	virtualenv venv && source venv/bin/activate
	pip3 install -r requirements.txt
	zappa update

deploy:
	virtualenv venv && source venv/bin/activate
	pip3 install -r requirements.txt
	zappa deploy

run-local:
	virtualenv venv && source venv/bin/activate
	pip3 install -r requirements.txt && python3 api.py