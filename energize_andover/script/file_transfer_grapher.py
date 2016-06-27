from django.http import HttpResponse
from mysite.settings import BASE_DIR
from wsgiref.util import FileWrapper
#from energize_andover.script.grapher import file_parser
from energize_andover.energize_andover.script.grapher import file_parser
import os
from io import BytesIO
from reportlab.pdfgen import canvas
from datetime import datetime

TEMPORARY_INPUT_FILENAME = 'graph_log.csv'
OUTPUT_FILENAME = 'graph.pdf'

def get_transformed_graph(form_data):
    """Transforms and returns the Metasys log file attached to the form"""
    _save_input_file(form_data['parsed_file'])
    _transform_saved_input_file(form_data['graph_data'],
                                #form_data['graph_period'],
    )
    return _respond_with_parsed_file()

def _temporary_input_file_path():
    return os.path.join(BASE_DIR, TEMPORARY_INPUT_FILENAME)

def _temporary_output_file_path():
    return os.path.join(BASE_DIR, OUTPUT_FILENAME)

def _save_input_file(temporary_file):
    """Save the uploaded file to disk so it can be handled by the grapher module"""
    with open(_temporary_input_file_path(), 'wb') as fout:
        for chunk in temporary_file.chunks():
            fout.write(chunk)

def _transform_saved_input_file(ftg,
                                #grouping
                                ):
    file_parser(_temporary_input_file_path(),
                output_file_name=_temporary_output_file_path(),
                field_to_graph=ftg,
                #grouping=grouping,
                )


def _respond_with_parsed_file():
    graph = open(_temporary_output_file_path(), 'rb')
    response = HttpResponse(FileWrapper(graph), content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="%s"' % OUTPUT_FILENAME
    return response