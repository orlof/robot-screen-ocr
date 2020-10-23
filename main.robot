*** Settings ***
Library         RPA.Browser

*** Task ***
Default
	Open Available Browser  http://www.robocorp.com/
	Sleep  5s
	Close All browsers
