"""QA Models"""

from typing import Dict, Optional

from pydantic import BaseModel  # pylint: disable=no-name-in-module

from kittens.models.qa import AnswersType, IdType, NotEmptyList, NotEmptyString
from kittens.models.qa.enums import QuestionType


class Answer(BaseModel):
    """Answer model"""

    answer_id: IdType
    answer: NotEmptyList | Dict[NotEmptyString, NotEmptyString]
    is_correct: Optional[bool]
    question_id: IdType
    author: IdType


class Question(BaseModel):
    """Question model"""

    question_id: IdType
    text: NotEmptyString
    question_type: QuestionType
    author: IdType


class QuestionGroup(BaseModel):
    """Question group model"""

    group_id: IdType
    answers: AnswersType
    extra_answers: Optional[AnswersType] = None
    question_id: IdType
    author: IdType
