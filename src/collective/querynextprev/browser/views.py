# -*- coding: utf-8 -*-
"""Views."""
import json

from Products.Five.browser import BrowserView
from plone import api

from collective.querynextprev import QUERY, UIDS, SEARCH_URL
from collective.querynextprev.utils import expire_session_data


class GoToItem(BrowserView):

    """Base class for GoToPreviousItem/GoToNextItem."""

    def find_item(self, new_uids, context_index, context_uid):  #pylint: disable=W0613
        """Override this method."""
        return NotImplemented

    def __call__(self):
        session = self.request.SESSION
        if session.has_key(QUERY) and session.has_key(UIDS):
            uids = json.loads(session[UIDS])
            params = json.loads(session[QUERY])

            # reexecute the query to search within most recent results
            catalog = api.portal.get_tool('portal_catalog')
            new_uids = [brain.UID for brain in catalog.searchResults(**params)]  #pylint: disable=E1103

            # search UID starting from context index in uids
            context_uid = self.context.UID()
            if context_uid in uids:
                context_index = uids.index(context_uid)
                uid = self.find_item(new_uids, context_index, [context_uid])

                if uid is not None:
                    next_url = api.content.get(UID=uid).absolute_url()

                    # update cookie
                    session[UIDS] = json.dumps(new_uids)

                    self.request.response.redirect(next_url)
                    return  # don't expire cookies

        if session.has_key(SEARCH_URL):
            self.request.response.redirect(session[SEARCH_URL])
        else:
            self.request.response.redirect(api.portal.get().absolute_url())

        expire_session_data(self.request)
        return


class GoToPreviousItem(GoToItem):

    """Go to previous item."""

    def find_item(self, items, index, excluded):
        """Find previous item in list starting from index."""
        if index < 0:
            return None
        elif items[index] not in excluded:
            return items[index]
        else:
            return self.find_item(items, index - 1, excluded)


class GoToNextItem(GoToItem):

    """Go to next item."""

    def find_item(self, items, index, excluded):
        """Find next item in list starting from index."""
        if index >= len(items):
            return None
        elif items[index] not in excluded:
            return items[index]
        else:
            return self.find_item(items, index + 1, excluded)
