import json
import boto3
from boto3.dynamodb.types import TypeDeserializer
from aws_lambda_powertools.event_handler import APIGatewayRestResolver
from aws_lambda_powertools.event_handler.exceptions import (
    InternalServerError
)

app = APIGatewayRestResolver()

dynamodb = boto3.resource('dynamodb', endpoint_url='http://dynamodb-local:8000')
table = dynamodb.Table('Books')


@app.get("/books/<id>")
def get_book(id):
    print(f"Book with id, {id}, was requested")

    # TODO : Validate ID is a number.  If it is not a number return a 400 with "The request is invalid"

    try:
        response = table.get_item(
            Key={ 'id': id }
        )

        item = response['Item']

        # TODO : If no item is returned, return a 404 with message "no book found with book id: {id}""

        print(item)

        return { "book": item }
    except Exception as e:
        print(e)
        raise InternalServerError("There was an unexpected error")


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
