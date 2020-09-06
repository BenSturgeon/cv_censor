from pyresparser import ResumeParser
import re
import pdfx
import pdf_redactor
import nltk
import argparse
import datetime
from datetime import datetime
from nltk.tag import StanfordNERTagger

from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter  # process_pdf
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from io import StringIO


def pdf_to_text(pdfname):
    # PDFMiner boilerplate
    rsrcmgr = PDFResourceManager()
    sio = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, sio, codec=codec, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)

    # Extract text
    fp = open(pdfname, 'rb')
    for page in PDFPage.get_pages(fp):
        interpreter.process_page(page)
    fp.close()

    # Get text from StringIO
    text = sio.getvalue()

    # Cleanup
    device.close()
    sio.close()

    return text


parser = argparse.ArgumentParser(description='Scrub a document of personal information')
parser.add_argument('input', type=str, help='Provide the filename and path to the input')
parser.add_argument('--depth', type=int, default=1,
                    help="minimal or deep name search. 1 provides only first 2 names found. 2 will censor all names "
                         "found")
parser.add_argument('--output_name', type=str, default=None,
                    help="(optional) Specify a specific name for the output file")
args = parser.parse_args()

pdf_name = None
if args.output_name == None:
    pdf_name = args.input
else:
    pdf_name = args.output_name


st = StanfordNERTagger('Stanford_ner/english.all.3class.distsim.crf.ser.gz',
                       'Stanford_ner/stanford-ner.jar')
options = pdf_redactor.RedactorOptions()
options.input_stream = pdf_name
options.output_stream = "cleaned_" +  str(datetime.utcnow())
pdf = pdfx.PDFx(pdf_name)
references_list = pdf.get_references()
data = ResumeParser(pdf_name).get_extracted_data()
# print(data)

text = pdf_to_text(pdf_name)
# print(text)
options.metadata_filters = {
    # Perform some field filtering --- turn the Title into uppercase.

    # Set some values, overriding any value present in the PDF.
    "Producer": [lambda value: "My Name"],
    "CreationDate": [lambda value: datetime.utcnow()],

    # Clear all other fields.
    "DEFAULT": [lambda value: None],
}

# Clear any XMP metadata, if present.
options.xmp_filters = [lambda xml: None]

#compile a list of names in the document using Stanford NER
names = []

for sent in nltk.sent_tokenize(text):
    tokens = nltk.tokenize.word_tokenize(sent)
    tags = st.tag(tokens)
    for tag in tags:
        if tag[1] == 'PERSON':
            names.append(tag[0])
            print(tag)

#Cover exceptions
if data['email'] == None:
    data['email'] = ""
if data['mobile_number'] == None:
    data['mobile_number'] = ""

options.content_filters = [
    (
        # for URLs
        re.compile("[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)"),
        lambda m: "   " #replace with 3 spaces. Other characters for replacement would need to exist in the document.
    ),
    (
        # Probably don't need next 2
        re.compile("\\/URI \\((.*)\\)"),
        lambda m: "   "
    ),
    (
        re.compile("\\/URI"),
        lambda m: "   "
    ),
    (
        # for emails
        re.compile(data['email']),
        lambda m: "   "
    ),
    # First convert all dash-like characters to dashes.
    (
        # for phone numbers
        re.compile(data['mobile_number']),
        lambda m: "   "
    ),
]
print(options.content_filters)
options.link_filters = [
    lambda href, annotation: None
]
exclude = ["Python", "Django", "Matlab"]
names = [v for v in names if v not in exclude]

if args.depth == 1:
    names = names[:2]

for name in names:
    if len(name) < 3:
        names.remove(name)
        continue
    if name.upper() not in names:
        names.append(name.upper())
    if name.lower() not in names:
        names.append(name.lower())



for name in names:
    print(name)
    options.content_filters.append((re.compile(name), lambda m: ""))
pdf_redactor.redactor(options)
