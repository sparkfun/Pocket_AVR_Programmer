// ======================================================================
// USBtiny template application
//
// Copyright 2006-2010 Dick Streefland
//
// This is free software, licensed under the terms of the GNU General
// Public License as published by the Free Software Foundation.
// ======================================================================

#include "usb.h"

// ----------------------------------------------------------------------
// Handle a non-standard SETUP packet.
// ----------------------------------------------------------------------
extern	byte_t	usb_setup ( byte_t data[8] )
{
	return 8;	// simply echo back the setup packet
}

// ----------------------------------------------------------------------
// Handle an IN packet. (USBTINY_CALLBACK_IN==1)
// ----------------------------------------------------------------------
extern	byte_t	usb_in ( byte_t* data, byte_t len )
{
	return 0;
}

// ----------------------------------------------------------------------
// Handle an OUT packet. (USBTINY_CALLBACK_OUT==1)
// ----------------------------------------------------------------------
extern	void	usb_out ( byte_t* data, byte_t len )
{
}

// ----------------------------------------------------------------------
// Main
// ----------------------------------------------------------------------
extern	int	main ( void )
{
	usb_init();
	for	( ;; )
	{
		usb_poll();
	}
}
