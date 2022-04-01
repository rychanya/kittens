"""QA Models"""

from typing import Optional

from pydantic import UUID4, BaseModel  # pylint: disable=no-name-in-module

from kittens.models.qa import (
    AnswersType,
    ExtraAnswersType,
    NotEmptyList,
    NotEmptyString,
)
from kittens.models.qa.enums import QuestionType


class Answer(BaseModel):
    """Answer model"""

    answer: NotEmptyList
    extra_answer: ExtraAnswersType = []
    is_correct: Optional[bool]


class AnswerDB(Answer):
    """Answer DB model"""

    question_id: UUID4
    answer_id: UUID4
    author: UUID4


class Question(BaseModel):
    """Question model"""

    text: NotEmptyString
    question_type: QuestionType
    answers: Optional[AnswersType] = None
    extra_answers: Optional[AnswersType] = None


class QuestionDB(Question):
    """Question DB model"""

    question_id: UUID4
    author: UUID4


class AddDataDTO(BaseModel):
    """Add qa dto model"""

    question: Question
    answer: Answer


class AddDataDTOResult(BaseModel):
    """Add data result dto model"""

    question: QuestionDB
    answer: AnswerDB
