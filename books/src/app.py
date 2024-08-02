import json
import boto3
from typing import Optional
from pydantic import BaseModel, Field
from boto3.dynamodb.types import TypeDeserializer

from aws_lambda_powertools.event_handler import APIGatewayRestResolver, Response, content_types
from aws_lambda_powertools.event_handler.openapi.exceptions import RequestValidationError
from aws_lambda_powertools.event_handler.exceptions import (
    InternalServerError,
    NotFoundError
)

app = APIGatewayRestResolver(enable_validation=True)
dynamodb = boto3.resource('dynamodb', endpoint_url='http://dynamodb-local:8000')
table = dynamodb.Table('Books')


class Book(BaseModel):
    id_: Optional[int] = Field(alias="id", default=None)
    IBAN: str
    title: str
    authors: list[str]
    category: str
    pages: int


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
    try:
        print(f"Request for book {id} was received")

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

        return item


@app.post("/books")
def create_book(book: Book):
    print(f"Request to create book was received")

    try:
        book_data: dict = book.dict(by_alias=True)
        book_data['id'] = book_data['IBAN'];
        print(f"Creating new book with id, {book_data['IBAN']}")

        table.put_item(
            Item=book_data
        )

        return book_data['IBAN']
    except Exception as e:
        print(e)
        raise InternalServerError("There was an unexpected error")


def lambda_handler(event, context):
    return app.resolve(event, context)
