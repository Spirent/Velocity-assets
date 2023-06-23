Project: RF switch driver 8x8 16 ports.
Description: iTest Python driver that connect 16 ports RF switch.
Category: driver
Class: Community
Tags: Drivers, Layer 2 Switch

This driver use Layer 2 Switch interface in order to connect RF switch ports under shelfs over multiple devices in a single link topology or in multi link topology
config.


WoW RF switch notes:::

8 input,
8 output,

1 input to multiple outputs.

example:

input 1 to output 1, output 2.


at end of reservation link inputs to output0 (unmap).

Notes:::

This driver connect a device 1 input to any Outputs only no reverse order is supported.

The driver connects pools of resources under a collection called cable-macs, on velocity topology this could been seen as shelfs containing such devices. (please look at attached images under Documentation).

The Input was defined as virtual ports, and the output was set at each shelf as a property per customer use case.

