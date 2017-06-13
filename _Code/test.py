from machine import Pinimport time
print('hello world')
pin = Pin(10, Pin.OUT)
for i in range(10):	pin.low()	time.sleep(0.5)	pin.high()	time.sleep(0.5)pin.high()while True:	if pin.value() == 0:		print('USR buttom push!!')	time.sleep(0.1)