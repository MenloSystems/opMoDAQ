

class Source:
    name: str

class Sampling:
    def __init__(self,
                 frequency:    int,
                 sample_range: set = { 0, 255 }):
        self.frequency:    int  = frequency
        self.sample_range: set  = sample_range
        self.sample_size:  int  = max(sample_range) - min(sample_range)

class Signal:
    def __init__(self,
                 signal_range: set = { -1.0, +1.0 },
                 offset:       float = 0.0):
        self.signal_range: range  = signal_range
        self.offset:       float  = offset
        self.min:          float  = min(signal_range)
        self.max:          float  = max(signal_range)
        self.amplitude:    float  = self.max - self.min
        self.baseline:     float  = offset + self.amplitude / 2

