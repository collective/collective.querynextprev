*** Settings ***
Documentation  collective.querynextprev keywords, built on the ui_plone${PLONE_MAJOR}.robot keywords.
...            Robot Framework 3.0 syntax (shared with the Plone 4.3 environment).
...            Fixture (testing.create_search_pages): faceted folder "search-pages" listing Page 1, Page 2, Page 3.
...            Selectors: eea.facetednavigation and this package.
Resource  ui_plone${PLONE_MAJOR}.robot


*** Variables ***
${RESULTS}  css=#faceted-results
${NEXT}  css=#querynextprev-navigation #query-nextprev-next
${PREVIOUS}  css=#querynextprev-navigation #query-nextprev-prev


*** Keywords ***
Open a manager browser
    Open test browser
    Set window size  1280  2000
    Enable autologin as  Manager

Search the pages
    Go to  ${PLONE_URL}/search-pages
    Wait until page contains element  ${RESULTS}
    Wait until element is not visible  css=.faceted-lock-overlay
    Wait until page contains element  ${RESULTS} a

Open the result
    [Arguments]  ${title}
    Click the faceted result  ${title}
    The content title is  ${title}

Go to the next item
    Click element  ${NEXT}

Go to the previous item
    Click element  ${PREVIOUS}

The navigation links are
    [Documentation]  shown or hidden (argument names differ from the case-insensitive selector variables)
    [Arguments]  ${previous_link}  ${next_link}
    Run keyword if  '${previous_link}' == 'shown'  Page should contain element  ${PREVIOUS}
    ...  ELSE  Page should not contain element  ${PREVIOUS}
    Run keyword if  '${next_link}' == 'shown'  Page should contain element  ${NEXT}
    ...  ELSE  Page should not contain element  ${NEXT}
