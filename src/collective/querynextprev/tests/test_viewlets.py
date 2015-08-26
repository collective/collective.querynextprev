# -*- coding: utf-8 -*-
import json
import unittest2 as unittest

from plone import api
from plone.app.testing import login, setRoles, TEST_USER_ID, TEST_USER_NAME

from collective.querynextprev.browser.viewlets import NextPrevNavigationViewlet
from collective.querynextprev.testing import COLLECTIVE_QUERYNEXTPREV_INTEGRATION_TESTING  # noqa #pylint: disable=C0301
from collective.querynextprev import QUERY, SEARCH_URL, UIDS


query = json.dumps({
    'portal_type': 'Document',
    'sort_on': 'sortable_title'
    })


class DummyView(object):
    pass


class TestNextPrevNavigationViewlet(unittest.TestCase):

    """Test NextPrevNavigationViewlet."""

    layer = COLLECTIVE_QUERYNEXTPREV_INTEGRATION_TESTING

    def setUp(self):
        portal = api.portal.get()
        setRoles(portal, TEST_USER_ID, ['Manager'])
        login(portal, TEST_USER_NAME)
        self.doc = api.content.create(
            id='mydoc', type='Document', container=portal)
        self.view = DummyView()
        portal.REQUEST.SESSION = {}
        self.portal = portal

    def test_no_query_set(self):
        portal = self.portal
        request = portal.REQUEST
        viewlet = NextPrevNavigationViewlet(self.doc, request, self.view)
        viewlet.update()
        session = request.SESSION
        for key in [QUERY, SEARCH_URL, UIDS]:
            self.assertNotIn(key, session)

        self.assertFalse(viewlet.is_navigable)

    def test_alone(self):
        portal = self.portal
        request = portal.REQUEST
        session = request.SESSION
        session[QUERY] = query
        viewlet = NextPrevNavigationViewlet(self.doc, request, self.view)
        viewlet.update()
        self.assertNotIn(QUERY, session)
        self.assertNotIn(UIDS, session)
        self.assertFalse(viewlet.is_navigable)

    def test_not_alone(self):
        portal = self.portal
        request = portal.REQUEST
        session = request.SESSION
        session[QUERY] = query
        doc1 = self.doc
        doc2 = api.content.create(
            id='mydoc2', type='Document', container=portal)
        viewlet = NextPrevNavigationViewlet(doc1, request, self.view)
        viewlet.update()
        self.assertEqual(session[QUERY], query)
        uids = json.loads(session[UIDS])
        self.assertIn(doc1.UID(), uids)
        self.assertIn(doc2.UID(), uids)
        self.assertTrue(viewlet.is_navigable)

    def test_window(self):
        """Test that 10 items before and 10 items after are kept in session."""
        portal = self.portal
        request = portal.REQUEST
        session = request.SESSION
        session[QUERY] = query
        for x in range(100):
            name = "mydoc-{}".format(x)
            api.content.create(id=name, type='Document', container=portal)

        viewlet = NextPrevNavigationViewlet(self.doc, request, self.view)
        viewlet.update()
        self.assertEqual(session[QUERY], query)
        uids = json.loads(session[UIDS])
        self.assertEqual(len(uids), 11)
        self.assertEqual(uids[0], self.doc.UID())
        self.assertTrue(viewlet.is_navigable)

        doc = portal['mydoc-50']
        viewlet = NextPrevNavigationViewlet(doc, request, self.view)
        viewlet.update()
        self.assertEqual(session[QUERY], query)
        uids = json.loads(session[UIDS])
        self.assertEqual(len(uids), 21)
        self.assertEqual(uids[10], doc.UID())
        self.assertTrue(viewlet.is_navigable)
