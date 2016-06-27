from django.http import HttpResponse
from mysite.settings import BASE_DIR
#from energize_andover.script.parse import parse, summarize, save_df
from energize_andover.energize_andover.script.parse import parse, summarize, save_df
import os
from datetime import datetime

TEMPORARY_INPUT_FILENAME = 'metasys_log.txt'
OUTPUT_FILENAME = 'parsed_metasys_log.csv'

def get_transformed_file(form_data):
    """Transforms and returns the Metasys log file attached to the form"""
    _save_input_file(form_data['metasys_file'])
    _transform_saved_input_file(
        return_summarized_data=form_data['summarize'],
        cost=form_data['cost'],
        start_date=form_data['start_time'],
        end_date=form_data['end_time']
    )
    return _respond_with_parsed_file()

def _temporary_input_file_path():
    return os.path.join(BASE_DIR, TEMPORARY_INPUT_FILENAME)

def _temporary_output_file_path():
    return os.path.join(BASE_DIR, OUTPUT_FILENAME)

def _save_input_file(temporary_file):
    """Save the uploaded file to disk so it can be handled by the parse module"""
    with open(_temporary_input_file_path(), 'wb') as fout:
        for chunk in temporary_file.chunks():
            fout.write(chunk)

def _transform_saved_input_file(return_summarized_data, cost, start_date, end_date):
    df = parse(_temporary_input_file_path())
    if return_summarized_data:
        df = summarize(df, cost, start_date, end_date)
    save_df(df, summarize, None, None, _temporary_output_file_path())

def _respond_with_parsed_file():
    parsed_file = open(_temporary_output_file_path()).read()
    response = HttpResponse(parsed_file, content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename="%s"' % OUTPUT_FILENAME

    return response
