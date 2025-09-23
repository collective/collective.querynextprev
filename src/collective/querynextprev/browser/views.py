# -*- coding: utf-8 -*-
"""Views."""
from collective.beaker.interfaces import ISession
from collective.querynextprev import NEXT_UIDS
from collective.querynextprev import PREVIOUS_UIDS
from collective.querynextprev import QUERY
from collective.querynextprev import SEARCH_URL
from collective.querynextprev.utils import convert_to_str
from collective.querynextprev.utils import expire_session_data
from collective.querynextprev.utils import first_common_item
from collective.querynextprev.utils import get_next_items
from collective.querynextprev.utils import get_previous_items
from collective.querynextprev.utils import json_object_hook
from plone import api
from Products.Five.browser import BrowserView

import json


class GoToNextItem(BrowserView):
    """Redirect to next item in query."""

    uids_param = NEXT_UIDS

    def get_uids(self):
        """Get uids of the query results."""
        catalog = api.portal.get_tool("portal_catalog")
        session = ISession(self.request)
        params = convert_to_str(
            json.loads(
                session[QUERY],
                object_hook=json_object_hook,
            )
        )
        return [brain.UID for brain in catalog.searchResults(**params)]

    def __call__(self):
        request = self.request
        session = ISession(self.request)
        if QUERY in session and self.uids_param in session:
            next_uids = convert_to_str(json.loads(session[self.uids_param]))

            # reexecute the query to search within most recent results
            new_uids = self.get_uids()

            # search UID starting from context index in uids
            uid = first_common_item(next_uids, new_uids)
            if uid is not None:
                next_url = api.content.get(UID=uid).absolute_url()

                # update uids in session
                index = new_uids.index(uid)
                previous_uids = list(reversed(get_previous_items(new_uids, index)))
                next_uids = get_next_items(new_uids, index)
                session[PREVIOUS_UIDS] = json.dumps(previous_uids)
                session[NEXT_UIDS] = json.dumps(next_uids)
                session.save()

                request.response.redirect(next_url)
                return  # don't expire session data

        if SEARCH_URL in session:
            request.response.redirect(session[SEARCH_URL])
        else:
            request.response.redirect(api.portal.get().absolute_url())

        expire_session_data(session)
        return


class GoToPreviousItem(GoToNextItem):
    """Redirect to previous item in query."""

    uids_param = PREVIOUS_UIDS

    def get_uids(self):
        """Reverse uids."""
        uids = super(GoToPreviousItem, self).get_uids()
        uids.reverse()
        return uids
