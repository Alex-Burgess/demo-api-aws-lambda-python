import json

# import requests
import boto3

dynamodb = boto3.resource('dynamodb', endpoint_url='http://dynamodb-local:8000')

def lambda_handler(event, context):
    print("CONNECTING TO TABLE")

    try:
        table = dynamodb.Table('Bookstore')

        # table.put_item(
        #     Item={
        #         'title': 'New book',
        #         'author': 'New author',
        #         'category': 'Computing',
        #     }
        # )
        # print('Created item')

        response = table.get_item(
            Key={
                'title': 'The Pragmatic Programmer',
                'author': 'David Thomas'
            }
        )
        item = response['Item']
        print(item)
    except Exception as e:
        # Send some context about this error to Lambda Logs
        print(e)

        return {
            "statusCode": 500,
            "body": json.dumps({
                "errorMessage": "Function failed to connect to table"
            })
        }

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "hello world",
            # "location": ip.text.replace("\n", "")
        }),
    }
