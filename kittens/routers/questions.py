"""Questions router"""
from fastapi import APIRouter, Depends, Response, status
from fastapi.exceptions import HTTPException
from pydantic import UUID4  # pylint: disable=no-name-in-module

from kittens import dependencies
from kittens.models.qa.models import (
    AddDataDTO,
    AddDataDTOResult,
    Answer,
    AnswerDB,
    Question,
    QuestionDB,
)
from kittens.store import Store

router = APIRouter()


@router.post(
    "/import",
    response_model=AddDataDTOResult,
    responses={status.HTTP_201_CREATED: {"model": AddDataDTOResult}},
)
async def import_qa(
    data: AddDataDTO,
    responce: Response,
    store: Store = Depends(dependencies.store),
    author_id: UUID4 = Depends(dependencies.user_id),
):
    """Import answer"""
    async with await store.db_client.start_session() as session:
        async with session.start_transaction():
            model, is_new = await store.import_answer(
                data=data, author_id=author_id, session=session
            )
            if is_new:
                responce.status_code = status.HTTP_201_CREATED
            return model


@router.post(
    "/",
    response_model=QuestionDB,
    responses={status.HTTP_201_CREATED: {"model": QuestionDB}},
)
async def get_or_create(
    question: Question,
    responce: Response,
    store: Store = Depends(dependencies.store),
    author_id: UUID4 = Depends(dependencies.user_id),
):
    """get or create question"""
    async with await store.db_client.start_session() as session:
        async with session.start_transaction():
            model, is_new = await store.get_or_create_questions(
                question=question, author_id=author_id, session=session
            )
    if is_new:
        responce.status_code = status.HTTP_201_CREATED
    return model


@router.get("/{question_id}", response_model=QuestionDB)
async def get_by_id(question_id: UUID4, store: Store = Depends(dependencies.store)):
    """get question by ID"""
    async with await store.db_client.start_session() as session:
        async with session.start_transaction():
            question = await store.get_question_by_id(question_id, session=session)
    if question is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return question


@router.post(
    "/{question_id}",
    response_model=AnswerDB,
    responses={status.HTTP_201_CREATED: {"model": AnswerDB}},
)
async def add_answer(
    question_id: UUID4,
    answer: Answer,
    responce: Response,
    store: Store = Depends(dependencies.store),
    author_id: UUID4 = Depends(dependencies.user_id),
):
    """Add answer to question"""
    async with await store.db_client.start_session() as session:
        async with session.start_transaction():
            question = await store.get_question_by_id(question_id, session=session)
            if question is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
            model, is_new = await store.get_or_create_answer(
                answer, question_id, author_id=author_id, session=session
            )
            if is_new:
                responce.status_code = status.HTTP_201_CREATED
            return model
