"""QA DTO"""


from pydantic import BaseModel  # pylint: disable=no-name-in-module

from kittens.models.qa.models import Answer, Question


class AddDataDTO(BaseModel):
    """Add qa dto model"""

    question: Question
    answer: Answer
