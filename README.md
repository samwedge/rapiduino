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
    led = LED()
    bindings = ((13, 0),)
    arduino.bind_component(led, bindings)
    
This creates an led object and binds it to the arduino. Binding it allows you to communicate with the led object, and let
the led object talk to the arduino object. To bind an object, you need to specify bindings. This is basically a tuple of
tuples to tell the arduino which pin is to be connected to each part of the component. In the case of the LED, there is
only one pin to connect (Pin 0) which is connected to the arduino (Pin 13). Hence, the tuple looks like:

    ((13, 0),)
    
When binding, the code automatically takes care of checking compatibility, raising an error if there is a problem. For
example, if you are trying to connect a component that requires a PWM pin to a non-PWM pin, you will get a helpful message.

Once the LED has been bound to the Arduino, you can re-write the blink example as:

    while True:
        led.toggle()
        time.sleep(1)

The benefit of this is that you can use methods with familiar names such as:

    led.turn_on()
    led.turn_off()
    
You don't need to think of pin numbers, pin states or pin modes beyone the initial set-up.


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