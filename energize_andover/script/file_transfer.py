from django.http import HttpResponse
from mysite.settings import BASE_DIR
from io import BytesIO
import zipfile
from energize_andover.script.parse import parse, summarize, save_df
from energize_andover.script.file_transfer_grapher import  _transform_saved_input_graph, _temporary_output_graph_path
#from energize_andover.energize_andover.script.parse import parse, summarize, save_df
import os
from datetime import datetime

field_type = dict([('MAIN ELECTRIC METER.Analog Inputs.Energy.Main-kWh-Energy (Trend1)',
                   True),
                  ('MAIN ELECTRIC METER.Analog Inputs.KVAR_Present_Demand.Main-kVAR_Present_Demand (Trend1)',
                   False),
                  ('MAIN ELECTRIC METER.Analog Inputs.KVAR_Total.Main-kVAR (Trend1)',
                   False),
                  ('MAIN ELECTRIC METER.Analog Inputs.KVARh.Main-kVARh (Trend1)',
                   True),
                  ('MAIN ELECTRIC METER.Analog Inputs.KVA_Present_Demand.Main-kVA_Present_Demand (Trend1)',
                   False),
                  ('MAIN ELECTRIC METER.Analog Inputs.KVA_Total.Main-kVA (Trend1)',
                   False),
                  ('MAIN ELECTRIC METER.Analog Inputs.KVAh.Main-kVAh (Trend1)',
                   True),
                  ('MAIN ELECTRIC METER.Analog Inputs.KW_A.Trend - Present Value (Trend1)',
                   False),
                  ('MAIN ELECTRIC METER.Analog Inputs.KW_B.Trend - Present Value (Trend1)',
                   False),
                  ('MAIN ELECTRIC METER.Analog Inputs.KW_C.Trend - Present Value (Trend1)',
                   False),
                  ('MAIN ELECTRIC METER.Analog Inputs.KW_Present_Demand.Main-kW_Present_Demand (Trend1)',
                   False),
                  ('MAIN ELECTRIC METER.Analog Inputs.KW_Total.Main-kW (Trend1)',
                   False),
                  ('PANEL COLLINS ELECTRIC METER.Analog Inputs.Energy.CollinCtr-Energy-kWh (Trend1)',
                   True),
                  ('PANEL COLLINS ELECTRIC METER.Analog Inputs.KVAR_Total.CollinCtr-kVAR (Trend1)',
                   False),
                  ('PANEL COLLINS ELECTRIC METER.Analog Inputs.KVARh.CollinCtr-kVARh (Trend1)',
                   True),
                  ('PANEL COLLINS ELECTRIC METER.Analog Inputs.KVA_Total.CollinCtr-kVA (Trend1)',
                   False),
                  ('PANEL COLLINS ELECTRIC METER.Analog Inputs.KVAh.CollinCtr-kVAh (Trend1)',
                   True),
                  ('PANEL COLLINS ELECTRIC METER.Analog Inputs.KW_Total.CollinCtr-kW (Trend1)',
                   False),
                  ('PANEL DE-ATS ELECTRIC METER.Analog Inputs.Energy.DE-ATS-Energy-kWh (Trend1)',
                   True),
                  ('PANEL DE-ATS ELECTRIC METER.Analog Inputs.KVAR_Total.DE-ATS-kVAR (Trend1)',
                   False),
                  ('PANEL DE-ATS ELECTRIC METER.Analog Inputs.KVARh.DE-ATS-kVARh (Trend1)',
                   True),
                  ('PANEL DE-ATS ELECTRIC METER.Analog Inputs.KVA_Total.DE-ATS-kVA (Trend1)',
                   False),
                  ('PANEL DE-ATS ELECTRIC METER.Analog Inputs.KVAh.DE-ATS-kVAh (Trend1)',
                   True),
                  ('PANEL DE-ATS ELECTRIC METER.Analog Inputs.KW_Total.DE-ATS-kW (Trend1)',
                   False),
                  ('PANEL DG ELECTRIC METER.Analog Inputs.Energy.DG-kWh-Energy (Trend1)',
                   True),
                  ('PANEL DG ELECTRIC METER.Analog Inputs.KVAR_Total.DG-kVAR (Trend1)',
                   False),
                  ('PANEL DG ELECTRIC METER.Analog Inputs.KVARh.DG-kVARh (Trend1)',
                   True),
                  ('PANEL DG ELECTRIC METER.Analog Inputs.KVA_Total.DG-kVA (Trend1)',
                   False),
                  ('PANEL DG ELECTRIC METER.Analog Inputs.KVAh.DG-kVAh (Trend1)',
                   True),
                  ('PANEL DG ELECTRIC METER.Analog Inputs.KW_Total.DG-kW (Trend1)',
                   False),
                  ('PANEL DHB ELECTRIC METER.Analog Inputs.Energy.DHB - kWh Total (Trend1)',
                   True),
                  ('PANEL DHB ELECTRIC METER.Analog Inputs.KVAR_Total.DHB-KVAR (Trend1)',
                   False),
                  ('PANEL DHB ELECTRIC METER.Analog Inputs.KVA_Total.DHB-KVA (Trend1)',
                   False),
                  ('PANEL DHB ELECTRIC METER.Analog Inputs.KVAh.DHB-kVAh (Trend1)',
                   True),
                  ('PANEL DHB ELECTRIC METER.Analog Inputs.KW_Total.DHB - kW - Present Value (Trend1)',
                   False),
                  ('PANEL DL ELECTRIC METER.Analog Inputs.Energy.DL-Energy-kWh (Trend1)',
                   True),
                  ('PANEL DL ELECTRIC METER.Analog Inputs.KVAR_Total.DL-kVAR (Trend1)',
                   False),
                  ('PANEL DL ELECTRIC METER.Analog Inputs.KVARh.DL-kVARh (Trend1)',
                   True),
                  ('PANEL DL ELECTRIC METER.Analog Inputs.KVA_Total.DL-kVA (Trend1)',
                   False),
                  ('PANEL DL ELECTRIC METER.Analog Inputs.KVAh.DL-kVAh (Trend1)',
                   True),
                  ('PANEL DL ELECTRIC METER.Analog Inputs.KW_Total.DL-kW (Trend1)',
                   False),
                  ('PANEL M1 ELECTRIC METER.Analog Inputs.Energy.M1-kWh-Energy (Trend1)',
                   True),
                  ('PANEL M1 ELECTRIC METER.Analog Inputs.KVAR_Total.M1-kVAR-Total (Trend1)',
                   False),
                  ('PANEL M1 ELECTRIC METER.Analog Inputs.KVARh.M1-kVARh (Trend1)',
                   True),
                  ('PANEL M1 ELECTRIC METER.Analog Inputs.KVA_Total.M1-kVA-Total (Trend1)',
                   False),
                  ('PANEL M1 ELECTRIC METER.Analog Inputs.KVAh.M1-kVAh (Trend1)',
                   True),
                  ('PANEL M1 ELECTRIC METER.Analog Inputs.KW_Total.M1-kW-Total (Trend1)',
                   False),
                  ])
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
    if form_data['graph']:
        _transform_saved_input_graph(form_data['graph_data'],
                                     form_data['graph_period'],
                                     field_type[form_data['graph_data']],
                                     )

    return _respond_with_parsed_file(form_data['graph'])

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

def _respond_with_parsed_file(ziprtn):
    if ziprtn:
        files= [_temporary_output_file_path(), _temporary_output_graph_path()]

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
