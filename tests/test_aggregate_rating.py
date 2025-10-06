from __future__ import annotations

import json
from typing import Any

import pytest
from lxml.html import HtmlElement, fromstring

from tests.utils import TEST_DATA_ROOT
from zyte_parsers.aggregate_rating import (
    AggregateRating,
    _get_rating_numbers,
    extract_rating,
)


@pytest.mark.parametrize(
    ("node", "expected"),
    [
        (
            fromstring("<div>4.1</div>"),
            AggregateRating(ratingValue=4.1, bestRating=None),
        ),
        (
            fromstring("<div>4.1 of 5</div>"),
            AggregateRating(ratingValue=4.1, bestRating=5.0),
        ),
        (
            fromstring("<div><span>4.1</span><span>of 5</span></div>"),
            AggregateRating(ratingValue=4.1, bestRating=5.0),
        ),
        (
            fromstring("<div></div>"),
            AggregateRating(ratingValue=None, bestRating=None),
        ),
    ],
)
def test_extract_rating(node: HtmlElement, expected: AggregateRating) -> None:
    assert extract_rating(node) == expected


@pytest.mark.parametrize(
    "item",
    json.loads((TEST_DATA_ROOT / "rating_values.json").read_text(encoding="utf8")),
)
def test_extract_rating_fixture(item: dict[str, Any]) -> None:
    value = extract_rating(
        fromstring(item["parent_html"]).xpath("*[@xd-target-node]")[0]
    )
    assert value.ratingValue == item["ratingValue"]
    assert value.bestRating == item["bestRating"]


def test_extract_rating_tail() -> None:
    root = fromstring("<p><span>5</span> of 6</p>")
    span = root.xpath("//span")[0]
    expected = AggregateRating(ratingValue=5.0, bestRating=6.0)

    for node in [root, span]:
        assert extract_rating(node) == expected


RATING_VALUE_CASES = [
    ("4.5", [4.5]),
    ("4", [4]),
    ("4 out of 5", [4, 5]),
    ("4.5/5", [4.5, 5]),
    ("4.5 out of 5 based on 2 reviews", [4.5, 5, 2]),
    ("3.1/10", [3.1, 10]),
    ("0", [0]),
    ("0 out of 5", [0, 5]),
    ("3,2", [3.2]),
    ("1,3 out of 5,0", [1.3, 5.0]),
    ("0", [0]),
    ("Rating value 3", [3]),
    ("Rating 3.4 out of 5", [3.4, 5]),
    ("Average Rating 4,2", [4.2]),
    ("Rating 5,6 out of 10", [5.6, 10]),
]


@pytest.mark.parametrize(("value", "expected"), RATING_VALUE_CASES)
def test_get_rating_numbers(value: str, expected: list[float]) -> None:
    assert expected == _get_rating_numbers(value)
