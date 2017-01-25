from PyPDF2 import PdfFileReader
import glob
import os
import csv

class PDFMetadata(object):
    def __init__(self, path, *initial_data, **kwargs):
        self.path = path
        for dictionary in initial_data:
            for key in dictionary:
                setattr(self, key, dictionary[key])
        for key in kwargs:
            setattr(self, key, kwargs[key])


def get_files(filetype, path=os.getcwd(), recursive=False):
    return [file for file in glob.glob(path + '/**/*.{0}'.format(filetype), recursive=recursive)]


def get_metadata_from_dir(filetype='pdf', recursive=False):
    files = get_files(filetype, os.getcwd(), True)
    return [build_metadata_from(file) for file in files]


def build_metadata_from(path):
    properties = get_raw_metadata(path)
    properties = {key.replace("/", ""): item.strip() for key, item in properties.items()}
    return PDFMetadata(path, properties)


def get_raw_metadata(path):
    pdf_toread = PdfFileReader(open(path, "rb"))
    pdf_info = pdf_toread.getDocumentInfo()
    return pdf_info


def export_csv(filename, pdfmetadata_list):
    with open('{0}.csv'.format(filename), 'w') as csvfile:
        fieldnames = ['Title', 'Author']#, 'CreationDate'*/]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        print(pdfmetadata_list)
        for pdf in pdfmetadata_list:
            print(pdf)
            author = getattr(pdf, 'Author') if hasattr(pdf, 'Author') else ''
            creation_date = getattr(pdf, 'CreationDate') if hasattr(pdf, 'CreationDate') else ''
            title = getattr(pdf, 'Title') if hasattr(pdf, 'Title') else ''
            print(title)
            writer.writerow({'Title': title, 'Author': author})#, 'CreationDate': creation_date})


pdf_list = get_metadata_from_dir('pdf', True)
export_csv('export', pdf_list)

