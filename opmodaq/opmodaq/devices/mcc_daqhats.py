from __future__ import print_function

import opmodaq.device as dev
import opmodaq.parameters as params
import opmodaq.generators as gen

import numpy as np

from daqhats import mcc152, OptionFlags, HatIDs, HatError, hat_list


class MCCDAQHatChannel(dev.Channel):

    def __init__(self, device, channel_idx):
        dev.Channel.__init__(self, device, channel_idx)
    
    def analog_out_samples(self, samples: list):
        board_num    = self.device.board_num
        signal_range = self.device.sampling.sample_range
        a_out_write  = self.device.dev_handle.a_out_write
        for value in samples:
            a_out_write(self.channel_idx,
                        value,
                        options=OptionFlags.DEFAULT)

    def analog_out(self,
                   generator:    gen.SignalGenerator,
                   sample_range: range = range(0,0)):
        if len(sample_range) == 0:
            sample_range = range(self.device.sampling.frequency)

        # Local variables to reduce dereferences in loop:
        board_num    = self.device.board_num
        signal_range = self.device.sampling.sample_range
        a_out_write  = self.device.dev_handle.a_out_write
        samples      = list(generator.samples(self.device.sampling,
                                              sample_range))
        data         = np.zeros(len(samples))
        sample_idx   = 0
        for sample in samples:
            data[sample_idx] = sample
            sample_idx = sample_idx + 1

        # interrupt_callback_enable
        while 1:
            for value in data:
                a_out_write(self.channel_idx,
                            value,
                            options = OptionFlags.DEFAULT)

class MCCDAQHat(dev.Device):
  
    def __init__(self, board_num, daqhat):
        self.daqhat = daqhat
        # Voltage ranges of analog outputs
        self.sampling = params.Sampling(
                            frequency     = 5000,
                            sample_range  = { self.daqhat.info().AO_MIN_VOLTAGE,
                                              self.daqhat.info().AO_MAX_VOLTAGE })
        
        self.num_ao_channels: int = self.daqhat.info().NUM_AO_CHANNELS

        dev.Device.__init__(self, board_num, self.daqhat)
        
    def channel(self, channel_idx):
        return MCCDAQHatChannel(self, channel_idx)

    @classmethod
    def discover(cls):
        device_enumeration: list = []

        board_list  = hat_list(filter_by_id = HatIDs.ANY)
        board_num   = 0
        board_index = 0
        if not board_list:
            return device_enumeration
        for device in board_list:
                board_num = device.address
                # ul.create_daq_device(board_num, device)
                board_index = board_index + 2
                device_enumeration.append(
                    MCCDAQHat(board_num, mcc152(board_num)))
        return device_enumeration

