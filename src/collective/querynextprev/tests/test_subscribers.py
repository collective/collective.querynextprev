# -*- coding: utf-8 -*-
"""Test subscribers."""

from collective.beaker.interfaces import ISession
from collective.querynextprev import QUERY
from collective.querynextprev import SEARCH_URL
from collective.querynextprev.interfaces import IAdditionalDataProvider
from collective.querynextprev.subscribers import convert_dates
from collective.querynextprev.subscribers import record_query_in_session
from collective.querynextprev.testing import COLLECTIVE_QUERYNEXTPREV_INTEGRATION_TESTING
from DateTime import DateTime
from plone import api
from zope.component import adapter
from zope.component import getGlobalSiteManager
from zope.interface import implementer
from zope.interface import Interface

import json
import unittest


class DummyEvent(object):
    pass


@implementer(IAdditionalDataProvider)
@adapter(Interface)
class ContextIdProvider(object):
    """Additional data: id of the faceted context."""

    def __init__(self, context):
        self.context = context

    def get_key(self):
        return "querynextprev.context_id"

    def get_value(self):
        return self.context.getId()


class TestSubscribers(unittest.TestCase):
    """Test subscribers."""

    layer = COLLECTIVE_QUERYNEXTPREV_INTEGRATION_TESTING

    def test_convert_dates(self):
        date = DateTime("2020/01/01 12:00:00 GMT+1")
        self.assertEqual(convert_dates(date), "DateTime:2020/01/01 12:00:00 GMT+1")
        self.assertRaises(TypeError, convert_dates, object())

    def test_record_query_in_session(self):
        """Test record_query_in_session subscriber."""
        portal = api.portal.get()
        request = portal.REQUEST
        session = ISession(request)
        self.assertEqual(session, {})
        event = DummyEvent()
        event.query = {"k": "foobar"}
        record_query_in_session(portal, event)
        self.assertIn(QUERY, ISession(request))
        self.assertIn(SEARCH_URL, ISession(request))

        # faceted query: paging keys removed, dates serialized; search url = referer
        request.environ["HTTP_REFERER"] = "http://nohost/plone/search"
        event.query = {
            "created": {"query": DateTime("2020/01/01 12:00:00 GMT+1"), "range": "min"},
            "portal_type": "Document",
            "facet.field": ["review_state"],
            "b_size": 20,
            "b_start": 0,
        }
        record_query_in_session(portal, event)
        self.assertEqual(
            json.loads(session[QUERY]),
            {
                "created": {"query": "DateTime:2020/01/01 12:00:00 GMT+1", "range": "min"},
                "portal_type": "Document",
            },
        )
        self.assertEqual(session[SEARCH_URL], "http://nohost/plone/search")
        self.assertNotIn("querynextprev.context_id", session)

        # IAdditionalDataProvider adapters of the faceted context store their data
        gsm = getGlobalSiteManager()
        gsm.registerAdapter(ContextIdProvider, name="context_id")
        self.addCleanup(gsm.unregisterAdapter, ContextIdProvider, name="context_id")
        record_query_in_session(portal, event)
        self.assertEqual(session["querynextprev.context_id"], portal.getId())
