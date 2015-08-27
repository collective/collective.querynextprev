# -*- coding: utf-8 -*-
"""Viewlets."""
import json

from plone import api
from plone.app.layout.viewlets.common import ViewletBase

from collective.querynextprev import QUERY, PREVIOUS_UIDS, NEXT_UIDS
from collective.querynextprev.utils import (
    expire_session_data, get_next_items, get_previous_items)


class NextPrevNavigationViewlet(ViewletBase):  # noqa #pylint: disable=W0223

    """Navigation viewlet for next/previous."""

    is_navigable = False
    previous_uids = []
    next_uids = []

    def update(self):
        session = self.request.SESSION
        if session.has_key(QUERY):  # noqa
            query = session[QUERY]
            params = json.loads(query)
            catalog = api.portal.get_tool('portal_catalog')
            uids = [brain.UID for brain in catalog.searchResults(**params)]  # noqa #pylint: disable=E1103
            context_uid = self.context.UID()
            if context_uid in uids and len(uids) > 1:
                self.is_navigable = True
                context_index = uids.index(context_uid)
                self.previous_uids = list(reversed(
                    get_previous_items(uids, context_index)))
                self.next_uids = get_next_items(uids, context_index)
                session[PREVIOUS_UIDS] = json.dumps(self.previous_uids)
                session[NEXT_UIDS] = json.dumps(self.next_uids)
                return  # don't delete session data

        expire_session_data(self.request)
