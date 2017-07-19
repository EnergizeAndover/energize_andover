import os
import zipfile
from io import BytesIO
from wsgiref.util import FileWrapper

from django.http import HttpResponse

from ea_parser.script.grapher import file_grapher
from mysite.settings import BASE_DIR

PARSE_CHAR = '/'
GRAPHING_ERROR = 'graph_error.txt'
TEMPORARY_INPUT_FILENAME = 'graph_log.csv'
OUTPUT_FILENAME = 'graph.pdf'
OUTPUT_FILE = 'graph'
OUTPUT_TYPE = '.pdf'


def get_transformed_graph(form_data):
    PARSE_CHAR = form_data['parse_symbol']
    """Transforms and returns the Metasys log file attached to the form"""
    error = False
    multi = 1
    _save_input_graph(form_data['parsed_file'])

    error = _transform_saved_input_graph(form_data['graph_data'],
                                         form_data['graph_period'],
                                         form_data['total_graph'],
                                         form_data['multiplot'],
                                         form_data['graph_title'],
                                         form_data['y_axis_label'],
                                         form_data['graph_type'],
                                         form_data['parse_symbol'],
                                         _temporary_input_graph_path(),
                                         )
    if not form_data['multiplot']:
        for char in form_data['graph_data']:
            if char == PARSE_CHAR:
                multi += 1
    return _respond_with_parsed_file(Errors=error, multi=multi)


def _temporary_input_graph_path():
    return os.path.join(BASE_DIR, TEMPORARY_INPUT_FILENAME)


def _graph_error_file_path():
    return os.path.join(BASE_DIR, GRAPHING_ERROR)


def _temporary_output_graph_path():
    return os.path.join(BASE_DIR, OUTPUT_FILENAME)


def _save_input_graph(temporary_file):
    """Save the uploaded file to disk so it can be handled by the grapher module"""
    with open(_temporary_input_graph_path(), 'wb') as fout:
        for chunk in temporary_file.chunks():
            fout.write(chunk)


def _transform_saved_input_graph(ftg,
                                 grouping,
                                 total,
                                 multiplot,
                                 title,
                                 ylabel,
                                 graph_type,
                                 symbol,
                                 input_file_path
                                 ):
    count = 0
    error = False
    if symbol == None:
      multifield = ftg
    else:
        PARSE_CHAR = symbol
        multifield = []
        temp = ''
        print(PARSE_CHAR)
        for char in ftg:
            if not char == PARSE_CHAR:
                temp += char
            else:
                multifield.append(temp)
                temp = ''
        multifield.append(temp)
    if not multiplot:
        for fields in multifield:
            if count == 0:
                error = error or file_grapher(input_file_path,
                                              output_file_name=_temporary_output_graph_path(),
                                              field_to_graph=fields,
                                              grouping=grouping,
                                              total=total,
                                              title=title,
                                              units=ylabel,
                                              graph_type=graph_type,
                                              )
            else:
                error = error or file_grapher(input_file_path,
                                              output_file_name=os.path.join(BASE_DIR, OUTPUT_FILE+str(count)+OUTPUT_TYPE),
                                              field_to_graph=fields,
                                              grouping=grouping,
                                              total=total,
                                              title=title,
                                              units=ylabel,
                                              graph_type=graph_type,
                                              )
            count += 1
        return error
    else:
        return file_grapher(input_file_path,
                            output_file_name=_temporary_output_graph_path(),
                            field_to_graph=multifield,
                            grouping=grouping,
                            total=total,
                            title=title,
                            units=ylabel,
                            graph_type=graph_type,
                            )




def _respond_with_parsed_file(Errors=False, multi=0):
    if (not Errors) and multi <= 1:
        graph = open(_temporary_output_graph_path(), 'rb')
        response = HttpResponse(FileWrapper(graph), content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="%s"' % OUTPUT_FILENAME
    else:
        if multi <= 1:
            files = [_temporary_output_graph_path(), _graph_error_file_path()]
        elif Errors:
            files = [_temporary_output_graph_path(), _graph_error_file_path()]
            cnt = 1
            while cnt < multi:
                files.append(os.path.join(BASE_DIR, OUTPUT_FILE+str(cnt)+OUTPUT_TYPE))
                cnt += 1
        else:
            files = [_temporary_output_graph_path()]
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
    return response
