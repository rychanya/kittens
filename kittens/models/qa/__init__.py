# pylint: disable=missing-module-docstring

from pydantic import confrozenset, conlist, constr  # pylint: disable=no-name-in-module

NotEmptyString = constr(min_length=1)
NotEmptyList = conlist(item_type=NotEmptyString, min_items=1, unique_items=True)
AnswersType = confrozenset(item_type=NotEmptyString, min_items=2)
ExtraAnswersType = list[NotEmptyString]
