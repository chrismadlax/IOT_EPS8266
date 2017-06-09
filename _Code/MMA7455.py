''' MMA7455 access demo'''
from machine import Pin, SPI

#setup h/w SPI port 1, speed 400khz, mode=0, cs pin in gpio15
hspi = SPI(1, baudrate=400000, polarity=0, phase=0)
cs = Pin(15, Pin.OUT)
cs.high()

class MMA7455:
	def __init__(self):
		cs.low()
		hspi.read(2)
		cs.high()
	def CS_on(self):
		cs.low()
	def CS_off(self):
		cs.high()
	def SPIread(self, Reg):
		Reg = Reg<<1
		buf = hspi.read(2, Reg)
		return buf
	def SPIwrite(self, Reg, Data):
		Reg = (Reg<<1)|0x80
		buf = [Reg, Data]
		buf = bytes(buf)
		hspi.write(buf)
		return buf
	def byte2int(self, DataH, DataL):
		Datalist = list(DataH+DataL)
		Datalist.reverse()
		DataOut = 0
		for i in range(4):
			DataOut = DataOut+(Datalist[i]*(256*i))
		return DataOut
	def DataReady(self):
		buf = self.SPIread(0x09)
		buf = list(buf)
		buf = buf[1]
		return buf
	def MeasurementOn(self):
		self.SPIwrite(0x16, 0x01)
	def ReadXYZ(self):
		buf = []
		for i in range(3):
			lsb = self.SPIread(i*2)
			msb = self.SPIread(i*2+1)
			buf.append(self.byte2int(msb, lsb))
		return buf
	
if __name__ == '__main__':
	sensor = MMA7455()
	import time
	
	sensor.CS_on()
	sensor.MeasurementOn()
	sensor.CS_off()
	while True:
		sensor.CS_on()
		DRDY = sensor.DataReady()
		if DRDY >= 1:
			Data = sensor.ReadXYZ()
			print('x=%d y=%d z=%d' %(Data[0], Data[1], Data[2]))
			if DRDY == 3:
				print('Over write')
		time.sleep_us(10)
		sensor.CS_off()