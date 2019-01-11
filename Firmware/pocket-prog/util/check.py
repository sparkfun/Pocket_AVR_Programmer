#!/usr/bin/python
# ======================================================================
# check.py - Check section sizes and other constraints
#
# Copyright 2006-2010 Dick Streefland
#
# This is free software, licensed under the terms of the GNU General
# Public License as published by the Free Software Foundation.
# ======================================================================

import os, sys

stacksize = 32
flashsize = 2048
ramsize   = 128

if len(sys.argv) > 2:
	stacksize = int(sys.argv[2])
if len(sys.argv) > 3:
	flashsize = int(sys.argv[3])
if len(sys.argv) > 4:
	ramsize   = int(sys.argv[4])

max_sram = ramsize - stacksize

crc4tab	= 0
text	= 0
data	= 0
bss	= 0
for line in os.popen('avr-objdump -ht ' + sys.argv[1]).readlines():
	a = line.split()
	if len(a) == 7:
		if a[1] == '.text':
			text = int(a[2], 16)
		if a[1] == '.data':
			data = int(a[2], 16)
		if a[1] == '.bss':
			bss = int(a[2], 16)
	if len(a) >= 5 and a[-1] == 'crc4tab':
		crc4tab = int(a[0], 16)
print 'text: %d, data: %d, bss: %d' % (text, data, bss)

status = 0
if text == 0:
	print 'ERROR: No code! Upgrade your binutils package or remove --gc-sections'
	status = 1
overflow = text + data - flashsize
if overflow > 0:
	print 'ERROR: Flash size limit exceeded by %d bytes.' % overflow
	status = 1
overflow = bss + data - max_sram
if overflow > 0:
	print 'ERROR: SRAM size limit exceeded by %d bytes.' % overflow
	status = 1
if (crc4tab & 0xff) > 0xf0:
	print 'ERROR: The table crc4tab should not cross a page boundary.'
	status = 1
sys.exit(status)
