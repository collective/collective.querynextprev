# -*- coding: utf-8 -*-
"""Test views."""
import unittest2 as unittest

from plone import api

from collective.querynextprev.testing import COLLECTIVE_QUERYNEXTPREV_INTEGRATION_TESTING  # noqa #pylint: disable=C0301
from collective.querynextprev.browser.views import GoToNextItem
from collective.querynextprev.browser.views import GoToPreviousItem


class DummyView(object):
    pass


class TestViews(unittest.TestCase):

    """Test views."""

    layer = COLLECTIVE_QUERYNEXTPREV_INTEGRATION_TESTING

    def test_find_next_item(self):
        """Test find_item for GoToNextItem view."""
        portal = api.portal.get()
        view = GoToNextItem(portal, DummyView())

        l1 = [0, 1, 2, 3, 4, 5]
        l2 = [0, 1, 4, 5]
        self.assertEqual(view.find_item(l2, l1.index(2), [2]), 4)

        l1 = [0, 1, 2, 3, 4, 5]
        l2 = [0, 1, 2, 3, 4, 5]
        self.assertEqual(view.find_item(l2, l1.index(2), [2]), 3)

        l1 = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        l2 = [0, 1, 2, 3, 4, 5]
        self.assertIsNone(view.find_item(l2, l1.index(5), [5]))

        l1 = [0, 1, 2, 3, 4, 5, 6]
        l2 = [0, 1, 2, 3, 4, 5, 6]
        self.assertEqual(view.find_item(l2, l1.index(5), [5]), 6)

    def test_find_previous_item(self):
        """Test find_item for GoToPreviousItem view."""
        portal = api.portal.get()
        view = GoToPreviousItem(portal, DummyView())

        l1 = [0, 1, 2, 3, 4, 5]
        l2 = [0, 2, 2, 3, 4, 5]
        self.assertEqual(view.find_item(l2, l1.index(2), [2]), 0)

        l1 = [0, 1, 2, 3, 4, 5]
        l2 = [0, 1, 2, 3, 4, 5]
        self.assertEqual(view.find_item(l2, l1.index(2), [2]), 1)

        l1 = [0, 1, 2]
        l2 = [0, 1, 2]
        self.assertIsNone(view.find_item(l2, l1.index(0), [0]))

        l1 = [0, 1, 2]
        l2 = []
        self.assertIsNone(view.find_item(l2, l1.index(0), [0]))

        l1 = [0, 1, 2, 3, 4, 5, 6]
        l2 = [0, 1, 2, 3, 4, 5, 6]
        self.assertEqual(view.find_item(l2, l1.index(5), [5]), 4)
