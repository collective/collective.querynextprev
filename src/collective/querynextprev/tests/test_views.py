# -*- coding: utf-8 -*-
"""Test views."""
from collective.beaker.interfaces import ISession
from collective.querynextprev import NEXT_UIDS
from collective.querynextprev import PREVIOUS_UIDS
from collective.querynextprev import QUERY
from collective.querynextprev import SEARCH_URL
from collective.querynextprev.browser.views import GoToNextItem
from collective.querynextprev.browser.views import GoToPreviousItem
from collective.querynextprev.testing import COLLECTIVE_QUERYNEXTPREV_INTEGRATION_TESTING
from collective.querynextprev.tests import query_utf8
from plone import api
from plone.app.testing import login
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME

import json
import unittest


class TestGoToNextItem(unittest.TestCase):
    """Test GoToNextItem view."""

    layer = COLLECTIVE_QUERYNEXTPREV_INTEGRATION_TESTING

    def setUp(self):
        portal = api.portal.get()
        setRoles(portal, TEST_USER_ID, ["Manager"])
        login(portal, TEST_USER_NAME)
        for x in range(30):
            name = "mydoc-{:02d}".format(x + 1)
            api.content.create(id=name, type="Document", container=portal, title="é")

        self.doc1 = portal["mydoc-01"]
        self.doc2 = portal["mydoc-02"]
        self.doc3 = portal["mydoc-03"]
        self.doc11 = portal["mydoc-11"]
        self.doc30 = portal["mydoc-30"]
        self.portal = portal

    def test_get_uids(self):
        """Test get_uids method."""
        request = self.portal.REQUEST
        session = ISession(request)
        session[QUERY] = query_utf8
        session.save()
        context = self.portal
        view = GoToNextItem(context, request)
        uids = view.get_uids()
        self.assertEqual(len(uids), 30)
        self.assertEqual(uids[0], self.doc1.UID())
        self.assertEqual(uids[10], self.doc11.UID())
        self.assertEqual(uids[29], self.doc30.UID())

    def test_view(self):
        doc1 = self.doc1
        doc2 = self.doc2
        doc3 = self.doc3
        portal = self.portal
        request = portal.REQUEST

        # no query, no search url
        session = ISession(request)
        session.save()
        view = GoToNextItem(doc1, request)
        view()
        self.assertEqual(request.response.getHeader("location"), portal.absolute_url())

        # no search url
        session[SEARCH_URL] = "http://www.example.com"
        session.save()
        view = GoToNextItem(doc1, request)
        view()
        self.assertEqual(
            request.response.getHeader("location"), "http://www.example.com"
        )

        # with a query
        session[QUERY] = query_utf8
        session[PREVIOUS_UIDS] = json.dumps([])
        session[NEXT_UIDS] = json.dumps([doc2.UID(), doc3.UID()])
        session[SEARCH_URL] = "http://www.example.com"
        session.save()
        view = GoToNextItem(doc1, request)
        view()
        self.assertEqual(request.response.getHeader("location"), doc2.absolute_url())

        # with a query, first next item deleted
        session[QUERY] = query_utf8
        session[PREVIOUS_UIDS] = json.dumps([])
        session[NEXT_UIDS] = json.dumps([doc2.UID(), doc3.UID()])
        session[SEARCH_URL] = "http://www.example.com"
        session.save()
        view = GoToNextItem(doc1, request)
        api.content.delete(doc2)
        view()
        self.assertEqual(request.response.getHeader("location"), doc3.absolute_url())


class TestGoToPreviousItem(unittest.TestCase):
    """Test GoToPreviousItem view."""

    layer = COLLECTIVE_QUERYNEXTPREV_INTEGRATION_TESTING

    def setUp(self):
        portal = api.portal.get()
        setRoles(portal, TEST_USER_ID, ["Manager"])
        login(portal, TEST_USER_NAME)
        for x in range(30):
            name = "mydoc-{:02d}".format(x + 1)
            api.content.create(id=name, type="Document", container=portal, title="é")

        self.doc1 = portal["mydoc-01"]
        self.doc2 = portal["mydoc-02"]
        self.doc3 = portal["mydoc-03"]
        self.doc20 = portal["mydoc-20"]
        self.doc30 = portal["mydoc-30"]
        self.portal = portal

    def test_get_uids(self):
        """Test get_uids method."""
        request = self.portal.REQUEST
        session = ISession(request)
        session[QUERY] = query_utf8
        session.save()
        context = self.portal
        view = GoToPreviousItem(context, request)
        uids = view.get_uids()
        self.assertEqual(len(uids), 30)
        self.assertEqual(uids[0], self.doc30.UID())
        self.assertEqual(uids[10], self.doc20.UID())
        self.assertEqual(uids[29], self.doc1.UID())

    def test_view(self):
        doc1 = self.doc1
        doc2 = self.doc2
        doc3 = self.doc3
        portal = self.portal
        request = portal.REQUEST

        # with a query
        session = ISession(request)
        session[QUERY] = query_utf8
        session[PREVIOUS_UIDS] = json.dumps([doc2.UID(), doc1.UID()])
        session[NEXT_UIDS] = json.dumps([])
        session[SEARCH_URL] = "http://www.example.com"
        session.save()
        view = GoToPreviousItem(doc3, request)
        view()
        self.assertEqual(request.response.getHeader("location"), doc2.absolute_url())

        # with a query, first next item deleted
        session[QUERY] = query_utf8
        session[PREVIOUS_UIDS] = json.dumps([doc1.UID()])
        session[NEXT_UIDS] = json.dumps([])
        session[SEARCH_URL] = "http://www.example.com"
        session.save()
        api.content.delete(doc1)
        view = GoToPreviousItem(doc2, request)
        view()
        self.assertEqual(
            request.response.getHeader("location"), "http://www.example.com"
        )
