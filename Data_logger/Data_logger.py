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
