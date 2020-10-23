# robot-screen-ocr
Simple example of on-screen ocr

## Name of task
This robot contains a python library ocr.py with two keywords: _Search_ and _Click_.

```
Robot Task
    ${matches}=  Search  Documentation
    Click  ${matches[0]}[x]  ${matches[0]}[y]

[
  {
    "text": "Documentation",
    "x": 1100,
    "y": 300    
  }
]
````
