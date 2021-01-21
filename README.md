[![Build and Test](https://github.com/samwedge/rapiduino/workflows/Build%20and%20Test/badge.svg)](https://github.com/samwedge/rapiduino/actions?query=workflow%3A%22Build+and+Test%22)
[![Coverage Status](https://coveralls.io/repos/github/samwedge/rapiduino/badge.svg?branch=master)](https://coveralls.io/github/samwedge/rapiduino?branch=master)
![Python Supported Versions](https://img.shields.io/pypi/pyversions/rapiduino)
[![GitHub - License](https://img.shields.io/github/license/samwedge/rapiduino)](https://github.com/samwedge/rapiduino/blob/master/LICENSE)
[![Latest Version](https://img.shields.io/pypi/v/rapiduino)](https://pypi.org/project/rapiduino/)

# Rapiduino

Rapiduino is a Python library to allow Python code to control an Arduino.
The Python code runs on a computer connected to an Arduino through a serial connection.

A sketch is provided to upload to the Arduino.
The Rapiduino library can be used to connect to the Arduino and send it familiar commands such as digitalWrite and pinMode.
By sending these commands from Python and not writing them directly on the Arduino, you gain the power of Python's wonderful syntax and libraries. 

## Why use Rapiduino?

* Rapidly develop using everyone's favourite language 😉
* Easily integrate an Arduino with Python's libraries to provide a real-time clock, web access, data visualisation, number crunching etc...
* Allow hot-swappable parts. Change pin mode, pin state etc. whenever you like from your Python code!
* Easily obtain data from your Arduino without setting up any custom communication
* Probably many other benefits that will become realised as time goes on...


## Are there any downsides?

Of course. Don't use this library if:
* You are not able to run a computer alongside an Arduino (not even a Raspberry Pi) because of issues such as size, battery, operating conditions etc.
* You need timing accuracy that Rapiduino does not yet support; For example, for an ultrasonic sensor where the connection
  lag could cause inaccuracy (although there are workarounds for this for specific components)
* Probably many others personal to your project...


## Status

Rapiduino is in active development.
It is ready to be used in simple projects, but there may be some breaking changes and restructuring until it settles down


## Installation

    pip install rapiduino


## Usage

To use with an ArduinoUno, simply import the class and globals as follows. Importing globals give you access to the same
INPUT, OUTPUT, HIGH, LOW, A0, A1 etc. as when developing an Arduino sketch

    from rapiduino.globals.arduino_uno import *
    from rapiduino.globals.common import *
    from rapiduino.boards.arduino import Arduino

Set up the class and serial connection with the following. The port to be passed in can be identified using the Arduino software

    arduino = Arduino.uno('port_identifier')
    
Then start using it! Here is a blinking LED example:
    
    import time
    while True:
        arduino.digital_write(13, HIGH)
        time.sleep(1)
        arduino.digital_write(13, LOW)
        time.sleep(1)
        
You can also use classes for components (such as LEDs) which make using the Arduino easier and less error-prone.
The components are "registered" to the Arduino along with a pin-mapping which tells the Arduino object which pins are connected
to the component. Let's look at an example with an LED:

    from rapiduino.components.led import LED
    led = LED(arduino, 13)
    
This creates an LED object and registers it to the arduino against pin 13. When binding, the code automatically
takes care of checking compatibility, raising an error if there is a problem. For example, if you are trying to connect 
a component that requires a PWM pin to a non-PWM pin, you will get a helpful message.

You can re-write the blink example as:

    while True:
        led.toggle()
        time.sleep(1)

The benefit of this is that you can use methods with familiar names such as:

    led.turn_on()
    led.turn_off()
    led.toggle()
    
You don't need to think of pin states or pin modes when interacting with your components, and you don't need to keep
track of which pin is connected to which component - rapiduino will do that for you.


## Contribution

Yes please! Code and/or suggestions are very welcome! Feel free to raise an issue or raise a pull request from a fork.


## Developing

Rapiduino uses [poetry](https://python-poetry.org/docs/) to handle the installation.

To install Rapiuino for development:

`poetry install`

To run tests:

`make test` will run all testing, linting, type checking and coverage reporting

`make fix` will auto-fix any issues found by `isort` and `mypy`


## Licence

[Rapiduino is released under the Apache-2.0 licence](https://github.com/samwedge/rapiduino/blob/master/LICENSE).

If you contribute code to this repository, you agree that your code will also be released under this licence.