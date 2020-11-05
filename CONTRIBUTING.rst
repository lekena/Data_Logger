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



End of API
----------


.. highlight:: shell

============
Contributing
============

Contributions are welcome, and they are greatly appreciated! Every little bit
helps, and credit will always be given.

You can contribute in many ways:

Types of Contributions
----------------------

Report Bugs
~~~~~~~~~~~

Report bugs at https://github.com/lekena/Data_logger/issues.

If you are reporting a bug, please include:

* Your operating system name and version.
* Any details about your local setup that might be helpful in troubleshooting.
* Detailed steps to reproduce the bug.

Fix Bugs
~~~~~~~~

Look through the GitHub issues for bugs. Anything tagged with "bug" and "help
wanted" is open to whoever wants to implement it.

Implement Features
~~~~~~~~~~~~~~~~~~

Look through the GitHub issues for features. Anything tagged with "enhancement"
and "help wanted" is open to whoever wants to implement it.

Write Documentation
~~~~~~~~~~~~~~~~~~~

Data_Logger could always use more documentation, whether as part of the
official Data_Logger docs, in docstrings, or even on the web in blog posts,
articles, and such.

Submit Feedback
~~~~~~~~~~~~~~~

The best way to send feedback is to file an issue at https://github.com/lekena/Data_logger/issues.

If you are proposing a feature:

* Explain in detail how it would work.
* Keep the scope as narrow as possible, to make it easier to implement.
* Remember that this is a volunteer-driven project, and that contributions
  are welcome :)

Get Started!
------------

Ready to contribute? Here's how to set up `Data_logger` for local development.

1. Fork the `Data_logger` repo on GitHub.
2. Clone your fork locally::

    $ git clone git@github.com:your_name_here/Data_logger.git

3. Install your local copy into a virtualenv. Assuming you have virtualenvwrapper installed, this is how you set up your fork for local development::

    $ mkvirtualenv Data_logger
    $ cd Data_logger/
    $ python setup.py develop

4. Create a branch for local development::

    $ git checkout -b name-of-your-bugfix-or-feature

   Now you can make your changes locally.

5. When you're done making changes, check that your changes pass flake8 and the
   tests, including testing other Python versions with tox::

    $ flake8 Data_logger tests
    $ python setup.py test or pytest
    $ tox

   To get flake8 and tox, just pip install them into your virtualenv.

6. Commit your changes and push your branch to GitHub::

    $ git add .
    $ git commit -m "Your detailed description of your changes."
    $ git push origin name-of-your-bugfix-or-feature

7. Submit a pull request through the GitHub website.

Pull Request Guidelines
-----------------------

Before you submit a pull request, check that it meets these guidelines:

1. The pull request should include tests.
2. If the pull request adds functionality, the docs should be updated. Put
   your new functionality into a function with a docstring, and add the
   feature to the list in README.rst.
3. The pull request should work for Python 3.5, 3.6, 3.7 and 3.8, and for PyPy. Check
   https://travis-ci.com/lekena/Data_logger/pull_requests
   and make sure that the tests pass for all supported Python versions.

Tips
----

To run a subset of tests::


    $ python -m unittest tests.test_Data_logger

Deploying
---------

A reminder for the maintainers on how to deploy.
Make sure all your changes are committed (including an entry in HISTORY.rst).
Then run::

$ bump2version patch # possible: major / minor / patch
$ git push
$ git push --tags

Travis will then deploy to PyPI if tests pass.
