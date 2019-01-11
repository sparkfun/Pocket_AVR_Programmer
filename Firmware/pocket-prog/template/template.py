#!/usr/bin/python
# ======================================================================
# template.py - USBtiny/template test program
#
# Copyright 2006-2010 Dick Streefland
# ======================================================================

import sys, os.path
sys.path[0] = os.path.join(sys.path[0], '../util')
import usbtiny

vendor  = 0x6666
product = 0x0001

dev = usbtiny.USBtiny(vendor, product)
dev.echo_test()
