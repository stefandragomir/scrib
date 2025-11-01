*** Variables ***
${v3}             55

*** Test Cases ***
tc2
    Should Be Equal    6    7
    Should Be Equal    8    9
    kw2
    kw4

*** Keywords ***
kw2
    Should Be Equal    6    7
    Should Be Equal    8    9

kw4
    Should Be Equal    6    11
    Should Be Equal    8    9
