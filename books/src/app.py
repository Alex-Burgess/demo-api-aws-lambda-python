import json
import boto3
from boto3.dynamodb.types import TypeDeserializer

from pydantic import BaseModel, Field

from aws_lambda_powertools.event_handler import APIGatewayRestResolver, Response, content_types
from aws_lambda_powertools.event_handler.openapi.exceptions import RequestValidationError
from aws_lambda_powertools.event_handler.exceptions import (
    InternalServerError,
    NotFoundError
)

app = APIGatewayRestResolver(enable_validation=True)

dynamodb = boto3.resource('dynamodb', endpoint_url='http://dynamodb-local:8000')
table = dynamodb.Table('Books')

@app.exception_handler(RequestValidationError)  
def handle_validation_error(ex: RequestValidationError):
    # logger.error("Request failed validation", path=app.current_event.path, errors=ex.errors())

    return Response(
        status_code=400,
        content_type=content_types.APPLICATION_JSON,
        body="Invalid data",
    )


@app.get("/books/<id>")
def get_book(id: str):
    print(f"Book with id, {id}, was requested")

    try:
        response = table.get_item(
            Key={ 'id': id }
        )
    except Exception as e:
        print(e)
        raise InternalServerError("There was an unexpected error")

    if response.get('Item') is None:
        print('No item was found')
        raise NotFoundError
    else:
        item = response['Item']
        print(item)

        return { "book": item }

@app.post("/books")
def create_book():
    print(f"Creating new book")

    book_data: dict = app.current_event.json_body  # deserialize json str to dict
    print(f"Creating new book with title, {book_data['title']}")

    try:
        table.put_item(
            Item={
                'title': book_data['title'],
                'author': book_data['author'],
                'category': book_data['category'],
            }
        )
        return { "statusCode": 200 }
    except Exception as e:
        print(e)
        return { "statusCode": 500, "body": json.dumps({ "message": "Creating book failed" })}


def lambda_handler(event, context):
    return app.resolve(event, context)
