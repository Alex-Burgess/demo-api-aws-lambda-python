# Demo API with AWS Lambda and Python


## Get Started (local Dev)
1. Start a local DynamoDB, with a table and test data:
    ```
    printf "None\nNone\nlocal\njson\n" | aws configure
    docker compose up --detach
    ```
1. Start python environment
    ```
    pyenv install 3.12.1
    pyenv virtualenv 3.12.1 test_environment
    pyenv activate test_environment
    pip install -r books/src/requirements.txt
    ```
1. Build:
    ```
    sam build
    ```
1. Run:
    ```
    sam local start-api
    ```
1. Test:
    ```
    curl http://127.0.0.1:3000/books
    ```


## Deployment
1. Export profile
    ```
    export AWS_DEFAULT_PROFILE=<Name>
    ```
1. Log in to AWS
    ```
    aws sso login --profile <Name>
    ```

## Implementation Notes
- Powertools for Event Routing (Reduce boiler plate), logging, etc. See https://docs.powertools.aws.dev/lambda/python/2.2.0/tutorial


## Useful Notes

### Manually Configure Local DynamoDB
Pull Docker Image:
```
docker run -p 8000:8000 amazon/dynamodb-local
```
Configure dummy AWS credentials
```
printf "None\nNone\nlocal\njson\n" | aws configure
```
Create DynamoDB table
```
aws dynamodb create-table --table-name Books --attribute-definitions AttributeName=id,AttributeType=S --key-schema AttributeName=id,KeyType=HASH --billing-mode PAY_PER_REQUEST --endpoint-url http://localhost:8000
```
List tables:
```
aws dynamodb list-tables --endpoint-url http://localhost:8000
```

### Manage Python Virtual Environment
See available python versions:
```
pyenv install -l
```

Install a new python version:
```
pyenv install 3.12.1
```

Create a new virtual environment:
```
pyenv virtualenv 3.12.1 test_environment
```

Active an environment:
```
pyenv activate test_environment
```

List all pythen environments:
```
pyenv virtualenvs
```

Deactivate python environment:
```
source deactivate
```

Delete python environment:
```
pyenv virtualenv-delete test_environment
```

### Manage Python Packages
Assumption is that packages will be installed in a virtual environment.

Install pip packages:
```
pip install -r requirements.txt
```

Resolve packages: Use **Command + shift + P** shortcut, type "Python: Select Interpreter" and select the virtual environment.