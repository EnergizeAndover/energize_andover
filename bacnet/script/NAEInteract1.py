from bacpypes.service.device import LocalDeviceObject
from bacpypes.basetypes import ServicesSupported
from bacpypes.app import BIPSimpleApplication
from bacpypes.iocb import IOCB
from bacpypes.apdu import WhoIsRequest, IAmRequest, ReadPropertyRequest
from bacpypes.errors import DecodingError
import sys
from bacpypes.debugging import  ModuleLogger
from bacpypes.consolelogging import ConfigArgumentParser
from bacpypes.core import run, stop
from bacpypes.pdu import Address
from bacpypes.object import get_datatype
from datetime import datetime

import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
sys.path.insert(0, "/var/www/gismap/")
#print (sys.path)
django.setup()
from bacnet.models import *

_debug=1
_log = ModuleLogger(globals())

object_identifier = None
object_destination = None
this_application = None
value = None
class GetNAEInfoApplication(BIPSimpleApplication):
    def __init__(self, device, address):
        BIPSimpleApplication.__init__(self, device, address)
        self._request=None
        iocb = IOCB(time=5)

    def request(self, apdu):
        print(apdu)
        self._request=apdu
        BIPSimpleApplication.request(self, apdu)

    def confirmation(self, apdu):
        global value
        datatype = get_datatype(apdu.objectIdentifier[0], apdu.propertyIdentifier)
        value=apdu.propertyValue.cast_out(datatype)
        BIPSimpleApplication.confirmation(self, apdu)
        stop()

    def indication(self, apdu):
        global object_identifier
        global object_destination
        if (isinstance(self._request, WhoIsRequest)) and (isinstance(apdu, IAmRequest)):
            device_type, device_instance = apdu.iAmDeviceIdentifier
            if device_type != 'device':
                raise DecodingError("invalid object type")
            if (self._request.deviceInstanceRangeLowLimit is not None) and \
                (device_instance < self._request.deviceInstanceRangeLowLimit):
                pass
            elif (self._request.deviceInstanceRangeHighLimit is not None) and \
                (device_instance > self._request.deviceInstanceRangeHighLimit):
                pass
            else:
                object_identifier=apdu.iAmDeviceIdentifier
                object_destination = apdu.pduSource
                sys.stdout.write('pduSource = ' + repr(apdu.pduSource) + '\n')
                sys.stdout.write('iAmDeviceIdentifier = ' + str(apdu.iAmDeviceIdentifier) + '\n')
                sys.stdout.write('maxAPDULengthAccepted = ' + str(apdu.maxAPDULengthAccepted) + '\n')
                sys.stdout.write('segmentationSupported = ' + str(apdu.segmentationSupported) + '\n')
                sys.stdout.write('vendorID = ' + str(apdu.vendorID) + '\n')
                if _debug: GetNAEInfoApplication._debug("__init__ %r", apdu)
                sys.stdout.flush()

        BIPSimpleApplication.indication(self, apdu)
        stop()
def findNAE():
    global object_identifier
    global object_destination
    global this_application
    args = ConfigArgumentParser(description=__doc__).parse_args()
    this_device = LocalDeviceObject(objectName=args.ini.objectname,
                                    objectIdentifier=int(args.ini.objectidentifier),
                                    maxApduLengthAccepted=int(args.ini.maxapdulengthaccepted),
                                    segmentationSupported=args.ini.segmentationsupported,
                                    vendorIdentifier=int(args.ini.vendoridentifier))

    this_application = GetNAEInfoApplication(this_device, args.ini.address)
    pss = ServicesSupported()
    pss['whoIs'] = 1
    pss['iAm'] = 1
    pss['readProperty'] = 1
    pss['writeProperty'] = 1
    this_device.protocolServicesSupported = pss
    services_supported = this_application.get_services_supported()
    this_device.protocolServicesSupported = services_supported.value
    this_application.who_is(None, None, Address(b'\x0A\x0C\x00\xFA\xba\xc0'))

    run()


count = 0
def write(name, value, school):
    global count
    global csv
    csv = open('trend.csv', 'a')
    csv.write(str(count) + "," + str(datetime.now()) + "," + name + "," + str(value) + "," + school + ",\n")
    csv.close()
    count += 1

def analog_value_request(identifier, name, school):
    global object_destination
    global value
    new_request = ReadPropertyRequest(objectIdentifier=("analogInput", identifier), propertyIdentifier="presentValue")
    new_request.pduDestination = object_destination
    this_application.request(new_request)
    run()
    dv = Data_Point(Value=value, Time = str(datetime.now()), Name = name, School = School.objects.get(Name=school))
    dv.save()
    write(name, value, school)

def close():
    global csv
    csv.close()

def main():
    analog_value_request(3007360, "Main (kW)", "Andover High School")
    analog_value_request(3017359, "DHB (kW)", "Andover High School")
    analog_value_request(3017523, "DG (kW)", "Andover High School")
    analog_value_request(3017605, "DE (kW)", "Andover High School")
    analog_value_request(3017769, "DL (kW)", "Andover High School")
    analog_value_request(3017441, "M1 (kW)", "Andover High School")
    analog_value_request(3017687, "AMDP (kW)", "Andover High School")
    analog_value_request(3007361, "Main (kWh)", "Andover High School")
    analog_value_request(3017360, "DHB (kWh)", "Andover High School")
    analog_value_request(3017524, "DG (kWh)", "Andover High School")
    analog_value_request(3017606, "DE (kWh)", "Andover High School")
    analog_value_request(3017770, "DL (kWh)", "Andover High School")
    analog_value_request(3017442, "M1 (kWh)", "Andover High School")
    analog_value_request(3017688, "AMDP (kWh)", "Andover High School")

