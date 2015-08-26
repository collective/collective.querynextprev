# -*- coding: utf-8 -*-
"""Subscribers."""
import json

from zope.component import getAdapters
from zope.globalrequest import getRequest

from collective.querynextprev import QUERY, SEARCH_URL
from collective.querynextprev.interfaces import IAdditionalDataProvider


def record_query_in_session(obj, event):
    """Record catalog query in session."""
    request = getRequest()
    session = request.SESSION
    session[QUERY] = json.dumps(event.query)
    session[SEARCH_URL] = request.HTTP_REFERER
    adapters = getAdapters((obj, ), IAdditionalDataProvider)
    for adapter in dict(adapters).values():
        session[adapter.get_key()] = adapter.get_value()
