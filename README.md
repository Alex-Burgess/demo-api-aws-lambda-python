# Demo API with AWS Lambda and Python
This application demonstrates a simple CRUD API which manages a table of books using a serverless architecture model on AWS. This demonstrates the following concepts:

- [Essential Tools](#essential-tools)
- [Initialising a New Project](#initialising-a-new-project)
- [Dev Environment](#dev-environment)
- [DynamoDB CRUD Operations](#dynamodb-crud-operations)
- [Best Practices with PowerTools](#best-practices-with-powertools)
- [Testing](#testing)
- [Deployment](#deployment)

TODO:
- [ ] Create API documentation
- [ ] Add unit tests around functions, including error scenarios.
- [ ] Create integration test for happy path
- [ ] Modify POST method to include Condition expression to prevent item being overwritten.
- [ ] Add PUT API Method
- [ ] Add DELETE API Method


## Essential Tools
The following tools are used to build and deploy the application:
- [Python](https://www.python.org/downloads/) & [Pyenv](https://github.com/pyenv/pyenv)
- [Docker](https://hub.docker.com/search/?type=edition&offering=community)
- [SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html) ([installation](https://formulae.brew.sh/formula/aws-sam-cli))
- [NoSQL Workbench](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/workbench.html) ([installation](https://formulae.brew.sh/cask/nosql-workbench))


## Initialising a New Project
[AWS Serverless Application Model (SAM)](https://aws.amazon.com/serverless/sam/) is used to simplify the configuration and development of serverless applications.  The [Hello World Tutorial](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-getting-started-hello-world.html) is a useful guide for initialising a new project.  This command was used to initialise this project:
```
sam init --no-interactive \
 --name books \
 --runtime python3.12 \
 --app-template hello-world \
 --package-type Zip \
 --dependency-manager pip
```

To run this project locally:
1. Start python environment
    ```
    pyenv install 3.12.1
    pyenv virtualenv 3.12.1 lambda-demo-app
    pyenv activate lambda-demo-app
    ```
1. Install all the project dependencies:
    ```
    pip install -r books/requirements.txt
    ```
1. Start a local DynamoDB instance:
    ```
    docker compose up --detach
    ```
1. Create a table:
    1. Open NoSQL Workbench, select `Data modeler`, then `import data model`, and select [Books.json](/Books.json).
    1. Select `Visualizer`, then `Commit to Amazon DynamoDB` using a Local Connection.
1. Add some test data:
    1. Select `Operation builder`, then open `Local Connection`
    1. Select the `Books` table, then `PartiQL editor` and enter the following statement:
    ```
    INSERT INTO "Books" value 
    {
        'id' : '978-1732102217',
        'title' : 'A Philosophy of Software Design, 2nd Edition',
        'authors': ['John Ousterhout'],
        'IBAN': '978-1732102217',
        'category': 'Programming',
        'pages': 196
    }
    ```
1. Build:
    ```
    cd books
    sam build
    ```
1. Run - note the `--docker-network` option with the same network name in the [compose.yaml](/compose.yaml) file, which ensures the two containers can reach other:
    ```
    sam local start-api --docker-network dynamodb-local-network
    ```
1. Test (in 2nd terminal):
    ```
    curl http://127.0.0.1:3000/books/978-1732102217
    ```

When making code changes (i.e. not to the template), there is no need to stop/start the local API, you can just rebuild the changes in a 2nd terminal window and run the tests.
```
sam build
curl http://127.0.0.1:3000/books/978-1732102217
```

## Dev Environment
At the beginning of starting this project we created a python virtual environment to ensure our project has an isolated environment with the dependencies it requires.  So that Visual Studio can resolve all the dependencies we need to switch the Interpreter it is using. Use **Command + shift + P** shortcut, type "Python: Select Interpreter" and select the virtual environment.

The [requirements.txt](/books/requirements.txt) installs some useful dependencies:
- `cfn-lint`: to check template files for potential issues (Note: comment out the Runtime property of the [template.yaml](/books/template.yaml) file to check it is working). See [CloudFormation Linter](https://marketplace.visualstudio.com/items?itemName=kddejong.vscode-cfn-lint).
- `boto3`: so that Visual Studio can resolve its dependencies when developing the code.
- `boto3-stubs[essential]`: to provide type annotations for the boto3 API. See [boto3-stubs](https://pypi.org/project/boto3-stubs/).


## DynamoDB CRUD Operations
The [AWS SDK for Python (boto3)](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html) is used to implement CRUD operations against DynamoDB. There are two interfaces available to work with *client* and *resource*.  For this project the *resource* interface, which is the higher-level and hence simpler interface, was used.  See [Understanding the client and resource abstraction layers](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/programming-with-python.html#programming-with-python-client-resource) for further information. 

Below are useful reference guides:
- [Boto3 - Table Resource docs](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb/table/index.html)
- [Amazon DynamoDB examples](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/dynamodb.html)

## Best Practices with PowerTools
[Powertools for AWS Lambda (Python)](https://docs.powertools.aws.dev/lambda/python/latest/) is a developer toolkit to implement best practices, with many features that can be adopted independently.  Using the toolkit provides a similar experience to using a framework, reducing boiler plate and increasing developer velocity.  The [tutorial](https://docs.powertools.aws.dev/lambda/python/2.2.0/tutorial) is a good place to start to get a feel for the problems it solves.


### API Event Handling (aka Routing)
This application has the following routes:
- POST /books
- GET /books/<id>
- PUT /books/<id>
- DELETE /books/<id>

It would be cumbersome to have one lambda function for each API path.  The [REST API Event Handler](https://docs.powertools.aws.dev/lambda/python/latest/core/event_handler/api_gateway/) provides a lightweight routing approach to handling requests for multiple URL paths/methods with one function.  The [app.py](/books/src/app.py) demonstrates this concept with one `lambda_handler` and specific function definitions for each route. 

The `return app.resolve(event, context)` line of the `lambda_handler` creates the [json response automatically](https://docs.powertools.aws.dev/lambda/python/latest/core/event_handler/api_gateway/#response-auto-serialization).

The Event Handler also provides a way to easily [raise HTTP errors](https://docs.powertools.aws.dev/lambda/python/latest/core/event_handler/api_gateway/#raising-http-errors). The [app.py](/books/src/app.py) lambda function demonstrates how to return error codes using the provided exceptions.  **Note:** a 404 is returned for any unmatched route by default.

The Event Handler can be used to validate requests.  The (/books/src/app.py) lambda function demonstrates how to validate path parameters, as well as incoming json payloads by using the Book class.  **Note** pydantic must be included in the [src/requirements.txt](/books/src/requirements.txt) file.

### Logging
The [app.py](/books/src/app.py) demonstrates how to implement PowerTools standardised approach to logging objects.  This shows the following:
- How to setup the logger
- How to log different levels
- Configure the log level using an environment variable
- How to log the context and include a Correlation ID.

The [Logger](https://docs.powertools.aws.dev/lambda/python/latest/core/logger/) documentation provides further implementation details.

### API Documenation


- [ ] See https://docs.powertools.aws.dev/lambda/python/latest/core/event_handler/api_gateway/#enabling-swaggerui
- [ ] OpenAPI spec
- [ ] Errors


## Testing
- [ ] Unit testing
- [ ] Integration testing 

Postman collection: 

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
- [ ] Github Actions CI/CD pipeline