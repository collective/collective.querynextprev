# -*- coding: utf-8 -*-

from collective.beaker.interfaces import ISession
from collective.beaker.testing import BEAKER_FIXTURE
from collective.beaker.testing import testingSession
from DateTime import DateTime
from eea.facetednavigation.interfaces import IPossibleFacetedNavigable
from plone import api
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.testing.zope import WSGI_SERVER_FIXTURE
from zope.component import provideAdapter
from zope.interface import alsoProvides
from zope.publisher.interfaces.http import IHTTPRequest

import collective.querynextprev
import eea.facetednavigation


class CollectiveQuerynextprevLayer(PloneSandboxLayer):

    defaultBases = (BEAKER_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        self.loadZCML(package=collective.querynextprev)
        provideAdapter(testingSession, (IHTTPRequest,), ISession)

    def setUpPloneSite(self, portal):
        applyProfile(portal, "collective.querynextprev:default")


COLLECTIVE_QUERYNEXTPREV_FIXTURE = CollectiveQuerynextprevLayer()


COLLECTIVE_QUERYNEXTPREV_INTEGRATION_TESTING = IntegrationTesting(
    bases=(COLLECTIVE_QUERYNEXTPREV_FIXTURE,),
    name="CollectiveQuerynextprevLayer:IntegrationTesting",
)


COLLECTIVE_QUERYNEXTPREV_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(COLLECTIVE_QUERYNEXTPREV_FIXTURE,),
    name="CollectiveQuerynextprevLayer:FunctionalTesting",
)


def create_search_pages(portal):
    """Faceted folder "search-pages" listing the pages Page 1, Page 2, Page 3 in this order."""
    with api.env.adopt_roles(["Manager"]):
        folder = api.content.create(
            container=portal, type="Folder", id="search-pages", title="Search pages"
        )
        # eea.facetednavigation 16: the "eea.faceted.navigable" behavior is not on Folder
        alsoProvides(folder, IPossibleFacetedNavigable)
        folder.unrestrictedTraverse("@@faceted_subtyper").enable()
        # default faceted configuration: Documents sorted on effective (reverse)
        for day, title in ((3, "Page 1"), (2, "Page 2"), (1, "Page 3")):
            page = api.content.create(container=folder, type="Document", title=title)
            page.setEffectiveDate(DateTime("2020/01/0{} 12:00".format(day)))
            page.reindexObject()


class CollectiveQuerynextprevRobotLayer(PloneSandboxLayer):
    """Real beaker memory sessions across requests: no testingSession adapter."""

    defaultBases = (BEAKER_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        self.loadZCML(package=eea.facetednavigation)
        self.loadZCML(package=collective.querynextprev)

    def setUpPloneSite(self, portal):
        applyProfile(portal, "eea.facetednavigation:default")
        applyProfile(portal, "collective.querynextprev:default")
        # eea.facetednavigation 16 async bundles: results randomly never load (jQuery.bbq undefined)
        for bundle in ("faceted.jquery", "faceted.view", "faceted.edit"):
            record = "plone.bundles/{}.load_async".format(bundle)
            if api.portal.get_registry_record(record, default=None) is not None:
                api.portal.set_registry_record(record, False)
        create_search_pages(portal)


COLLECTIVE_QUERYNEXTPREV_ROBOT_FIXTURE = CollectiveQuerynextprevRobotLayer()


COLLECTIVE_QUERYNEXTPREV_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        COLLECTIVE_QUERYNEXTPREV_ROBOT_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        WSGI_SERVER_FIXTURE,
    ),
    name="CollectiveQuerynextprevLayer:AcceptanceTesting",
)
