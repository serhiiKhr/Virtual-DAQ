from tkinter import filedialog
import dwdatareader as dw
dw.encoding = 'utf-8'

class DWReader:
    def __init__(self, filepath: str):
        self.filepath = filepath
        
    def data_generator(self, chunk_size: int, start_index: int = 0):
        reader = dw.open(self.filepath)
        chunks = {}
        signal_length = reader.info.duration * reader.info.sample_rate
        # 1869401
        # channel_names = self.get_channels()
        generators = {
            channel.name: channel.series_generator(chunk_size)
            for channel in reader.channels
            if channel.number_of_samples > 0 and channel.number_of_samples == signal_length
        }
        for _ in range(start_index):
            for gen in generators.values():
                next(gen)
                
        while True:
            chunks = {}
            for name, gen in generators.items():
                try:
                    series = next(gen)
                    chunks[name] = series.values
                except StopIteration:
                    return None
            yield chunks
            
    def get_duration(self):
        reader = dw.open(self.filepath)
        return reader.info.duration 
                    
    def get_sampling_rate(self):
         with dw.open(self.filepath) as f:
            return f.info.sample_rate
        
    def get_channels(self):
        with dw.open(self.filepath) as f:
            return [ch.name for ch in f.channels]
        
    def read_channel(self, channel: str = ''):
        with dw.open(self.filepath) as f:
            for ch in f.channels:
                if channel == ch.name:
                    dataframe = ch.dataframe()
                    return dataframe[channel]
                
        return None

    def get_signal_length(self, channel: str = ''):
        with dw.open(self.filepath) as f:
            for ch in f.channels:
                if channel == ch.name:
                    number_of_samples = ch.number_of_samples
                    sampling_rate = self.get_sampling_rate(channel==channel)
                    length = number_of_samples / sampling_rate
                    return length
                
        return None