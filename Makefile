default: build package deploy

build:
	sam build --use-container

clean:
	rm -f ./handler.zip
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
	cd colors_api && pip3 install -r requirements.txt && python3 colors.py