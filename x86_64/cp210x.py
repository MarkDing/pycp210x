from ctypes import *
import time


class PORT_CONFIG(Structure):
	_fields_ = [("Mode", c_ushort),
				("Reset_Latch", c_ushort),
				("Suspend_Latch", c_ushort),
				("EnhancedFxn", c_ubyte)]

#
# CP2108 Quad Port Config Structure
#
class QUAD_PORT_STATE(Structure):
	_fields_ = [("Mode_PB0", c_ushort),
				("Mode_PB1", c_ushort),
				("Mode_PB2", c_ushort),
				("Mode_PB3", c_ushort),
				("Mode_PB4", c_ushort),
				("LowPower_PB0", c_ushort),
				("LowPower_PB1", c_ushort),
				("LowPower_PB2", c_ushort),
				("LowPower_PB3", c_ushort),
				("LowPower_PB4", c_ushort),
				("Latch_PB0", c_ushort),
				("Latch_PB1", c_ushort),
				("Latch_PB2", c_ushort),
				("Latch_PB3", c_ushort),
				("Latch_PB4", c_ushort)
				]

class QUAD_PORT_CONFIG(Structure):
	_fields_ = [("Reset_Latch", QUAD_PORT_STATE),
				("Suspend_Latch", QUAD_PORT_STATE),
				("IPDelay_IFC0", c_ubyte),
				("IPDelay_IFC1", c_ubyte),
				("IPDelay_IFC2", c_ubyte),
				("IPDelay_IFC3", c_ubyte),
				("EnhancedFxn_IFC0", c_ubyte),
				("EnhancedFxn_IFC1", c_ubyte),
				("EnhancedFxn_IFC2", c_ubyte),
				("EnhancedFxn_IFC3", c_ubyte),
				("EnhancedFxn_Device", c_ubyte),
				("ExtClk0Freq", c_ubyte),
				("ExtClk1Freq", c_ubyte),
				("ExtClk2Freq", c_ubyte),
				("ExtClk3Freq", c_ubyte)
				]

if __name__ == '__main__':
	time_begin = time.clock()

	dll = cdll.LoadLibrary("CP210xManufacturing.dll")
	dwNumDevices = c_int()
	pStr = create_string_buffer(b'\000' * 256)

	status = dll.CP210x_GetNumDevices(byref(dwNumDevices))
	print("Found %d devices" %dwNumDevices.value)

	i = 0
	# Get description
	status = dll.CP210x_GetProductString(i, byref(pStr), 0x1)
	print((pStr.value))


	hdl = c_int()
	tmp = c_int()
	dll.CP210x_Open(i, byref(hdl))


	dll.CP210x_GetPartNumber(hdl.value, byref(tmp))
	print("Part Number = %d" %tmp.value);

	dll.CP210x_GetDeviceVid(hdl.value, byref(tmp))
	print("Vendor ID = %s" %hex(tmp.value));

	dll.CP210x_GetDevicePid(hdl.value, byref(tmp))
	print("Product ID = %s" %hex(tmp.value));

	dll.CP210x_GetSelfPower(hdl.value, byref(tmp))
	print("SelfPower = %s" %hex(tmp.value));

	dll.CP210x_GetMaxPower(hdl.value, byref(tmp))
	print("MaxPower = %s" %hex(tmp.value));

	dll.CP210x_GetDeviceVersion(hdl.value, byref(tmp))
	print("Version = %s" %hex(tmp.value));

	pcfg = QUAD_PORT_CONFIG()
	status = dll.CP210x_GetQuadPortConfig(hdl.value, byref(pcfg))

	pcfg.EnhancedFxn_IFC0 = 0x10

	status = dll.CP210x_SetQuadPortConfig(hdl.value, byref(pcfg))

	dll.CP210x_Reset(hdl.value)
	t = time.clock() - time_begin
	print("Time cost: %f" %t)
