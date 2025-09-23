# -*- coding: utf-8 -*-
"""Test utilities."""
from collective.beaker.interfaces import ENVIRON_KEY
from collective.beaker.interfaces import ISession
from collective.querynextprev.testing import COLLECTIVE_QUERYNEXTPREV_INTEGRATION_TESTING
from collective.querynextprev.utils import clean_query
from collective.querynextprev.utils import expire_session_data
from collective.querynextprev.utils import first_common_item
from collective.querynextprev.utils import get_next_items
from collective.querynextprev.utils import get_previous_items
from plone import api

import unittest


class TestUtils(unittest.TestCase):
    """Test NextPrevNavigationViewlet."""

    layer = COLLECTIVE_QUERYNEXTPREV_INTEGRATION_TESTING

    def setUp(self):
        portal = api.portal.get()
        self.request = portal.REQUEST

    def tearDown(self):
        if hasattr(self.request, "SESSION"):
            del self.request.environ[ENVIRON_KEY]

    def test_expire_session_data(self):
        """Test expire_session_data function."""
        request = self.request
        session = ISession(request)
        self.assertEqual(session, {})
        expire_session_data(session)
        self.assertEqual(ISession(request), {})

        session = ISession(request)
        session["foo"] = "bar"
        session["querynextprev.foo"] = "bar"
        session["querynextprev.bar"] = "foo"
        expire_session_data(session)
        self.assertEqual(ISession(request), {"foo": "bar"})

    def test_first_common_item(self):
        """Test first common item util."""
        l1 = [4, 5, 6, 7]
        l2 = [1, 2, 6, 7]

        self.assertEqual(first_common_item(l1, l2), 6)

        l1 = [1, 2, 4, 5, 6, 7]
        l2 = [1, 2, 6, 7]
        self.assertEqual(first_common_item(l1, l2), 1)

        l1 = [4, 5, 6, 7]
        l2 = [1, 2]
        self.assertIsNone(first_common_item(l1, l2))

        l1 = [1]
        l2 = [1]
        self.assertEqual(first_common_item(l1, l2), 1)

    def test_get_next_items(self):
        """Test get_next_items function."""
        lst = list(range(40))
        index = 19
        self.assertEqual(get_next_items(lst, index), list(range(20, 30)))

        index = 35
        self.assertEqual(get_next_items(lst, index), list(range(36, 40)))

        self.assertEqual(
            get_next_items(lst, index, include_index=True), list(range(35, 40))
        )

    def test_get_previous_items(self):
        """Test get_previous_items function."""
        lst = list(range(40))
        index = 21
        self.assertEqual(get_previous_items(lst, index), list(range(11, 21)))

        index = 5
        self.assertEqual(get_previous_items(lst, index), list(range(5)))

        self.assertEqual(
            get_previous_items(lst, index, include_index=True), list(range(6))
        )

    def test_clean_query(self):
        query = {
            "sort_order": "descending",
            "Language": ["fr", ""],
            "sort_on": "created",
            "facet.field": [
                "",
                "review_state",
                "treating_groups",
                "assigned_user",
                "recipient_groups",
                "mail_type",
            ],
            "b_size": 24,
            "b_start": 0,
            "portal_type": {"query": ["dmsincomingmail"]},
        }
        self.assertDictEqual(
            clean_query(query),
            {
                "sort_order": "descending",
                "Language": ["fr", ""],
                "sort_on": "created",
                "portal_type": {"query": ["dmsincomingmail"]},
            },
        )
