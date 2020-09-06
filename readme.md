A project that pulls on a few different NER tools in order to parse sensitive client information and remove it from a resume or CV document.

# Installation

1. Install the latest version of python

2. Installation of python packages. 

I recommend doing this through: 

$pip install -r requirements.txt

## Execution

The system can be run by passing a pdf file as an argument to hide.py.

An example: 

$ python3 hide.py Benjamin_Sturgeon_Resume.pdf

Two further arguments can be passed, depth of name search and a custom output name. 
In the default case it would be best if the file being converted is in the current directory. 

###### Expected input:

Installing facilities to convert docx and doc to pdf.

I found this can be achieved on a debian system through:

$sudo apt install abiword

To use above facilities for conversion of a file from doc/docx to pdf on a linux system I have found the following shell command to be effective:

$ abiword --to=pdf filetoconvert.docx


