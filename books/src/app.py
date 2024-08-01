import json
import boto3
from boto3.dynamodb.types import TypeDeserializer
from aws_lambda_powertools.event_handler import APIGatewayRestResolver

app = APIGatewayRestResolver()

dynamodb = boto3.resource('dynamodb', endpoint_url='http://dynamodb-local:8000')
table = dynamodb.Table('Books')


@app.get("/books/<id>")
def get_book(id):
    print(f"Book with id, {id}, was requested")

    try:
        response = table.get_item(
            Key={ 'id': id }
        )

        item = response['Item']
        print(item)

        return { "statusCode": 200, "body": json.dumps(item, default=str)}
    except Exception as e:
        print(e)
        return { "statusCode": 500, "body": json.dumps({ "message": "Query for book failed" })}


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


# def dynamo_to_python(dynamo_object: dict) -> dict:
#     deserializer = TypeDeserializer()
#     return {
#         k: deserializer.deserialize(v) 
#         for k, v in dynamo_object.items()
#     }