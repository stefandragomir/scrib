*** Variables ***
${v1}             11
@{v2}             22    33

*** Test Cases ***
tc1
    Should Be Equal    6    7
    Should Be Equal    8    9
    Comment    debug test    debug test 2    debug test 3    debug test 4
    wrong_keyword    ${var1}
    kw1
    kw3    ${var2}

*** Keywords ***
kw1
    Should Be Equal    2    3
    Should Be Equal    4    5

kw3
    Should Be Equal    6    7
    Should Be Equal    8    9
