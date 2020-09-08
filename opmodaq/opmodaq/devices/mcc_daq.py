import platform
import warnings

devices: list = []

if platform.system() == "Windows":
    print("Importing Windows universal library")
    import opmodaq.devices.mcc_daq_mcculw as mcc_daq
    from opmodaq.devices.mcc_daq_mcculw import MCCDAQ
elif platform.system() == "Linux":
    print("Importing daqhats Linux library")
    import opmodaq.devices.mcc_daq_daqhats as mcc_daq
    from opmodaq.devices.mcc_daq_daqhats import MCCDAQ


