# Demo API with AWS Lambda and Python
This application demonstrates a simple CRUD API which manages a table of books using a serverless architecture model on AWS. This demonstrates the following concepts:

- [AWS Serverless Application Model (SAM)](https://aws.amazon.com/serverless/sam/) to simplify the configuration and development of API services.
- [Powertools for AWS Lambda (Python)](https://docs.powertools.aws.dev/lambda/python/latest/) developer toolkit to implement best practices.
- [AWS SDK for Python (boto3)](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html) to implement CRUD operations against DynamoDB.
- Docker to develop and test the API locally.
- Integration with OpenAPI to make documentation
- Unit and integration testing
- GitHub Actions to implement a CI/CD pipeline to deploy the API to AWS.


**Contents:**
- [Prerequisites](#prerequisites)
- [Getting Started](#getting-started)
- [Best Practices with PowerTools](#best-practices-with-powertools)
- [Developing the Application](#developing-the-application)
- [Testing](#testing)
- [Deployment](#deployment)


## Prerequisites
The following tools are used to build and deploy the application:
- [SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html)
- [Python](https://www.python.org/downloads/) & [Pyenv](https://github.com/pyenv/pyenv)
- [Docker](https://hub.docker.com/search/?type=edition&offering=community)
- [NoSQL Workbench](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/workbench.html) installed from [Homebrew](https://formulae.brew.sh/cask/nosql-workbench)


## Getting Started
- [ ] Follow steps to initialise project with AWS SAM...
1. Start a local DynamoDB instance using the [Docker compose file](/compose.yaml):
    ```
    docker compose up --detach
    ```
1. Create table
1. Create test data
1. Start python environment
    ```
    pyenv install 3.12.1
    pyenv virtualenv 3.12.1 test_environment
    pyenv activate test_environment
    pip install -r bboks/requirements.txt
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


## Best Practices with PowerTools
- [ ] Powertools for Event Routing (Reduce boiler plate), logging, etc. See https://docs.powertools.aws.dev/lambda/python/2.2.0/tutorial
Routing, Logging, tracing, metrics.

## Developing the Application


### VSCode Settings
Resolve packages: Use **Command + shift + P** shortcut, type "Python: Select Interpreter" and select the virtual environment.

- Cloudformation linting
- [ ] (Note working) Boto3 - https://marketplace.visualstudio.com/items?itemName=Boto3typed.boto3-ide, https://www.tecracer.com/blog/2022/05/enable-autocomplete-for-boto3-in-vscode.html

### Local Network Connectivity between DynamoDB and Lambda Function Containers
- [ ] https://stackoverflow.com/questions/73557259/unable-to-connect-aws-sam-local-api-to-dynamodb-local-running-in-docker-instance

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

### API Implementation
- POST /books
- GET /books/<id>
- PUT /books/<id>
- DELETE /books/<id>

### DynamoDB Implementation
- [ ] Notes on simple table CRUD operations.

### API Documenation
- [ ] OpenAPI spec

## Testing
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
- [ ] Github Actions pipeline