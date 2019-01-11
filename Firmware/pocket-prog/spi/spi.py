#!/usr/bin/python
# ======================================================================
# spi.py - USBtiny/spi test program
#
# Copyright 2006-2010 Dick Streefland
# ======================================================================

import sys, os.path, time
sys.path[0] = os.path.join(sys.path[0], '../util')
import usbtiny

vendor	= 0x1781
product	= 0x0C9F

# Generic requests
USBTINY_ECHO		= 0	# echo test
USBTINY_READ		= 1	# read byte (wIndex:address)
USBTINY_WRITE		= 2	# write byte (wIndex:address, wValue:value)
USBTINY_CLR		= 3	# clear bit (wIndex:address, wValue:bitno)
USBTINY_SET		= 4	# set bit (wIndex:address, wValue:bitno)
# Programming requests
USBTINY_POWERUP		= 5	# apply power (wValue:SCK-period, wIndex:RESET)
USBTINY_POWERDOWN	= 6	# remove power from chip
USBTINY_SPI		= 7	# issue SPI command (wValue:c1c0, wIndex:c3c2)
USBTINY_POLL_BYTES	= 8	# set poll bytes for write (wValue:p1p2)
USBTINY_FLASH_READ	= 9	# read flash (wIndex:address)
USBTINY_FLASH_WRITE	= 10	# write flash (wIndex:address, wValue:timeout)
USBTINY_EEPROM_READ	= 11	# read eeprom (wIndex:address)
USBTINY_EEPROM_WRITE	= 12	# write eeprom (wIndex:address, wValue:timeout)

usage = """Available commands:
	t                          - echo test
	r <addr>                   - read byte at <addr>
	w <addr> <byte>            - write byte at <addr>
	c <addr> <bit>             - clear bit at <addr>
	s <addr> <bit>             - set bit at <addr>
	U <reset>                  - powerup; set RESET to <reset>
	D                          - powerdown
	R                          - powerup; track MISO state with LED
	C <c1> <c2> <c3> <c4>      - issue SPI command
	P <p1> <p2>                - set poll bytes
	f <addr> <count>           - read from flash
	e <addr> <count>           - read from EEPROM
	F <addr> <timeout> <byte>  - write byte to flash
	E <addr> <timeout> <byte>  - write byte to EEPROM"""

# --- check arguments
cmd  = None
addr = 0x00
byte = 0x00
c3   = 0x00
c4   = 0x00
argc = len(sys.argv)
if argc > 1:
	cmd = sys.argv[1][0]
if argc > 2 and cmd != 't':
	byte = int(sys.argv[2], 16)
if argc > 3:
	addr = byte
	byte = int(sys.argv[3], 16)
if argc > 4:
	c3 = int(sys.argv[4], 16)
if argc > 5:
	c4 = int(sys.argv[5], 16)
if  not (argc == 2 and cmd in "tDR")\
and not (argc == 3 and cmd in "rU")\
and not (argc == 4 and cmd in "wcsPfe")\
and not (argc == 5 and cmd in "FE")\
and not (argc == 6 and cmd in "C"):
	print >> sys.stderr, usage
	sys.exit(1)

# --- open USB device
dev = usbtiny.USBtiny(vendor, product)

# --- dispatch command
if cmd == 't':
	dev.echo_test()
elif cmd == 'r':
	addr = byte
	byte = dev.control_in(USBTINY_READ, 0, addr, 1)
	print "%02x: %02x" % (addr, ord(byte))
elif cmd == 'w':
	dev.control_in(USBTINY_WRITE, byte, addr, 0)
elif cmd == 'c':
	dev.control_in(USBTINY_CLR, byte, addr, 0)
elif cmd == 's':
	dev.control_in(USBTINY_SET, byte, addr, 0)
elif cmd == 'U':
	dev.control_in(USBTINY_POWERUP, 20, byte, 0)
elif cmd == 'D':
	dev.control_in(USBTINY_POWERDOWN, 0, 0, 0)
elif cmd == 'R':
	try:
		dev.control_in(USBTINY_POWERUP, 20, 1, 0)
		led = 1
		while True:
			# read input PD3 (MISO from target)
			pind = dev.control_in(USBTINY_READ, 0, 0x30, 1)
			pd3 = (ord(pind) >> 3) & 1
			if pd3 != led:
				# update PB0 output (programmer LED)
				if pd3:
					dev.control_in(USBTINY_SET, 0, 0x38, 0)
				else:
					dev.control_in(USBTINY_CLR, 0, 0x38, 0)
				led = pd3
			time.sleep(0.02)
	except:
		pass
	finally:
		dev.control_in(USBTINY_POWERUP, 20, 0, 0)
		time.sleep(0.2)
		dev.control_in(USBTINY_POWERDOWN, 0, 0, 0)
elif cmd == 'C':
	r = dev.control_in(USBTINY_SPI, addr + (byte << 8), c3 + (c4 << 8), 4)
	if len(r) == 4:
		print "%02x %02x %02x %02x" % tuple([ord(i) for i in r])
	else:
		print "No power"
elif cmd == 'P':
	dev.control_in(USBTINY_POLL_BYTES, addr + (byte << 8), 0, 0)
elif cmd == 'f':
	r = dev.control_in(USBTINY_FLASH_READ, 0, addr, byte)
	usbtiny.dump(addr, r)
elif cmd == 'e':
	r = dev.control_in(USBTINY_EEPROM_READ, 0, addr, byte)
	usbtiny.dump(addr, r)
elif cmd == 'F':
	buf = chr(c3)
	dev.control_out(USBTINY_FLASH_WRITE, byte, addr, buf)
elif cmd == 'E':
	buf = chr(c3)
	dev.control_out(USBTINY_EEPROM_WRITE, byte, addr, buf)
