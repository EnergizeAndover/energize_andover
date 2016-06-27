from django import forms

class MetasysUploadForm(forms.Form):
    summarize = forms.BooleanField(
        label='Group by day',
        required=False
    )

    cost = forms.FloatField(
        label='Estimated cost of electricity ($/kWh)',
        required=False
    )

    start_time = forms.TimeField(
        label='Start time (HH:MM)',
        input_formats=['%H:%M'],
        required=False
    )

    end_time = forms.TimeField(
        label='End time (HH:MM)',
        input_formats=['%H:%M'],
        required=False
    )

    metasys_file = forms.FileField(
        label='Select a file'
    )

class GraphUploadForm(forms.Form):
    parsed_file = forms.FileField(
        label='Select a Metasys file'

    )

    #graph_period = forms.ChoiceField(
    #    label='time interval:',
    #    choices=[(None, 'all data'),
    #             ('hour', 'hour'),
    #             ('day', 'day'),
    #             ('month', 'month'),
    #             ]
    #)

    graph_data = forms.ChoiceField(
        label='data to graph:',
        choices=[('MAIN ELECTRIC METER.Analog Inputs.Energy.Main-kWh-Energy (Trend1)',
                  'MAIN ELECTRIC METER.Analog Inputs.Energy.Main-kWh-Energy (Trend1)'),
                 ('MAIN ELECTRIC METER.Analog Inputs.KVAR_Present_Demand.Main-kVAR_Present_Demand (Trend1)',
                  'MAIN ELECTRIC METER.Analog Inputs.KVAR_Present_Demand.Main-kVAR_Present_Demand (Trend1)'),
                 ('MAIN ELECTRIC METER.Analog Inputs.KVAR_Total.Main-kVAR (Trend1)',
                  'MAIN ELECTRIC METER.Analog Inputs.KVAR_Total.Main-kVAR (Trend1)'),
                 ('MAIN ELECTRIC METER.Analog Inputs.KVARh.Main-kVARh (Trend1)',
                  'MAIN ELECTRIC METER.Analog Inputs.KVARh.Main-kVARh (Trend1)'),
                 ('MAIN ELECTRIC METER.Analog Inputs.KVA_Present_Demand.Main-kVA_Present_Demand (Trend1)',
                  'MAIN ELECTRIC METER.Analog Inputs.KVA_Present_Demand.Main-kVA_Present_Demand (Trend1)'),
                 ('MAIN ELECTRIC METER.Analog Inputs.KVA_Total.Main-kVA (Trend1)',
                  'MAIN ELECTRIC METER.Analog Inputs.KVA_Total.Main-kVA (Trend1)'),
                 ('MAIN ELECTRIC METER.Analog Inputs.KVAh.Main-kVAh (Trend1)',
                  'MAIN ELECTRIC METER.Analog Inputs.KVAh.Main-kVAh (Trend1)'),
                 ('MAIN ELECTRIC METER.Analog Inputs.KW_A.Trend - Present Value (Trend1)',
                  'MAIN ELECTRIC METER.Analog Inputs.KW_A.Trend - Present Value (Trend1)'),
                 ('MAIN ELECTRIC METER.Analog Inputs.KW_B.Trend - Present Value (Trend1)',
                  'MAIN ELECTRIC METER.Analog Inputs.KW_B.Trend - Present Value (Trend1)'),
                 ('MAIN ELECTRIC METER.Analog Inputs.KW_C.Trend - Present Value (Trend1)',
                  'MAIN ELECTRIC METER.Analog Inputs.KW_C.Trend - Present Value (Trend1)'),
                 ('MAIN ELECTRIC METER.Analog Inputs.KW_Present_Demand.Main-kW_Present_Demand (Trend1)',
                  'MAIN ELECTRIC METER.Analog Inputs.KW_Present_Demand.Main-kW_Present_Demand (Trend1)'),
                 ('MAIN ELECTRIC METER.Analog Inputs.KW_Total.Main-kW (Trend1)',
                  'MAIN ELECTRIC METER.Analog Inputs.KW_Total.Main-kW (Trend1)'),
                 ('PANEL COLLINS ELECTRIC METER.Analog Inputs.Energy.CollinCtr-Energy-kWh (Trend1)',
                  'PANEL COLLINS ELECTRIC METER.Analog Inputs.Energy.CollinCtr-Energy-kWh (Trend1)'),
                 ('PANEL COLLINS ELECTRIC METER.Analog Inputs.KVAR_Total.CollinCtr-kVAR (Trend1)',
                  'PANEL COLLINS ELECTRIC METER.Analog Inputs.KVAR_Total.CollinCtr-kVAR (Trend1)'),
                 ('PANEL COLLINS ELECTRIC METER.Analog Inputs.KVARh.CollinCtr-kVARh (Trend1)',
                  'PANEL COLLINS ELECTRIC METER.Analog Inputs.KVARh.CollinCtr-kVARh (Trend1)'),
                 ('PANEL COLLINS ELECTRIC METER.Analog Inputs.KVA_Total.CollinCtr-kVA (Trend1)',
                  'PANEL COLLINS ELECTRIC METER.Analog Inputs.KVA_Total.CollinCtr-kVA (Trend1)'),
                 ('PANEL COLLINS ELECTRIC METER.Analog Inputs.KVAh.CollinCtr-kVAh (Trend1)',
                  'PANEL COLLINS ELECTRIC METER.Analog Inputs.KVAh.CollinCtr-kVAh (Trend1)'),
                 ('PANEL COLLINS ELECTRIC METER.Analog Inputs.KW_Total.CollinCtr-kW (Trend1)',
                  'PANEL COLLINS ELECTRIC METER.Analog Inputs.KW_Total.CollinCtr-kW (Trend1)'),
                 ('PANEL DE-ATS ELECTRIC METER.Analog Inputs.Energy.DE-ATS-Energy-kWh (Trend1)',
                  'PANEL DE-ATS ELECTRIC METER.Analog Inputs.Energy.DE-ATS-Energy-kWh (Trend1)'),
                 ('PANEL DE-ATS ELECTRIC METER.Analog Inputs.KVAR_Total.DE-ATS-kVAR (Trend1)',
                  'PANEL DE-ATS ELECTRIC METER.Analog Inputs.KVAR_Total.DE-ATS-kVAR (Trend1)'),
                 ('PANEL DE-ATS ELECTRIC METER.Analog Inputs.KVARh.DE-ATS-kVARh (Trend1)',
                  'PANEL DE-ATS ELECTRIC METER.Analog Inputs.KVARh.DE-ATS-kVARh (Trend1)'),
                 ('PANEL DE-ATS ELECTRIC METER.Analog Inputs.KVA_Total.DE-ATS-kVA (Trend1)',
                  'PANEL DE-ATS ELECTRIC METER.Analog Inputs.KVA_Total.DE-ATS-kVA (Trend1)'),
                 ('PANEL DE-ATS ELECTRIC METER.Analog Inputs.KVAh.DE-ATS-kVAh (Trend1)',
                  'PANEL DE-ATS ELECTRIC METER.Analog Inputs.KVAh.DE-ATS-kVAh (Trend1)'),
                 ('PANEL DE-ATS ELECTRIC METER.Analog Inputs.KW_Total.DE-ATS-kW (Trend1)',
                  'PANEL DE-ATS ELECTRIC METER.Analog Inputs.KW_Total.DE-ATS-kW (Trend1)'),
                 ('PANEL DG ELECTRIC METER.Analog Inputs.Energy.DG-kWh-Energy (Trend1)',
                  'PANEL DG ELECTRIC METER.Analog Inputs.Energy.DG-kWh-Energy (Trend1)'),
                 ('PANEL DG ELECTRIC METER.Analog Inputs.KVAR_Total.DG-kVAR (Trend1)',
                  'PANEL DG ELECTRIC METER.Analog Inputs.KVAR_Total.DG-kVAR (Trend1)'),
                 ('PANEL DG ELECTRIC METER.Analog Inputs.KVARh.DG-kVARh (Trend1)',
                  'PANEL DG ELECTRIC METER.Analog Inputs.KVARh.DG-kVARh (Trend1)'),
                 ('PANEL DG ELECTRIC METER.Analog Inputs.KVA_Total.DG-kVA (Trend1)',
                  'PANEL DG ELECTRIC METER.Analog Inputs.KVA_Total.DG-kVA (Trend1)'),
                 ('PANEL DG ELECTRIC METER.Analog Inputs.KVAh.DG-kVAh (Trend1)',
                  'PANEL DG ELECTRIC METER.Analog Inputs.KVAh.DG-kVAh (Trend1)'),
                 ('PANEL DG ELECTRIC METER.Analog Inputs.KW_Total.DG-kW (Trend1)',
                  'PANEL DG ELECTRIC METER.Analog Inputs.KW_Total.DG-kW (Trend1)'),
                 ('PANEL DHB ELECTRIC METER.Analog Inputs.Energy.DHB - kWh Total (Trend1)',
                  'PANEL DHB ELECTRIC METER.Analog Inputs.Energy.DHB - kWh Total (Trend1)'),
                 ('PANEL DHB ELECTRIC METER.Analog Inputs.KVAR_Total.DHB-KVAR (Trend1)',
                  'PANEL DHB ELECTRIC METER.Analog Inputs.KVAR_Total.DHB-KVAR (Trend1)'),
                 ('PANEL DHB ELECTRIC METER.Analog Inputs.KVA_Total.DHB-KVA (Trend1)',
                  'PANEL DHB ELECTRIC METER.Analog Inputs.KVA_Total.DHB-KVA (Trend1)'),
                 ('PANEL DHB ELECTRIC METER.Analog Inputs.KVAh.DHB-kVAh (Trend1)',
                  'PANEL DHB ELECTRIC METER.Analog Inputs.KVAh.DHB-kVAh (Trend1)'),
                 ('PANEL DHB ELECTRIC METER.Analog Inputs.KW_Total.DHB - kW - Present Value (Trend1)',
                  'PANEL DHB ELECTRIC METER.Analog Inputs.KW_Total.DHB - kW - Present Value (Trend1)'),
                 ('PANEL DL ELECTRIC METER.Analog Inputs.Energy.DL-Energy-kWh (Trend1)',
                  'PANEL DL ELECTRIC METER.Analog Inputs.Energy.DL-Energy-kWh (Trend1)'),
                 ('PANEL DL ELECTRIC METER.Analog Inputs.KVAR_Total.DL-kVAR (Trend1)',
                  'PANEL DL ELECTRIC METER.Analog Inputs.KVAR_Total.DL-kVAR (Trend1)'),
                 ('PANEL DL ELECTRIC METER.Analog Inputs.KVARh.DL-kVARh (Trend1)',
                  'PANEL DL ELECTRIC METER.Analog Inputs.KVARh.DL-kVARh (Trend1)'),
                 ('PANEL DL ELECTRIC METER.Analog Inputs.KVA_Total.DL-kVA (Trend1)',
                  'PANEL DL ELECTRIC METER.Analog Inputs.KVA_Total.DL-kVA (Trend1)'),
                 ('PANEL DL ELECTRIC METER.Analog Inputs.KVAh.DL-kVAh (Trend1)',
                  'PANEL DL ELECTRIC METER.Analog Inputs.KVAh.DL-kVAh (Trend1)'),
                 ('PANEL DL ELECTRIC METER.Analog Inputs.KW_Total.DL-kW (Trend1)',
                  'PANEL DL ELECTRIC METER.Analog Inputs.KW_Total.DL-kW (Trend1)'),
                 ('PANEL M1 ELECTRIC METER.Analog Inputs.Energy.M1-kWh-Energy (Trend1)',
                  'PANEL M1 ELECTRIC METER.Analog Inputs.Energy.M1-kWh-Energy (Trend1)'),
                 ('PANEL M1 ELECTRIC METER.Analog Inputs.KVAR_Total.M1-kVAR-Total (Trend1)',
                  'PANEL M1 ELECTRIC METER.Analog Inputs.KVAR_Total.M1-kVAR-Total (Trend1)'),
                 ('PANEL M1 ELECTRIC METER.Analog Inputs.KVARh.M1-kVARh (Trend1)',
                  'PANEL M1 ELECTRIC METER.Analog Inputs.KVARh.M1-kVARh (Trend1)'),
                 ('PANEL M1 ELECTRIC METER.Analog Inputs.KVA_Total.M1-kVA-Total (Trend1)',
                  'PANEL M1 ELECTRIC METER.Analog Inputs.KVA_Total.M1-kVA-Total (Trend1)'),
                 ('PANEL M1 ELECTRIC METER.Analog Inputs.KVAh.M1-kVAh (Trend1)',
                  'PANEL M1 ELECTRIC METER.Analog Inputs.KVAh.M1-kVAh (Trend1)'),
                 ('PANEL M1 ELECTRIC METER.Analog Inputs.KW_Total.M1-kW-Total (Trend1)',
                  'PANEL M1 ELECTRIC METER.Analog Inputs.KW_Total.M1-kW-Total (Trend1)')
                 ]
    )
