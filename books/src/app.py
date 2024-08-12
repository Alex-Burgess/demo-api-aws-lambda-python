import json
import boto3
from typing import Optional
from pydantic import BaseModel, Field
from boto3.dynamodb.types import TypeDeserializer

from aws_lambda_powertools import Logger
from aws_lambda_powertools.logging import correlation_paths
from aws_lambda_powertools.event_handler import APIGatewayRestResolver
from aws_lambda_powertools.event_handler import APIGatewayRestResolver, Response, content_types
from aws_lambda_powertools.event_handler.openapi.exceptions import RequestValidationError
from aws_lambda_powertools.event_handler.exceptions import (
    InternalServerError,
    NotFoundError
)

logger = Logger(service="Books API")

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
    logger.error("Request failed validation", path=app.current_event.path, errors=ex.errors())

    return Response(
        status_code=400,
        content_type=content_types.APPLICATION_JSON,
        body="Invalid data",
    )


@app.get("/books/<id>")
def get_book(id: str):
    logger.info(f"Request for book {id} received")

    try:
        response = table.get_item(
            Key={ 'id': id }
        )
    except Exception as e:
        logger.exception("Unexpected error getting item from table")
        raise InternalServerError("There was an unexpected error")

    if response.get('Item') is None:
        logger.info("No item was found")
        raise NotFoundError
    else:
        item = response['Item']
        logger.info(f"Item with {id} found")
        logger.debug(item)
        return item


@app.post("/books")
def create_book(book: Book):
    logger.info(f"Request to create book was received")

    try:
        book_data: dict = book.dict(by_alias=True)
        book_data['id'] = book_data['IBAN'];
        logger.info(f"Creating new book with id, {book_data['IBAN']}")

        table.put_item(
            Item=book_data
        )
        # TODO: Add condition expression

        return book_data['IBAN']
    except Exception as e:
        logger.exception("Unexpected error creating item in table")
        raise InternalServerError("There was an unexpected error")


@logger.inject_lambda_context(correlation_id_path=correlation_paths.API_GATEWAY_REST)
def lambda_handler(event, context):
    logger.debug(event)
    return app.resolve(event, context)
