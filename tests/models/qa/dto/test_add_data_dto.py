"""test parsing"""
import pytest
from pydantic import ValidationError

from kittens.models.qa.dto import AddDataDTO
from kittens.models.qa.enums import QuestionType


@pytest.fixture
def add_data_dto_dict():
    """Dict data for dto"""
    return {
        "question": "question",
        "answer": ["1"],
        "is_correct": True,
        "question_type": QuestionType.ONLY_ONE,
        "answers": ["1", "2"],
        "extra_answers": None,
    }


# pylint: disable=redefined-outer-name, missing-function-docstring


def test_normal(add_data_dto_dict: dict):
    AddDataDTO(**add_data_dto_dict)


def test_without_type(add_data_dto_dict: dict):
    add_data_dto_dict.pop("question_type")
    with pytest.raises(ValidationError):
        AddDataDTO(**add_data_dto_dict)


def test_not_match_question_with_extra(add_data_dto_dict: dict):
    assert add_data_dto_dict["question_type"] != QuestionType.MATCH
    add_data_dto_dict["extra_answers"] = ["3", "4"]
    with pytest.raises(ValidationError):
        AddDataDTO(**add_data_dto_dict)


def test_not_match_question_with_dict_answer(add_data_dto_dict: dict):
    assert add_data_dto_dict["question_type"] != QuestionType.MATCH
    add_data_dto_dict["answer"] = {"1": "2", "3": "4"}
    with pytest.raises(ValidationError):
        AddDataDTO(**add_data_dto_dict)


def test_match_question_with_answers_and_without_extra(add_data_dto_dict: dict):
    assert add_data_dto_dict["answers"]
    assert add_data_dto_dict["extra_answers"] is None
    add_data_dto_dict["question_type"] = QuestionType.MATCH
    with pytest.raises(ValidationError):
        AddDataDTO(**add_data_dto_dict)


def test_match_question_without_answers_and_extra_and_with_dict_answer(
    add_data_dto_dict: dict,
):
    add_data_dto_dict["answers"] = None
    add_data_dto_dict["extra_answers"] = None
    add_data_dto_dict["question_type"] = QuestionType.MATCH
    add_data_dto_dict["answer"] = {"1": "2", "3": "4"}
    with pytest.raises(ValidationError):
        AddDataDTO(**add_data_dto_dict)


def test_match_question_with_answers_and_extra_and_list_answer(add_data_dto_dict: dict):
    add_data_dto_dict["answers"] = ("1", "2", "3")
    add_data_dto_dict["question_type"] = QuestionType.MATCH
    add_data_dto_dict["extra_answers"] = ("4", "5", "6")
    add_data_dto_dict["answer"] = ["2", "3", "1", "7"]
    with pytest.raises(ValidationError):
        AddDataDTO(**add_data_dto_dict)


def test_match_question_with_answers_and_extra_and_dict_answer(add_data_dto_dict: dict):
    add_data_dto_dict["answers"] = ("1", "2", "3")
    add_data_dto_dict["question_type"] = QuestionType.MATCH
    add_data_dto_dict["extra_answers"] = ("4", "5", "6")
    add_data_dto_dict["answer"] = {"1": "4"}
    with pytest.raises(ValidationError):
        AddDataDTO(**add_data_dto_dict)
