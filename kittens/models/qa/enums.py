"""QA Enums"""
from enum import Enum


class QuestionType(str, Enum):
    """Questions types"""

    ONLY_ONE = "ONLY_ONE"
    MANY = "MANY"
    ORDERED = "ORDERED"
    MATCH = "MATCH"
