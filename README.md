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
* You need timing accuracy that Rapiduino does not yet support; For example, for an ultrasonic sensor where the connection lag could cause innacuracy
* Probably many others personal to your project...


## Status

Rapiduino is in active development.
It is ready to be used in simple projects, but there may be some major breaking changes and restructuring until it settles down


## Installation

    pip install rapiduino


## Usage

To use with an ArduinoUno, simply import the class and globals as follows

    from rapiduino.devices import ArduinoUno
    from rapiduino.globals.arduino_uno import *

Set up the class and serial connection with the following. The port to be passed in can be identified using the Arduino software

    arduino = ArduinoUno('/dev/ttyACM0')
    
Then start using it! Here is a blinking LED example:
    
    import time
    while True:
        arduino.digital_write(13, HIGH)
        time.sleep(1)
        arduino.digital_write(13, LOW)
        time.sleep(1)
        
You can also use classes for components (such as LEDs, Servos etc.) which make using the Arduino easier and less error-prone.
The components are "bound" to the Arduino along with a pin-mapping which tells the Arduino object which pin is connected
to which component pin. As an example, the LED class has one pin which can be initialised and connected to the arduino
as follows:

    from rapiduino.components.basic import LED
    from rapiduino.devices import PinMapping
    led = LED()
    bindings = [PinMapping(device_pin_no=13, component_pin_no=0)]
    arduino.bind_component(led, bindings)
    
This creates an led object and binds it to the arduino. Binding it allows you to communicate with the led object, and let
the led object talk to the arduino object. To bind an object, you need to specify bindings. This is basically a sequence of
PinMappings to tell the arduino which pin is to be connected to each part of the component. In the case of the LED, there is
only one pin to connect (Pin 0) which is connected to the arduino (Pin 13). Hence, the binding looks like:

    [PinMapping(device_pin_no=13, component_pin_no=0)]
    
When binding, the code automatically takes care of checking compatibility, raising an error if there is a problem. For
example, if you are trying to connect a component that requires a PWM pin to a non-PWM pin, you will get a helpful message.

Once the LED has been bound to the Arduino, you can re-write the blink example as:

    while True:
        led.toggle()
        time.sleep(1)

The benefit of this is that you can use methods with familiar names such as:

    led.turn_on()
    led.turn_off()
    
You don't need to think of pin numbers, pin states or pin modes beyond the initial set-up.


## Contribution

Yes please! Code and/or suggestions are very welcome! Feel free to raise an issue or raise a pull request from a fork.


## Developing

Rapiduino uses [poetry](https://python-poetry.org/docs/) to handle the installation.


To install Rapiuino for development:

`poetry install`

To run tests:

`poetry run python -m unittest discover`

Type checking:

`poetry run python -m mypy rapiduino`

Linting:

`poetry run python -m flake8 rapiduino`


## Licence

[Rapiduino is released under the Apache-2.0 licence](https://github.com/samwedge/rapiduino/blob/master/LICENSE).

If you contribute code to this repository, you agree that your code will also be released under this licence.