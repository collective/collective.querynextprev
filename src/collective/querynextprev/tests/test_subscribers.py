# -*- coding: utf-8 -*-
"""Test subscribers."""

from collective.beaker.interfaces import ISession
from collective.querynextprev import QUERY
from collective.querynextprev import SEARCH_URL
from collective.querynextprev.subscribers import record_query_in_session
from collective.querynextprev.testing import COLLECTIVE_QUERYNEXTPREV_INTEGRATION_TESTING
from plone import api

import unittest


class DummyEvent(object):
    pass


class TestSubscribers(unittest.TestCase):
    """Test subscribers."""

    layer = COLLECTIVE_QUERYNEXTPREV_INTEGRATION_TESTING

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
