# -*- coding: utf-8 -*-
"""Viewlets."""
from collective.beaker.interfaces import ISession
from collective.querynextprev import NEXT_UIDS
from collective.querynextprev import PREVIOUS_UIDS
from collective.querynextprev import QUERY
from collective.querynextprev.interfaces import INextPrevNotNavigable
from collective.querynextprev.utils import convert_to_str
from collective.querynextprev.utils import expire_session_data
from collective.querynextprev.utils import first_common_item
from collective.querynextprev.utils import get_next_items
from collective.querynextprev.utils import get_previous_items
from collective.querynextprev.utils import json_object_hook
from plone import api
from plone.app.layout.viewlets.common import ViewletBase
from plone.protect.utils import addTokenToUrl

import json


class NextPrevNavigationViewlet(ViewletBase):
    """Navigation viewlet for next/previous."""

    is_navigable = False
    previous_uids = []
    next_uids = []

    @property
    def go_to_previous_link(self):
        url = f"{self.context.absolute_url()}/@@go_to_previous_item"
        return addTokenToUrl(url)

    @property
    def go_to_next_link(self):
        url = f"{self.context.absolute_url()}/@@go_to_next_item"
        return addTokenToUrl(url)

    def update(self):
        if INextPrevNotNavigable.providedBy(self.context):
            return

        session = ISession(self.request)
        if session and QUERY in session:
            query = session[QUERY]
            params = convert_to_str(json.loads(query, object_hook=json_object_hook))
            catalog = api.portal.get_tool("portal_catalog")
            brains = catalog.searchResults(**params)

            # if we have too many results, we return and delete session data
            max_res = (
                api.portal.get_registry_record("collective.querynextprev.maxresults")
                or 250
            )
            if len(brains) > max_res:
                self.is_navigable = False
                expire_session_data(session)
                return

            uids = [brain.UID for brain in brains]
            context_uid = self.context.UID()
            if context_uid in uids and len(uids) > 1:
                self.is_navigable = True
                context_index = uids.index(context_uid)
                self.previous_uids = list(
                    reversed(get_previous_items(uids, context_index))
                )
                self.next_uids = get_next_items(uids, context_index)
                session[PREVIOUS_UIDS] = json.dumps(self.previous_uids)
                session[NEXT_UIDS] = json.dumps(self.next_uids)
                session.save()
                return  # don't delete session data
            elif PREVIOUS_UIDS in session or NEXT_UIDS in session:
                # context is not in results anymore
                # get previous
                old_previous = json.loads(session[PREVIOUS_UIDS])
                previous_item = first_common_item(uids, old_previous)
                if previous_item:
                    self.is_navigable = True
                    index = uids.index(previous_item)
                    self.previous_uids = list(
                        reversed(get_previous_items(uids, index, include_index=True))
                    )
                    session[PREVIOUS_UIDS] = json.dumps(self.previous_uids)

                # get next
                old_next = json.loads(session[NEXT_UIDS])
                next_item = first_common_item(uids, old_next)
                if next_item:
                    self.is_navigable = True
                    index = uids.index(next_item)
                    self.next_uids = get_next_items(uids, index, include_index=True)
                    session[NEXT_UIDS] = json.dumps(self.next_uids)

                session.save()
                if previous_item or next_item:
                    return  # don't delete session data

            expire_session_data(session)
