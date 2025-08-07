import subprocess
import serial
import struct
from serial.tools import list_ports
import time

class ComPortSender:
    def __init__(self, to_port: str):
        print('ComPortSender')
        self.to_port = to_port
        self._serial = None
        self._init_serial()
        
    def send(self, data):
        channel_count = len(data.keys())
        values = list(data.values())
        payload = b''
        resord_count = len(values[0])
        
        for value in values:
            payload += struct.pack(f'<{len(value)}f', *value)
            
        payload_size = len(payload)
        
        header = struct.pack('<2sHBB', b'\xAA\x55', payload_size, channel_count, resord_count)
        packet = header + payload
        
        self._serial.write(packet)
        self._serial.flush()
    
    def close(self):
        self._serial.close()
    
    
    def _init_serial(self):
        self._serial = serial.Serial(port=self.to_port, baudrate=230400, timeout=1)