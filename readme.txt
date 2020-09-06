A project that pulls on a few different NER tools in order to parse sensitive client information and remove it from a resume or CV document.

A few steps are required for installation:
It is assumed that the latest version of python is installed on the system.

1. Installation of python packages. 

I recommend doing this through: 

$pip install -r requirements.txt

2.

This should provide all the necessary libraries. There are a number of dependencies built into the directory. 

The system can be run by passing a pdf file as an argument to hide.py.

An example: 

python3 hide.py OmkarResume.pdf

Two further arguments can be passed, depth of name search and a custom output name. 
In the default case it would be best if the file being converted is in the current directory. 

Expected input:

Installing facilities to convert docx and doc to pdf.

I found this can be achieved on a debian system through:

$sudo apt install abiword

To use above facilities for conversion of a file from doc/docx to pdf on a linux system I have found the following shell command to be effective:

$ abiword --to=pdf filetoconvert.docx


