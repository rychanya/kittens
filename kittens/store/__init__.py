"""Store"""
from typing import Optional, Tuple
from uuid import uuid4

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection
from pydantic import UUID4  # pylint: disable=no-name-in-module

from kittens.models.qa.models import Answer, AnswerDB, Question, QuestionDB
from kittens.store.settings import StoreSettings


class Store:
    """Store"""

    def __init__(self, db_client: AsyncIOMotorClient, settings: StoreSettings) -> None:
        self.settings = settings
        self.db_client = db_client

    def _get_collection(self, collection_name: str) -> AsyncIOMotorCollection:
        return self.db_client.get_database(self.settings.db_name).get_collection(
            collection_name
        )

    @property
    def answers(self):
        """answers collection"""
        return self._get_collection("answers")

    @property
    def questions(self):
        """questins collection"""
        return self._get_collection("questions")

    async def get_question_by_id(
        self, question_id: UUID4, session=None
    ) -> Optional[QuestionDB]:
        """Get question by ID"""
        doc = await self.questions.find_one(
            {"question_id": question_id}, session=session
        )
        if doc:
            return QuestionDB.parse_obj(doc)

    async def get_or_create_questions(
        self, question: Question, author_id: UUID4, session=None
    ) -> Tuple[QuestionDB, bool]:
        """Get or create question in DB"""
        doc = await self.questions.find_one(
            {
                "text": question.text,
                "question_type": question.question_type,
                "$expr": {
                    "$and": [
                        {"$setEquals": ["$answers", list(question.answers)]}
                        if question.answers
                        else {"$eq": ["$answers", None]},
                        {"$setEquals": ["$extra_answers", list(question.extra_answers)]}
                        if question.extra_answers
                        else {"$eq": ["$extra_answers", None]},
                    ]
                },
            },
            session=session,
        )
        if doc:
            return (QuestionDB.parse_obj(doc), False)
        inserted_id = uuid4()
        await self.questions.insert_one(
            {
                "text": question.text,
                "question_type": question.question_type,
                "question_id": inserted_id,
                "author": author_id,
                "answers": list(question.answers)
                if question.answers is not None
                else None,
                "extra_answers": list(question.extra_answers)
                if question.extra_answers is not None
                else None,
            },
            session=session,
        )
        return (
            QuestionDB(
                author=author_id,
                question_id=inserted_id,
                text=question.text,
                question_type=question.question_type,
                answers=question.answers,
                extra_answers=question.extra_answers,
            ),
            True,
        )

    async def get_or_create_answer(
        self, answer: Answer, question_id: UUID4, author_id: UUID4, session=None
    ) -> Tuple[AnswerDB, bool]:
        """get or create answer"""
        doc = await self.answers.find_one(
            {
                "is_correct": answer.is_correct,
                "question_id": question_id,
                "answer": answer.answer,
                "extra_answer": answer.extra_answer,
            },
            session=session,
        )
        if doc:
            return (AnswerDB.parse_obj(doc), False)
        inserted_id = uuid4()
        await self.answers.insert_one(
            {
                "answer": answer.answer,
                "extra_answer": answer.extra_answer,
                "is_correct": answer.is_correct,
                "question_id": question_id,
                "answer_id": inserted_id,
                "author": author_id,
            },
            session=session,
        )
        return (
            AnswerDB(
                answer=answer.answer,
                is_correct=answer.is_correct,
                question_id=question_id,
                author=author_id,
                answer_id=inserted_id,
            ),
            True,
        )
