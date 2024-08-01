import json
import boto3
from boto3.dynamodb.conditions import Key
from aws_lambda_powertools.event_handler import APIGatewayRestResolver

app = APIGatewayRestResolver()

dynamodb = boto3.resource('dynamodb', endpoint_url='http://dynamodb-local:8000')
table = dynamodb.Table('Books')

@app.get("/books")
def get_books():
    print("All books were requested")

    try:
        # table = dynamodb.Table('Books')

        response = table.get_item(
            Key={
                'title': 'The Pragmatic Programmer',
                'author': 'David Thomas'
            }
        )
        item = response['Item']
        print(item)
        return { "statusCode": 200, "body": json.dumps(item)}
    except Exception as e:
        print("Unexpected error: " + e)
        return { "statusCode": 500, "body": json.dumps({ "message": "Listing all books failed" })}


@app.get("/books/<title>")
def get_book(title):
    print(f"Book with title, {title}, was requested")

    try:
        # table = dynamodb.Table('Books')

        response = table.query(
            KeyConditionExpression=Key('title').eq(title),
        )

        items = response['Items']
        print(items)
        return { "statusCode": 200, "body": json.dumps(items)}
    except Exception as e:
        print(e)
        return { "statusCode": 500, "body": json.dumps({ "message": "Query for book failed" })}


@app.post("/books")
def create_book():
    print(f"Creating new book")

    book_data: dict = app.current_event.json_body  # deserialize json str to dict
    print(f"Creating new book with title, {book_data['title']}")

    try:
        # table = dynamodb.Table('Books')

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