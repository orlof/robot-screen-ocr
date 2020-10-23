*** Settings ***
Library         ocr.py
Library         RPA.Browser
Test Teardown   Close All Browsers

*** Tasks ***
Documentation
    Open Available Browser    https://robocorp.com
    
    ${matches}=  Search  Documentation
    Click  ${matches[0]}[x]  ${matches[0]}[y]
    
    Sleep  2s


