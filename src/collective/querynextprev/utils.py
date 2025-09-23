# -*- coding: utf-8 -*-
"""Utils."""

from collections.abc import Iterable
from collections.abc import Mapping
from DateTime import DateTime

import re


WINDOW_SIZE = 10


def expire_session_data(session):
    """Expire all querynextprev data in session."""
    for key in list(session.keys()):
        if key.startswith("querynextprev"):
            del session[key]
    session.save()


def first_common_item(l1, l2):
    """Get first item in l2 that is also in l1."""
    for item in l2:
        if item in l1:
            return item

    return None


def get_next_items(lst, index, include_index=False):
    """Get WINDOW_SIZE next items."""
    last_index = min(index + WINDOW_SIZE, len(lst))
    if include_index:
        index -= 1

    return lst[index + 1 : last_index + 1]  # noqa E203


def get_previous_items(lst, index, include_index=False):
    """Get WINDOW_SIZE previous items."""
    first_index = max(index - 10, 0)
    if include_index:
        index += 1

    return lst[first_index:index]


def convert_to_str(value):
    """Converts a value to str."""
    # pylint: disable=W0141
    if isinstance(value, str):
        return value
    elif isinstance(value, Mapping):
        return dict(list(map(convert_to_str, iter(list(value.items())))))
    elif isinstance(value, Iterable):
        return type(value)(list(map(convert_to_str, value)))
    else:
        return value


def clean_query(query):
    """Remove from eeafacetednavigation query useless keys"""
    return {
        k: v
        for k, v in list(query.items())
        if k not in ("facet.field", "b_size", "b_start")
    }


def json_object_hook(value):
    if isinstance(value, dict):
        return {k: json_object_hook(v) for k, v in list(value.items())}
    if isinstance(value, list):
        return list(map(json_object_hook, value))
    regexp = re.compile(r"^DateTime:\d{4}\/\d{2}\/\d{2} \d{2}:\d{2}:\d{2}")
    if isinstance(value, str) and re.match(regexp, value):
        return DateTime(value[9:])
    return value
