*** Settings ***
Documentation  Plone 6 UI keywords (same names and arguments as ui_plone4.robot)
Resource  plone/app/robotframework/keywords.robot
Resource  plone/app/robotframework/selenium.robot
Library  Remote  ${PLONE_URL}/RobotRemote


*** Keywords ***
The content title is
    [Arguments]  ${title}
    Wait until element contains  css=#content header h1  ${title}

Click the faceted result
    [Documentation]  eea.facetednavigation 16 preview card: title in h5, link "Read more"
    [Arguments]  ${title}
    Click element  xpath=//*[@id="faceted-results"]//*[contains(@class, "card-body")][h5[normalize-space()="${title}"]]//a
