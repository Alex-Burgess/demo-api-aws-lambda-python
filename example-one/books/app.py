import json
import boto3
from boto3.dynamodb.conditions import Key
from aws_lambda_powertools.event_handler import APIGatewayRestResolver

app = APIGatewayRestResolver()

dynamodb = boto3.resource('dynamodb', endpoint_url='http://dynamodb-local:8000')


@app.get("/books")
def get_books():
    print("All books were requested")

    try:
        table = dynamodb.Table('Bookstore')

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
        table = dynamodb.Table('Bookstore')

        response = table.query(
            KeyConditionExpression=Key('title').eq(title),
        )

        items = response['Items']
        print(items)
        return { "statusCode": 200, "body": json.dumps(items)}
    except Exception as e:
        print(e)
        return { "statusCode": 500, "body": json.dumps({ "message": "Query for book failed" })}

# def create_book():
    # table = dynamodb.Table('Bookstore')
    # table.put_item(
    #     Item={
    #         'title': 'New book',
    #         'author': 'New author',
    #         'category': 'Computing',
    #     }
    # )
    # print('Created item')


def lambda_handler(event, context):
    # return get_book("The Pragmatic Programmer")
    return app.resolve(event, context)