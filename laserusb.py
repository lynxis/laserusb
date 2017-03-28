import usb.core
from usb.util import endpoint_address, endpoint_direction, ENDPOINT_IN, ENDPOINT_OUT
import struct

# wait time out for aiting the device to respond for an allocation request
# in ms
ALLOC_TIMEOUT = 100

class LaserUSB(object):
    def __init__(self):
        self.dev = None
        self.connected = False

        # [input, output]
        self.interupt = [None, None]
        self.bulk = [None, None]

    # the laser has 3 endpoints
    # - 0 command
    # - 1 interupt
    # - 2 bulk
    def connect(self):
        dev = usb.core.find(idVendor=0x0471, idProduct=0x0999)
        if dev is None:
            raise ValueError('Device not found')

        dev.set_configuration()
        self.dev = dev
        cfg = dev.get_active_configuration()
        intf = cfg[(0,0)]

        for ep in intf:
            if endpoint_address(ep.bEndpointAddress) == 0x1:
                if endpoint_direction(ep.bEndpointAddress) == ENDPOINT_IN:
                    self.interupt[0] = ep
                else:
                    self.interupt[1] = ep

            if endpoint_address(ep.bEndpointAddress) == 0x2:
                if endpoint_direction(ep.bEndpointAddress) == ENDPOINT_IN:
                    self.bulk[0] = ep
                else:
                    self.bulk[1] = ep

        if None in self.interupt:
            raise RuntimeError("Could not find interupt endpoint")
        if None in self.bulk:
            raise RuntimeError("Could not find bulk endpoint")
        self.connected = True

    # when sending data, send the length data (16bit) over interupt line
    def write(self, data):
        if len(data) >= 2**16:
            raise RuntimeError("Laserdata to big. max 16 bit")

        # big endian 16 bit as length
        inter_data = struct.pack('>h', len(data))
        if self.interupt[1].write(inter_data) != 2:
            raise RuntimeError("Could not send interupt data")
        # now wait for interupt data
        inter_data = self.interupt[0].read(1, ALLOC_TIMEOUT)
        if inter_data[0] != 0x1:
            raise RuntimeError("Did not receive confirmation for sending HPGL data")

        self.bulk[1].write(data)

class LaserControl(LaserUSB):
    cmd_stepping = "ZZZFile0;VP100;VK100;SP2;SP2;VQ15;VJ24;VS10;PR;PU%d,%d;ZED;"
    cmd_stop = "ZZZFile0;ZQ;ZED"
    def _ensure_connected(self):
        if not self.connected:
            self.connect()

    def up(self, steps=80):
        self._ensure_connected()
        self.write(self.cmd_stepping % (0, -steps))

    def down(self, steps=80):
        self._ensure_connected()
        self.write(self.cmd_stepping % (0, steps))

    def left(self, steps=80):
        self._ensure_connected()
        self.write(self.cmd_stepping % (-steps, 0))

    def right(self, steps=80):
        self._ensure_connected()
        self.write(self.cmd_stepping % (steps, 0))

    def stop(self):
        self._ensure_connected()
        self.write(self.cmd_stop)
