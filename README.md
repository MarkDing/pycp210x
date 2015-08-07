How do I setup CP2108 port config using python?
=======

## Get CP210x manufacturing DLL from AN721
AN721SW package contains a DLL file for accessing CP210x configuration. Here is the path of Windows DLL.  
AN721SW\Windows\CP210x_InterfaceLibrary\ManufacturingDLL\x86_64\CP210xManufacturing.dll

## Load DLL file
Prepare a Python file, named cp210x.py, 
    
* import ctypes. 

```python
from ctypes import *
```

ctypes is a foreign function library for Python. It provides C compatible data types, and allows calling functions in DLLs or shared libraries. It can be used to wrap these libraries in pure Python.

* Load DLL

```python
dll = cdll.LoadLibrary("CP210xManufacturing.dll")
```

Load a shared library into the process and return it. This method always returns a new instance of the library

## Call function inside dll
Some functions contain pointer parameters. Like this one:

```C
CP210x_STATUS CP210x_GetNumDevices( LPDWORD NumDevices )
```

Python ctypes exports the byref() function which is used to pass parameters by reference. 
Here is the example:

```python
dwNumDevices = c_int()
status = dll.CP210x_GetNumDevices(byref(dwNumDevices))
print("Found %d devices" %dwNumDevices.value)
```

For a CP2108 device, it outputs "Found 4 devices"

## Get CP2108 port config

Two functions access CP2108 port config

```C
CP210x_STATUS CP210x_GetQuadPortConfig( 
    HANDLE cyHandle,
    QUAD_PORT_CONFIG*   QuadPortConfig
    );
CP210x_STATUS CP210x_SetQuadPortConfig( 
    HANDLE cyHandle,
    QUAD_PORT_CONFIG*   QuadPortConfig
    );
```

The parameter QUAD_PORT_CONFIG is a structure which defined in CP210xManufaturingDLL.h. 
In Python, structures and unions must derive from the Structure and Union base classes which are defined in the ctypes module.
Here are the definitions in Python.

```python
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
```

Then, we can get port config values and set one GPIO to be clock output. Here is the example code

```python
pcfg = QUAD_PORT_CONFIG()
status = dll.CP210x_GetQuadPortConfig(hdl.value, byref(pcfg))
pcfg.EnhancedFxn_IFC0 = 0x10
status = dll.CP210x_SetQuadPortConfig(hdl.value, byref(pcfg))
dll.CP210x_Reset(hdl.value)
```

On the board, we can see the LED DS3 is on. We can see clock signal by measuring on an oscilloscope.
   

## Reference:
Here is the Python official website for ctypes
https://docs.python.org/3.4/library/ctypes.html#structure-union-alignment-and-byte-order
