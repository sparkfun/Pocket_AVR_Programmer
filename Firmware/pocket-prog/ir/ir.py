#!/usr/bin/python
# ======================================================================
# ir.py - USBtiny/ir test program
# ======================================================================

import sys, os.path
sys.path[0] = os.path.join(sys.path[0], '../util')
import usbtiny

vendor  = 0x03eb
product = 0x0002

IGORPLUG_CLEAR	= 1	# clear IR data
IGORPLUG_READ	= 2	# read IR data (wValue: offset)
LCD_INSTR	= 20	# write instructions to LCD (via OUT)
LCD_DATA	= 21	# write data to LCD (via OUT)

usage = """Available commands:
    t               - perform USB echo test
    c               - clear IR data
    r               - read current IR data
    i <byte> ...    - send instruction bytes to LCD
    d <byte> ...    - send data bytes to LCD
    s <string> ...  - send strings to LCD"""

dev = usbtiny.USBtiny(vendor, product)

cmd = '?'
if len(sys.argv) > 1:
	cmd = sys.argv[1]
arg = sys.argv[2:]
if cmd == 'r':
	data = dev.control_in(IGORPLUG_READ, 0, 0, 3 + 36)
	usbtiny.dump(0, data)
elif cmd == 'c':
	dev.control_in(IGORPLUG_CLEAR, 0, 0, 0)
elif cmd == 't':
	dev.echo_test()
elif cmd == 'i':
	s = ''.join([chr(int(x,16)) for x in arg])
	dev.control_out(LCD_INSTR, 0, 0, s)
elif cmd == 'd':
	s = ''.join([chr(int(x,16)) for x in arg])
	dev.control_out(LCD_DATA, 0, 0, s)
elif cmd == 's':
	dev.control_out(LCD_DATA, 0, 0, ' '.join(arg))
else:
	print >> sys.stderr, usage
	sys.exit(1)
