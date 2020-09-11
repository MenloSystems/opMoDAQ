# Windows DAQ device interface

import opmodaq.parameters as params
import opmodaq.device as dev
import opmodaq.generators as gen

from ctypes import cast, POINTER, c_ushort

from mcculw import ul, structs, enums
from mcculw.enums import ULRange, InterfaceType
from mcculw.device_info import DaqDeviceInfo
from mcculw.ul import ULError

class MCCDAQChannel(dev.Channel):

    def __init__(self, device, channel_idx):
        dev.Channel.__init__(self, device, channel_idx)
  
    def set_analog_out(self,
                       value: float):
        board_num = self.device.board_num
        ul_range  = self.device.ao_range
        convert   = lambda value: ul.from_eng_units(
                                    board_num       = board_num,
                                    ul_range        = ul_range,
                                    eng_units_value = value)
        ul.a_out(board_num  = board_num,
                 ul_range   = ul_range,
                 channel    = self.channel_idx,
                 data_value = convert(value))

    def analog_out(self,
                   generator:    gen.SignalGenerator,
                   sample_range: range):
        # Local variables to reduce dereferences in loop:
        board_num = self.device.board_num
        ul_range  = self.device.ao_range
        convert   = lambda value: ul.from_eng_units(
                                    board_num       = board_num,
                                    ul_range        = ul_range,
                                    eng_units_value = value)
        a_out     = ul.a_out
        
        for value in generator.samples(sample_range):
            a_out(board_num  = board_num,
                  ul_range   = ul_range,
                  channel    = self.channel_idx,
                  data_value = convert(value))
    


class MCCDAQ(dev.Device):
    __registered_board_nums = []
    __memhandles            = []
    
    def __init__(self,
                 board_num:  int,
                 dev_handle: ul.DaqDeviceDescriptor,
                 sampling:   params.Sampling):
        self.dev_info = DaqDeviceInfo(board_num)
        self.sampling = sampling
        self.ao_range = self.dev_info.get_ao_info().supported_ranges[0]
        self.channels = []
        self.num_ao_channels:    int = self.dev_info.get_ao_info().num_chans
        self.points_per_channel: int = 1024
        self.buffer_size             = self.num_ao_channels * self.points_per_channel

        dev.Device.__init__(self, self.board_num, self.dev_info)

        if MCCDAQ.__registered_board_nums.index(board_num) == -1:
            ul.ignore_instacal()
            ul.create_daq_device(board_num, dev_handle)
            MCCDAQ.__registered_board_nums.append(board_num)
            MCCDAQ.__memhandles.append(
              ul.win_buf_alloc(self.buffer_size))

        self.memhandle = MCCDAQ.__memhandles.index(self.board_num)
        if not self.memhandle:
            raise Exception('MCCDAQChannel: Failed to allocate memory')
        
        self.cdata = cast(self.memhandle, POINTER(c_ushort))
        
        for channel_idx in range(self.num_ao_channels):
          self.channels.append(MCCDAQChannel(self, channel_idx))

    def channel(self, channel_idx):
        return self.channels[channel_idx]

#   def analog_out(self, channel_generators: dict, sample_range: range):
#       channels    = channel_generators.keys
#       generators  = channel_generators.values
#       low_chan    = min(channels)
#       high_chan   = max(channels)
#       num_chans   = high_chan - low_chan + 1
#       num_samples = min(self.buffer_size,
#                         num_chans * len(sample_range))
#       # Generate D/A data:
#       data_index  = 0
#       for t in sample_range[:points_per_channel]:
#           for channel_idx in channels:
#               self.cdata[data_index] = generators[channel_idx]
#       
#       # Send data to D/A:
#       ul.a_out_scan(board_num  = self.board_num,
#                     low_chan   = low_chan,
#                     high_chan  = high_chan,
#                     num_points = num_samples,
#                     rate       = self.sampling.frequency,
#                     ul_range   = self.ao_range,
#                     memhandle  = self.memhandle,
#                     options    = ( enums.ScanOptions.BACKGROUND | 
#                                    enums.ScanOptions.CONTINUOUS |
#                                    enums.ScanOptions.RETRIGMODE )


    @classmethod
    def discover(cls):
        device_enumeration: list
        
        board_num   = 0
        board_index = 0
        for dev_handle in ul.get_daq_device_inventory(InterfaceType.ANY):
                board_num   = board_index
                board_index = board_index + 1
                device_enumeration.append(
                    MCCDAQ(board_num  = board_num,
                          dev_handle = dev_handle,
                          sampling   = params.Sampling(
                                          frequency    = 100,
                                          sample_range = { 0, 255 })))

        return device_enumeration
    
