# Flask / Flasgger

## Requirements

- python3.7+
- pip3
- AWS CLI
- SAM CLI
- virtualenv
- [Flask](http://flask.pocoo.org/)

## Local Development

```
make run-local
```

Navigate to `http://localhost:5000/apidocs/` in the browser for Docs.

Example call:
Enter `http://127.0.0.1:5000/colors/all/` in the browser.

## Packaging and deployment

An S3 bucket must be created before deployment to hold the lambda code:

```
aws s3 mb s3://BUCKET_NAME
```

Set the follow environment variables:
```
export S3_BUCKET=
export STACK_NAME=
```

```
make
```