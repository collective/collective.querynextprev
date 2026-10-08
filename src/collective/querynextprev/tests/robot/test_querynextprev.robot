*** Settings ***
Documentation  Next/Previous navigation through the results of a faceted search.
...            Version-independent: Plone selectors are in ui_plone*.robot.
Resource  querynextprev.robot
Test Setup  Open a manager browser
Test Teardown  Close all browsers


*** Test Cases ***
Next and Previous follow the faceted search results
    Search the pages
    Open the result  Page 2
    The navigation links are  shown  shown
    Go to the next item
    The content title is  Page 3
    The navigation links are  shown  hidden
    Go to the previous item
    The content title is  Page 2
    Go to the previous item
    The content title is  Page 1
    The navigation links are  hidden  shown

A page opened outside a search has no navigation
    Go to  ${PLONE_URL}/search-pages/page-2
    The content title is  Page 2
    The navigation links are  hidden  hidden
