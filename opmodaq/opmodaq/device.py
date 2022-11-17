

class Device:
    def __init__(self,
                 board_num,
                 dev_handle):
        self.board_num  = board_num
        self.dev_handle = dev_handle

class Channel(object):
    def __init__(self, device: Device, channel_idx):
        self.device      = device
        self.channel_idx = channel_idx


