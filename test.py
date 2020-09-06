from pyresparser import ResumeParser
data = ResumeParser('OmkarResume.pdf').get_extracted_data()
print(data)