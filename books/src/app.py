import boto3
import json

from aws_lambda_powertools.event_handler import APIGatewayRestResolver
from aws_lambda_powertools.utilities.typing import LambdaContext
from aws_lambda_powertools.logging import correlation_paths
from aws_lambda_powertools import Logger
from aws_lambda_powertools import Tracer
from aws_lambda_powertools import Metrics
from aws_lambda_powertools.metrics import MetricUnit

# dynamodb = boto3.resource('dynamodb', endpoint_url='http://dynamodb-local:8000')

app = APIGatewayRestResolver()
tracer = Tracer()
logger = Logger()
metrics = Metrics(namespace="Powertools")

@app.get("/books")
@tracer.capture_method
def books():
    logger.info("Request for all books received")

    try:
        dynamodb = boto3.resource('dynamodb', endpoint_url='http://dynamodb-local:8000')
        table = dynamodb.Table('Bookstore')

        table.put_item(
            Item={
                'title': 'New book2',
                'author': 'New author',
                'category': 'Computing',
            }
        )
        print('Created item')

    #     response = table.get_item(
    #         Key={
    #             'title': 'The Pragmatic Programmer',
    #             'author': 'David Thomas'
    #         }
    #     )
    #     item = response['Item']
    #     print(item)
    except Exception as e:
        # Send some context about this error to Lambda Logs
        print(e)

        return {
            "statusCode": 500,
            "body": json.dumps({
                "errorMessage": "Function failed to connect to table"
            })
        }

    metrics.add_metric(name="SuccessfulGetBooksRequest", unit=MetricUnit.Count, value=1)
    return {"message": "hello unknown!"}
    # return {
    #     "statusCode": 200,
    #     "body": json.dumps({
    #         "message": "hello world"
    #     })
    # }


@logger.inject_lambda_context(correlation_id_path=correlation_paths.API_GATEWAY_REST)
@tracer.capture_lambda_handler
@metrics.log_metrics(capture_cold_start_metric=True)
def lambda_handler(event: dict, context: LambdaContext) -> dict:
    return app.resolve(event, context)
