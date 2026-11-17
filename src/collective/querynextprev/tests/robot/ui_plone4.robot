*** Settings ***
Documentation  Plone 4 UI keywords (same names and arguments as ui_plone6.robot)
Resource  plone/app/robotframework/keywords.robot
Resource  plone/app/robotframework/selenium.robot
Library  Remote  ${PLONE_URL}/RobotRemote


*** Keywords ***
The content title is
    [Arguments]  ${title}
    Wait until element contains  css=h1.documentFirstHeading  ${title}

Click the faceted result
    [Documentation]  eea.facetednavigation 14 preview item: the link contains the title
    [Arguments]  ${title}
    Click element  xpath=//*[@id="faceted-results"]//a[contains(normalize-space(.), "${title}")]
