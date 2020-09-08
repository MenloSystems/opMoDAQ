# Windows DAQ device interface

import opmodaq.device as dev
import opmodaq.parameters as params
import opmodaq.generators as gen

import matplotlib.pyplot as plt


class PlotDeviceChannel(dev.Channel):

    def __init__(self, device, channel_idx):
        dev.Channel.__init__(self, device, channel_idx)
      
    def analog_out(self,
                   generator:    gen.SignalGenerator,
                   sample_range: range):
        x_values = []
        for x in sample_range:
            x_values.append(x)

        y_values = []
        for y in generator.samples(self.device.sampling, sample_range):
            y_values.append(y)
        
        self.device.plot_obj.plot(x_values, y_values)
    


class PlotDevice(dev.Device):
  
    def __init__(self, sampling: params.Sampling, plot_obj = plt):
        self.plot_obj = plot_obj
        self.sampling = sampling
        dev.Device.__init__(self, board_num = 0, dev_handle = plot_obj)
    
    def channel(self, channel_idx):
        return PlotDeviceChannel(self, channel_idx)

