from __future__ import annotations

from typing import TYPE_CHECKING

from price_parser import Price

from zyte_parsers.utils import extract_text

if TYPE_CHECKING:
    from zyte_parsers import SelectorOrElement


def extract_price(
    node: SelectorOrElement | str,
    *,
    currency_hint: SelectorOrElement | str | None = None,
) -> Price:
    """Extract a price value from a node or a string that contains it.

    :param node: A node or a string that includes the price text.
    :param currency_hint: A string or a node that can contain currency. It will
        be passed as a hint to ``price-parser``. If currency is present in the
        price string, it could be preferred over the value extracted from
        ``currency_hint``.
    :return: The price value as a ``price_parser.Price`` object.
    """
    text = node if isinstance(node, str) else extract_text(node)
    if currency_hint is not None and not isinstance(currency_hint, str):
        currency_hint = extract_text(currency_hint)
    return Price.fromstring(text, currency_hint=currency_hint)
