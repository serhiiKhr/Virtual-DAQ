import tkinter as tk
import configparser
from tkinter import filedialog
import numpy as np
import os
import math

from utils.helpers import deep_get

class MeraReader:
    def __init__(self, filepath: str = ''):
        self.filepath = filepath
        self.data = None
        
    def data_generator(self, chunk_size: int, start_index: int = 0):
        channels = self.get_channels()
        if self.data is None:
            self.data = {}
            for ch in channels:
                sampling_rate = self.get_sampling_rate(ch_name=ch)
                data = self.read_channel(channel=ch)
                duration = len(data) / sampling_rate
                self.data[ch] = data
            
        
        total_length = len(next(iter(self.data.values())))

        if start_index >= total_length:
            return

        for i in range(start_index, total_length, chunk_size):
            yield {
                key: values[i:i + chunk_size]
                for key, values in self.data.items()
            }
        
    def get_duration(self):
        channels = self.get_channels()
        duration = self.get_signal_length(channel=channels[0]) 
        return duration
        
    def get_sampling_rate(self, ch_name: str = ''):
        if not ch_name:
            ch_name = self.get_channels()[0]
        meta = self.get_file_meta()
        return float(deep_get(meta, [ch_name, 'freq'], 0))
    
    def get_file_meta(self):
        if not self.filepath:
            return None
       
        config = configparser.ConfigParser(strict=False)
        config.read(self.filepath, encoding='windows-1251')
        return {section: dict(config[section]) for section in config.sections()}
    
    def get_channels(self):
        meta = self.get_file_meta()
        
        return [name for name in meta.keys() if name.lower() != 'mera']

    
    def read_channel(self, channel):
        # global mera_path, parameters
        
        if not self.filepath:
            return None
        
        if self.data is None or channel not in self.data.keys():
            meta = self.get_file_meta()
            y_format = meta.get("YFormat", "I2")
            freq = deep_get(meta, [channel, 'freq'], 0)
            step = float(meta.get("Step", 1.0))

            k0 = float(meta.get("k0", 0))
            k1 = float(meta.get("k1", 1))
            polyTX = int(meta.get("PolyTX", 0))

            dtype_map = {
                "I1": np.int8, "UI1": np.uint8,
                "I2": np.int16, "UI2": np.uint16,
                "I4": np.int32, "I8": np.int64,
                "R4": np.float32, "R8": np.float64
            }
            dat_path = os.path.join(os.path.dirname(self.filepath), channel + ".dat")
            dtype = dtype_map.get(y_format.upper(), np.int16)
            data = np.fromfile(dat_path, dtype=dtype)
            
            if polyTX == 0:
                data = k1 * (data - k0)
            else:
                data = k1 * data + k0
        
            return data
        else:
            return self.data[channel]
    
    def get_signal_length(self, channel: str):
        if not channel:
            return None
        
        sampling_rate = self.get_sampling_rate(ch_name=channel)
              
        data = self.read_channel(channel=channel)
        length = len(data) / sampling_rate 
        return length
    
    def _init_data(self):
        channels = self.get_channels()
        if self.data is None:
            self.data = {}
            for ch in channels:
                sampling_rate = self.get_sampling_rate(ch_name=ch)
                data = self.read_channel(channel=ch)
                duration = len(data) / sampling_rate
                self.data[ch] = data