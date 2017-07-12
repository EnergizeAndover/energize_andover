import os
import zipfile
from io import BytesIO

from django.http import HttpResponse

from ea_parser.script.parse import parse, summarize, save_df, header_parse

from .file_transfer_grapher import  _transform_saved_input_graph, _temporary_output_graph_path, _graph_error_file_path

from mysite.settings import BASE_DIR

OUTPUT_FILE = 'graph'
OUTPUT_TYPE = '.pdf'
TEMPORARY_INPUT_FILENAME = 'metasys_log.txt'
OUTPUT_FILENAME = 'parsed_metasys_log.csv'
TEMPORARY_INPUT_HEADER_FILENAME = 'column_headers.csv'

def graph_transformed_file(graph_data):
    multi = 1
    error = _transform_saved_input_graph(graph_data['graph_data'],
                                         graph_data['graph_period'],
                                         graph_data['total_graph'],
                                         graph_data['multiplot'],
                                         graph_data['graph_title'],
                                         graph_data['y_axis_label'],
                                         graph_data['graph_type'],
                                         None,  # graphing_data['parse_symbol'],
                                         _temporary_output_file_path()
                                         )
    if not graph_data['multiplot']:
        for char in graph_data['graph_data']:
            if char == '/':
                multi += 1
    return _respond_with_parsed_file(True, error=error, multi=multi)

def get_transformed_file(form_data, graphing_data=None):
    error = False
    multi = 1
    """Transforms and returns the Metasys log file attached to the form"""
    _save_input_file(form_data['metasys_file'])
    _save_input_header_file(form_data['columns_file'])
    _transform_saved_input_file(
        return_summarized_data=form_data['summarize'],
        cost=form_data['cost'],
        start_date=form_data['start_time'],
        end_date=form_data['end_time']
    )

    if graphing_data is None:
        return _respond_with_parsed_file(form_data['graph'], error=error, multi=multi)
    else:
        return None


def _temporary_input_file_path():
    return os.path.join(BASE_DIR, TEMPORARY_INPUT_FILENAME)

def _temporary_input_header_file_path():
    return os.path.join(BASE_DIR, TEMPORARY_INPUT_HEADER_FILENAME)


def _temporary_output_file_path():
    return os.path.join(BASE_DIR, OUTPUT_FILENAME)

def _save_input_header_file(temporary_file):
    """Save the uploaded file to disk so it can be handled by the parse module"""
    with open(_temporary_input_header_file_path(), 'wb') as fout:
        for chunk in temporary_file.chunks():
            fout.write(chunk)


def _save_input_file(temporary_file):
    """Save the uploaded file to disk so it can be handled by the parse module"""
    with open(_temporary_input_file_path(), 'wb') as fout:
        for chunk in temporary_file.chunks():
            fout.write(chunk)


def _transform_saved_input_file(return_summarized_data, cost, start_date, end_date):
    df = parse(_temporary_input_file_path())
    columns = header_parse(_temporary_input_header_file_path())
    if return_summarized_data:
        df = summarize(df, columns, start_date, end_date)
    save_df(df, summarize, None, None, _temporary_output_file_path())


def _respond_with_parsed_file(ziprtn, error=False, multi=1,):
    if ziprtn:
        if (not error) and (multi <= 1):
            files = [_temporary_output_file_path(), _temporary_output_graph_path()]
        elif multi <= 1:
            files = [_temporary_output_file_path(), _temporary_output_graph_path(), _graph_error_file_path()]
        elif error:
            files = [_temporary_output_file_path(), _temporary_output_graph_path(), _graph_error_file_path()]
            cnt = 1
            while cnt < multi:
                files.append(os.path.join(BASE_DIR, OUTPUT_FILE + str(cnt) + OUTPUT_TYPE))
                cnt += 1
        else:
            files = [_temporary_output_file_path(), _temporary_output_graph_path()]
            cnt = 1
            while cnt < multi:
                files.append(os.path.join(BASE_DIR, OUTPUT_FILE + str(cnt) + OUTPUT_TYPE))
                cnt += 1

        zip_subdir = "Parse_And_Graph"
        zip_filename = "%s.zip" % zip_subdir

        s = BytesIO()

        zf = zipfile.ZipFile(s, "w")

        for fpath in files:
            fdir, fname = os.path.split(fpath)
            zip_path = os.path.join(zip_subdir, fname)

            zf.write(fpath, zip_path)

        zf.close()

        response = HttpResponse(s.getvalue(), content_type="application/x-zip-compressed")
        response["Content-Disposition"] = "attachment; filename=%s" % zip_filename
        pass
    else:
        parsed_file = open(_temporary_output_file_path()).read()
        response = HttpResponse(parsed_file, content_type='text/plain')
        response['Content-Disposition'] = 'attachment; filename="%s"' % OUTPUT_FILENAME

    return response
