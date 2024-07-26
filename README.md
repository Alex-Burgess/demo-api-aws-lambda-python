# Demo API with AWS Lambda and Python


## Get Started (local Dev)
1. Start a local DynamoDB, with a table and test data:
    ```
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
    sam local start-api --docker-network dynamodb-local-network
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
1. Deployment steps...

- [ ] Add deployment steps

## Useful Notes

### Create DynamoDB Table - Option 1
- [ ] https://formulae.brew.sh/cask/nosql-workbench

### Create DynamoDB Table - Option 2
Note: To run these commands, dummy AWS credentials need to be configured.  Use:
```
printf "None\nNone\nlocal\njson\n" | aws configure
```

Create DynamoDB table:
```
aws dynamodb create-table --table-name Books --attribute-definitions AttributeName=id,AttributeType=S --key-schema AttributeName=id,KeyType=HASH --billing-mode PAY_PER_REQUEST --endpoint-url http://localhost:8000
```
List tables:
```
aws dynamodb list-tables --endpoint-url http://localhost:8000
```

### Local Network Connectivity between DynamoDB and Lambda Function Containers
- [ ] https://stackoverflow.com/questions/73557259/unable-to-connect-aws-sam-local-api-to-dynamodb-local-running-in-docker-instance

### AWS PowerTools
- [ ] Powertools for Event Routing (Reduce boiler plate), logging, etc. See https://docs.powertools.aws.dev/lambda/python/2.2.0/tutorial


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


### VSCode Settings
- Cloudformation linting
- [ ] (Note working) Boto3 - https://marketplace.visualstudio.com/items?itemName=Boto3typed.boto3-ide, https://www.tecracer.com/blog/2022/05/enable-autocomplete-for-boto3-in-vscode.html

### Developing Changes
A good workflow is to have two terminals open.  One to run the local API, and another to run tests and rebuild after changes.

Terminal 1:
```
sam local start-api --docker-network dynamodb-local-network
```

Terminal 2:
```
sam build
curl http://127.0.0.1:3000/books
```

### Testing
Get a list of all books:
```
curl http://127.0.0.1:3000/books
```

Get a book by title:
```
curl http://127.0.0.1:3000/books/The%20Pragmatic%20Programmer
```

Create a book:
```
curl --header "Content-Type: application/json" \
  --request POST \
  --data '{"title":"Scrum","author":"Jeff Sutherland","category":"Agile"}' \
  http://127.0.0.1:3000/books
```