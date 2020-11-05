How to Use Data_Logger System
--------------------------- 
* The Breadboard and The Raspberry pi need to be used in a Greenhouse at a place where the rain cannot reach
* The system needs internet to remotely monitor the matrics measured such as Temperature and humidity
* Need a computer and the system to view the matrics locally and remotely
* Connet the whole system using the report of EEE3097S provided as a manual
* for more information please email us at tlotlisanglk@gmail.com and we can assist you with everything you need to know about the system


The API
-------

import os
import time
import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
import adafruit_dht
from Adafruit_IO import Client, Feed


#sets up dht11 output to pi GPIO and provides login details to webclient
class SetUp:
	def __init__(self, dhtDevice, IO_USERNAME, IO_KEY, aio):
		self.dhtDevice = dhtDevice
		self.IO_USERNAME = IO_USERNAME
		self.IO_KEY = IO_KEY
		self.aio = aio
#connects to feeds on webclient so sensor data can be sent to and displayed online
class SetFeed:
	def __init__(self, temperature_feed, humidity_feed, light_feed):
		self.temperature_feed = temperature_feed
		self.humidity_feed = humidity_feed
		self.light_feed = light_feed
#main class, reads sensor and ADC data and sends data to webclient
class ReadAndSend:
	def __init__(self):
		pass

	def readAndSend(self):
		#login details passed to SetUp class. dht output set to gpio 24
		newSetUp = SetUp(adafruit_dht.DHT11(board.D24), "Ddoy", "aio_OqZD42C9OM09r2wiYNAVoyK1K9yC", Client("Ddoy", "aio_OqZD42C9OM09r2wiYNAVoyK1K9yC"))
		#feeds passed to SetFeed class
		newFeed = SetFeed(newSetUp.aio.feeds('temperature'), newSetUp.aio.feeds('humidity'), newSetUp.aio.feeds('light'))
		#setting up adc spi communication with raspberry pi
		spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
		#setting adc output to gpio 22 on pi
		cs = digitalio.DigitalInOut(board.D22)
		mcp = MCP.MCP3008(spi, cs)
		#setting LDR analog output to mcp3008 pin 1
		chan1 = AnalogIn(mcp, MCP.P1)
		#while loop reads and sends sensor values every 0.5 sec, also handles errors
		while True:
			try:
				#getting values of DHT11 and ACD
				temperature = newSetUp.dhtDevice.temperature
				humidity = newSetUp.dhtDevice.humidity
				#voltage value converted to lumen
				light = chan1.voltage*40
				#prints light, temp and humidity to console
				print("Light level: " + str(light) + " lux")
				print("Temp: " + str(temperature) + "C   " + "Humidity: " + str(humidity) + "%")
				#sends sensor values to feeds on webclient 
				newSetUp.aio.send(newFeed.temperature_feed.key, str(temperature))
				newSetUp.aio.send(newFeed.humidity_feed.key, str(humidity))
				newSetUp.aio.send(newFeed.light_feed.key, str(light))
				#displays error causing runtime then continues while loop 
			except RuntimeError as error:
				print(error.args[0])
				time.sleep(0.5)
				continue
			except Exception as error:
				raise error
			#closes program when keyboard interrupted
			except (KeyboardInterrupt, SystemExit):
				interrupt()
			time.sleep(0.5)
	def interrupt(self):
		raise Exception("Program Closed")

newRead = ReadAndSend()
newRead.readAndSend()




Credits
-------

This package was created with Cookiecutter






