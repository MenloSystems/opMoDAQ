import platform
import warnings

print("Importing MCC Universa Library")
import opmodaq.devices.mcc_mccul as mcc
from opmodaq.devices.mcc_mccul import MCCDAQ, MCCDAQChannel

if platform.system() == "Linux":
    print("Importing MCC daqhats Linux library")
    from opmodaq.devices.mcc_daqhats import MCCDAQHat, MCCDAQHatChannel


