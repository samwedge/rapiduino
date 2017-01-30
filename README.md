# Rapiduino

Rapiduino is a Python library (fully tested in Python 2.7 and 3.4) to allow Python code to control an Arduino.
The Python code runs on a computer connected to an Arduino through a serial connection.

A sketch is provided to upload to the Arduino.
The Rapiduino library can be used to connect to the Arduino and send it familiar commands such as digitalWrite and pinMode.
By sending these commands from Python and not writing them directly on the Arduino, you gain the power of Python's wonderful syntax and libraries. 


## Why use Rapiduino?

* Rapidly develop using everyone's favourite language
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

Install this package using Pip:
    
    pip install git+https://github.com/samwedge/rapiduino.git

Alternatively, copy the "rapiduino" package directory into your python site-packages or to a local directory.

It has been fully tested with Python 2.7 and Python 3.4.


## Usage

To use with an ArduinoUno, simply import the class and globals as follows

    from rapiduino.devices import ArduinoUno
    from rapiduino.globals import *

Set up the class and serial connection with the following. The port can be identified using the Arduino software

    serial_port = '/dev/ttyACM0'
    arduino = ArduinoUno()
    arduino.connection.open(serial_port)
    
Then start using! Here is a blinking LED example:
    
    import time
    while True:
        arduino.digital_write(13, HIGH)
        time.sleep(1)
        arduino.digital_write(13, LOW)
        time.sleep(1)
        
The above works out of the box.
My plan for the future is to create components that can be "plugged in" to the Arduino object to make things really simple,
 allowing things such as servos to be hot-pluggable. 
    

## Contribution

Yes please! Code and/or suggestions are very welcome!


## License

Copyright (c) 2017 Samuel Wedge
samwedge@gmail.com, samwedge.co.uk

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.