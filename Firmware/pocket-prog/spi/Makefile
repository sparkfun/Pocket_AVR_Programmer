# ======================================================================
# Makefile for USB SPI interface
#
# Copyright (C) 2006 Dick Streefland
#
# This is free software, licensed under the terms of the GNU General
# Public License as published by the Free Software Foundation.
# ======================================================================

USBTINY		= ../usbtiny
TARGET_ARCH	= -mmcu=attiny2313
OBJECTS		= main.o
FLASH_CMD	= avrdude -c usbtiny -B 1 -pt2313 -U flash:w:main.hex
#FUSE_CMD	= avrdude -c usbtiny -B 10 -pt2313 -U hfuse:w:0xd9:m -U lfuse:w:0xef:m
FUSE_CMD	= avrdude -c usbtiny -pt2313 -U hfuse:w:0xdf:m -U lfuse:w:0xef:m
STACK		= 32
FLASH		= 2048
SRAM		= 128
SCHEM		= spi.ps

include $(USBTINY)/common.mk
