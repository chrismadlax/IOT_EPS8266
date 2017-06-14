from machine import Pin
import onewire

ow = onewire.OneWire(Pin(12))

import time, ds18x20

ds = ds18x20.DS18X20(ow)
while True:
	roms = ds.scan()
	ds.convert_temp()
	time.sleep_ms(750)
	for rom in roms:
		print(ds.read_temp(rom)) 