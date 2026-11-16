*** Settings ***
Resource  resource.robot
Suite Setup     Open And Configure Browser
Suite Teardown  Close Browser
Test Setup      Reset Application Create User And Go To Register Page

*** Test Cases ***

Register With Valid Username And Password
    Set Username  kalle
    Set Password  12345678
    Click  button >> text=Register
    Register Should Succeed

Register With Too Short Username And Valid Password
    Set Username  ka
    Set Password  12345678
    Click  button >> text=Register
    Register Should Fail With Message  Username should contain at least 3 characters

Register With Valid Username And Too Short Password
    Set Username  kalle
    Set Password  123
    Click  button >> text=Register
    Register Should Fail With Message  Password should contain at least 8 characters

Register With Username That Is Already In Use
    Set Username  ville
    Set Password  12345678
    Click  button >> text=Register
    Register Should Fail With Message  Username is already taken

*** Keywords ***
Set Username
    [Arguments]  ${username}
    Fill Text  id=username  ${username}

Set Password
    [Arguments]  ${password}
    Fill Secret  id=password  $password
    Fill Secret  id=password_confirmation  $password

Register Should Succeed
    Welcome Page Should Be Open

Register Should Fail With Message
    [Arguments]  ${message}
    Register Page Should Be Open
    Get Text  body  *=  ${message}

Reset Application Create User And Go To Register Page
    Reset Application
    Create User  ville  ville123 
    Go To Register Page