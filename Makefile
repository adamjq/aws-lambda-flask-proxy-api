default: validate build

validate:
	sam validate

build:
	sam build --use-container

test:
	python -m unittest discover

clean:
	rm -rf .aws-sam
	rm -rf venv
	rm -f ./packaged.yaml

package:
	echo "package stack to S3 bucket ${S3_BUCKET}..."
	sam package \
    	--output-template-file packaged.yaml \
    	--s3-bucket ${S3_BUCKET}

deploy:
	echo "deploy stack ${STACK_NAME}..."
	sam deploy \
    	--template-file packaged.yaml \
    	--stack-name ${STACK_NAME} \
    	--capabilities CAPABILITY_IAM

run-local:
	virtualenv venv && source venv/bin/activate
	cd users && pip3 install -r requirements.txt && python3 users.py

deploy-stack: validate build package deploy