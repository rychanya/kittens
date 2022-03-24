"""QA DTO"""
from typing import Dict, Optional

from pydantic import BaseModel, root_validator  # pylint: disable=no-name-in-module

from kittens.models.qa import AnswersType, NotEmptyList, NotEmptyString
from kittens.models.qa.enums import QuestionType


class AddDataDTO(BaseModel):
    """Add qa dto model"""

    question: NotEmptyString
    answer: NotEmptyList | Dict[NotEmptyString, NotEmptyString]
    is_correct: Optional[bool]
    question_type: QuestionType
    answers: Optional[AnswersType] = None
    extra_answers: Optional[AnswersType] = None

    @root_validator
    def consistency(cls, values: dict):  # pylint: disable=no-self-argument
        """consistency validation"""
        question_type: Optional[QuestionType] = values.get("question_type")
        answers: Optional[AnswersType] = values.get("answers")
        extra_answers: Optional[AnswersType] = values.get("extra_answers")
        answer: Optional[list | dict] = values.get("answer")
        if question_type is None:
            return values
        if question_type == QuestionType.MATCH:
            if answers is None and extra_answers is None:
                if not isinstance(answer, list):
                    raise ValueError(
                        "Answer must be list in match question without group"
                    )
            elif answer is None or extra_answers is None:
                raise ValueError(
                    "Answers or extra answers must be none or not none together"
                )
            else:
                if isinstance(answer, list) and answers != set(answer):
                    raise ValueError("All answers must be in answer")
                if isinstance(answer, dict) and (
                    answers != set(answer.keys())
                    or extra_answers != set(answer.values())
                ):
                    raise ValueError("Incorrect answer")

        else:
            if extra_answers:
                raise ValueError("Extra answers can be only in match question")
            if not isinstance(answer, list):
                raise ValueError("Answer of not match type question must be list")

        return values
