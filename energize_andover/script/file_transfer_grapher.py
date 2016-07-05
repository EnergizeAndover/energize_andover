from django.http import HttpResponse
from mysite.settings import BASE_DIR
from wsgiref.util import FileWrapper
from energize_andover.script.grapher import file_parser
#from energize_andover.energize_andover.script.grapher import file_parser
import os


TEMPORARY_INPUT_FILENAME = 'graph_log.csv'
OUTPUT_FILENAME = 'graph.pdf'
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

def get_transformed_graph(form_data):
    """Transforms and returns the Metasys log file attached to the form"""
    _save_input_graph(form_data['parsed_file'])
    _transform_saved_input_graph(form_data['graph_data'],
                                form_data['graph_period'],
                                field_type[form_data['graph_data']],
    )
    return _respond_with_parsed_file()

def _temporary_input_graph_path():
    return os.path.join(BASE_DIR, TEMPORARY_INPUT_FILENAME)

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
                                ):
    file_parser(_temporary_input_graph_path(),
                output_file_name=_temporary_output_graph_path(),
                field_to_graph=ftg,
                grouping=grouping,
                total=total,
                )



def _respond_with_parsed_file():
    graph = open(_temporary_output_graph_path(), 'rb')
    response = HttpResponse(FileWrapper(graph), content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="%s"' % OUTPUT_FILENAME
    return response