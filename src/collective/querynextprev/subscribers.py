# -*- coding: utf-8 -*-
"""Subscribers."""
from collective.beaker.interfaces import ISession
from collective.querynextprev import QUERY
from collective.querynextprev import SEARCH_URL
from collective.querynextprev.interfaces import IAdditionalDataProvider
from collective.querynextprev.utils import clean_query
from DateTime import DateTime
from zope.component import getAdapters
from zope.globalrequest import getRequest

import json


def convert_dates(obj):
    """Convert dates to iso format for json serialization."""
    if isinstance(obj, DateTime):
        return "DateTime:{0}".format(str(obj))
    else:
        raise TypeError(repr(obj) + " is not JSON serializable")


def record_query_in_session(obj, event):
    """Record catalog query in session."""
    request = getRequest()
    session = ISession(request)
    session[QUERY] = json.dumps(clean_query(event.query), default=convert_dates)
    session[SEARCH_URL] = request.HTTP_REFERER
    adapters = getAdapters((obj,), IAdditionalDataProvider)
    for adapter in list(dict(adapters).values()):
        session[adapter.get_key()] = adapter.get_value()
    session.save()
