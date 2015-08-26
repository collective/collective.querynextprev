# -*- coding: utf-8 -*-
"""Viewlets."""
import json

from plone import api
from plone.app.layout.viewlets.common import ViewletBase

from collective.querynextprev import QUERY, UIDS
from collective.querynextprev.utils import expire_session_data


class NextPrevNavigationViewlet(ViewletBase):  # noqa #pylint: disable=W0223

    """Navigation viewlet for next/previous."""

    is_navigable = False

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
                first_index = max(context_index - 10, 0)
                last_index = min(context_index + 10, len(uids))
                session[UIDS] = json.dumps(uids[first_index:last_index+1])
                return  # don't delete session data

        expire_session_data(self.request)
