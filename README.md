# Flask API with AWS API Gateway (Lambda proxy)

## Requirements

- python3.7
- pip3
- AWS CLI
- AWS profile configured with Admin access
- virtualenv
- [Flask](http://flask.pocoo.org/)
- [Zappa](https://github.com/Miserlou/Zappa)

## Overview

The API uses Zappa to host a Flask app in a lambda function using AWS API Gateway proxy integration.

It uses Flasgger to host an `openapi 3.0` schema document from the Lambda function. Custom schema validation of API 
request bodies against schema components is achieved in the `api_utils` module.

## Local Development

#### Unit tests
```
make run-tests
```

#### Manual testing
```
make
```

Navigate to `http://localhost:5000/apidocs/` in the browser for Docs.

Example call:  
Enter `http://127.0.0.1:5000/users/1/` in the browser.

## Packaging and deployment

The repo uses [Zappa](https://github.com/Miserlou/Zappa) to package and deploy the API. 

Run the following command to initialize the deployment:

```
# Activate virtualenv and install project dependencies
make install

# Create the zappa_settings.json file needed for deployment
zappa init

# Deploy stack to AWS with zappa
zappa deploy

# Update stack
zappa update
```

## Clean up deployment resources

```
make clean
```