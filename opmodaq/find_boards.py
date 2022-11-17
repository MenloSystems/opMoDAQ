import sys
from daqhats import hat_list, HatIDs, mcc152

# get hat list of MCC daqhat boards
board_list = hat_list(filter_by_id = HatIDs.ANY)
if not board_list:
    print("No boards found")
    sys.exit()

# Read and display every channel
for entry in board_list: 
    if entry.id == HatIDs.MCC_152:
        print("Board {}: MCC 152".format(entry.address))
        board = mcc152(entry.address)
        for channel in range(board.info().NUM_AO_CHANNELS):
            value = board.a_in_read(channel)
            print("Ch {0}: {1:.3f}".format(channel, value))
