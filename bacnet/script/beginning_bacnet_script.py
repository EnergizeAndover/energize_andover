from bacpypes.comm import Client, Server, bind, Debug, PDU, PCI
from bacpypes.pdu import *
from bacpypes.consolecmd import ConsoleCmd
from bacpypes.iocb import IOCB, IOController
from bacpypes.capability import Capability, Collector
import bacpypes
import sys

class MyServer(Server):
     def indication(self, arg):
         print ("working on", arg)
         self.response(arg.upper())

class MyClient(Client):
    def confirmation(self, pdu):
        print ("thanks for the", pdu)

class SomeController(IOController):
    def process_io(self,iocb):
        self.complete_io(iocb, iocb.args[0] + iocb.args[1] * iocb.kwargs['a'])

class BaseCollector(Collector):
    def transform(self, value):
        for fn in self.capability_functions('transform'):
            value = fn(self, value)
        return value

class PlusOne (Capability):
    def transform(self, value):
        return value + 1

class ExampleOne(BaseCollector, PlusOne): # more than 1 class can be added, order matters
    pass

s = MyServer()
c= MyClient()
d = Debug("middle")

bind (c,d,s)

#c.request("hi")

#pdu = PDU(b"hello!!")
#print(pdu.get())
#pdu.debug_contents()
#print(pdu.get_short())
#pdu.debug_contents()
#print(pdu.get_long())
#pdu.debug_contents()
#pdu.put(108)
#pdu.debug_contents()
#pdu.put_short(25964)
#pdu.debug_contents()
#pdu.put_long(1819222305)
#pdu.debug_contents()

addr1 = Address(b'123456')
#print(addr1)
addr2 = Address(12)
#print (addr2)
#print(addr1.addrAddr)
LocalStation(b'/1/2/3/4/xba/xc0')
LocalStation(b'/1/2/3/4/xba/xc3')
#print(LocalBroadcast())
#print(RemoteStation(15,b'123456'))
#print (RemoteBroadcast(17))
#print(GlobalBroadcast())
#print(Address(1).addrType==Address.localStationAddr)
#print(Address(1) == LocalStation(b'\01'))
#print(Address(2) == LocalStation(b'\02'))
#print(Address("0x0304") == LocalStation(b'\3\4'))
#print(Address("*")==LocalBroadcast())
#print(Address("1:2") == RemoteStation(1, 2))
#print(Address("3:*") == RemoteBroadcast(3))
#print(Address("*:*") == GlobalBroadcast())
#print(Address("192.168.1.2").addrAddr)
#print(Address("192.168.1.2:47809").addrAddr)
#print(hex(Address("192.168.3.4/24").addrSubnet))
#print(Address("192.168.5.6/16").addrBroadcastTuple)
if '==console' in sys.argv:
    ConsoleCmd()
iocb = IOCB(1,2, a=3)
#print(iocb.args)
#print(iocb.kwargs)

some_controller = SomeController()
some_controller.request_io(iocb)
#print(iocb.ioComplete)
#print(iocb.ioComplete.is_set())
#print(iocb.ioState == bacpypes.iocb.COMPLETED/ABORTED)
#print(iocb.ioResponse)
iocb = IOCB(1,2)
some_controller.request_io(iocb)
#print (iocb.ioError)

def call_me(iocb):
    print("call me, %r or %r" %(iocb.ioResponse, iocb.ioError))

iocb= IOCB(1, 2, a=10)
#iocb.add_callback(call_me)
#print(some_controller.request_io(iocb))
some_controller.request_io(iocb)
iocb.ioComplete.wait()
some_transformer = BaseCollector()
print(some_transformer.transform(10))

some_transformer = ExampleOne()
print(some_transformer.transform(10))

