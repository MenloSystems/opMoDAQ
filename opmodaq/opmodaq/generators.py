
from __future__ import absolute_import, division, print_function

import opmodaq.parameters as params
import opmodaq.generators as gen
import opmodaq.signal     as sig

from opmodaq.device  import Device

import array
import numpy as np
import math
import time
import enum
import types



class SignalGenerator(object):
    """
    Function generator base class
    """
    def __init__(self,
                 signal:     params.Signal,
                 sample_fun: types.FunctionType):
        self.signal     = signal
        self.sample_fun = sample_fun



class LevelSequence(gen.SignalGenerator):
    """
    Function generator setting analog output levels with specified
    edge distances.
    """

class SingleShot(gen.SignalGenerator):
    """
    Function generator setting analog output levels with specified
    edge distances.
    """

class Oscillator(gen.SignalGenerator):
    """
    Function generator of oscillating (continuously repeated) values
    in the value domain
    """
    
    @classmethod
    def zero(cls,
             signal:      params.Signal,
             sampling:    params.Sampling,
             sample_t:    int):
        return 0
    
    def __init__(self,
                 signal:        params.Signal,
                 generator_fun: zero):
        self.signal        = signal
        self.generator_fun = generator_fun
        
        gen.SignalGenerator.__init__(
            self,
            signal     = signal,
            sample_fun = self.samples)
    
    def generator(self, sampling: params.Sampling):
        return self.generator_fun(sampling = sampling)

    def samples(self,
                sampling:     params.Sampling,
                sample_range: range):
        return map(self.generator(sampling), sample_range)

class Sine(gen.Oscillator):

    def __init__(self,
                 freq:   float,
                 signal: params.Signal):
          self.freq = freq          
          gen.Oscillator.__init__(
              self,
              signal        = signal,
              generator_fun = self.fun)
             
    def fun(self,
            sampling: params.Sampling):
        return lambda t: ( ( ( math.sin( math.pi * 2
                                       * self.freq * t
                                       / sampling.frequency
                                     ) + 1 
                           ) / 2 * self.signal.amplitude
                         ) + self.signal.min + self.signal.offset )
                         

class Saw(gen.Oscillator):

    def __init__(self,
                 freq:   float,
                 signal: params.Signal):
          self.freq = freq
          gen.Oscillator.__init__(
              self,
              signal        = signal,
              generator_fun = self.fun)
             
    def fun(self,
            sampling: params.Sampling):
        return lambda t: ( (t * (self.freq / sampling.frequency))
                               % (self.signal.amplitude / 2)
                         ) * 2 + self.signal.min + self.signal.offset


