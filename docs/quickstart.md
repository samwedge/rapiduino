# Quickstart

## Installation

```bash
pip install rapiduino
```

## Usage

To use with an Arduino Uno, simply import the class and globals as follows. Importing globals give you access to the same
INPUT, OUTPUT, HIGH, LOW, A0, A1 etc. as when developing an Arduino sketch

```python
from rapiduino.globals.arduino_uno import *
from rapiduino.globals.common import *
from rapiduino.boards.arduino import Arduino
```

Set up the class and serial connection with the following. The port to be passed in can be identified using the Arduino software

```python
arduino = Arduino.uno('port_identifier')
```

Then start using it! Here is a blinking LED example:

```python
import time
while True:
    arduino.digital_write(13, HIGH)
    time.sleep(1)
    arduino.digital_write(13, LOW)
    time.sleep(1)
```

You can also use classes for components (such as LEDs) which make using the Arduino easier and less error-prone.
The components are "registered" to the Arduino along with a pin-mapping which tells the Arduino object which pins are connected
to the component. Let's look at an example with an LED:

```python
from rapiduino.components.led import LED
led = LED(arduino, 13)
```

This creates an LED object and registers it to the arduino against pin 13. When binding, the code automatically
takes care of checking compatibility, raising an error if there is a problem. For example, if you are trying to connect 
a component that requires a PWM pin to a non-PWM pin, you will get a helpful message.

You can re-write the blink example as:

```python
while True:
    led.toggle()
    time.sleep(1)
```

The benefit of this is that you can use methods with familiar names such as:

```python
led.turn_on()
led.turn_off()
led.toggle()
```
    
You don't need to think of pin states or pin modes when interacting with your components, and you don't need to keep
track of which pin is connected to which component - rapiduino will do that for you.

