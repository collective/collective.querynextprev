# -*- coding: utf-8 -*-
"""Test utilities."""
import unittest2 as unittest

from plone import api

from collective.querynextprev.utils import expire_session_data
from collective.querynextprev.testing import COLLECTIVE_QUERYNEXTPREV_INTEGRATION_TESTING  # noqa #pylint: disable=C0301


class TestUtils(unittest.TestCase):

    """Test NextPrevNavigationViewlet."""

    layer = COLLECTIVE_QUERYNEXTPREV_INTEGRATION_TESTING

    def setUp(self):
        portal = api.portal.get()
        self.request = portal.REQUEST

    def tearDown(self):
        del self.request.SESSION

    def test_expire_session_data(self):
        """Test expire_session_data function."""
        request = self.request
        request.SESSION = {}
        expire_session_data(request)
        self.assertEqual(request.SESSION, {})

        request.SESSION = {
            'foo': 'bar',
            'querynextprev.foo': 'bar',
            'querynextprev.bar': 'foo',
            }
        expire_session_data(request)
        self.assertEqual(request.SESSION, {'foo': 'bar'})
