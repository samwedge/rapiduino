# Rapiduino

Rapiduino is a Python library to allow Python code to control an Arduino.
The Python code runs on a computer connected to an Arduino through a serial connection.

A sketch is provided to upload to the Arduino.
The Rapiduino library can be used to connect to the Arduino and send it familiar commands such as `digitalWrite` and `pinMode`.
By sending these commands from Python and not compiling/uploading directly to the Arduino, you gain the ability to dynamically
attach and test components and also have the capability to obtain data from your sensors wiithout having to write any custom
Arduino code. You also gain the power of Python's wonderful syntax and libraries. 


## Why use Rapiduino?

* Rapidly develop using everyone's favourite language 😉
* Easily integrate an Arduino with Python's libraries to provide a real-time clock, web access, data visualisation, number crunching etc...
* Allow hot-swappable parts. Change pin mode, pin state etc. whenever you like from your Python code!
* Easily obtain data from your Arduino without setting up any custom communication.
* Probably many other benefits that will become realised as time goes on...


## Are there any downsides?

Of course. Don't use this library if:

* You are not able to run a computer alongside an Arduino (not even a Raspberry Pi) because of issues such as size, battery, operating conditions etc.
* You need timing accuracy that Rapiduino does not yet support; For example, for an ultrasonic sensor where the connection
  lag could cause inaccuracy (although there are workarounds for this for specific components)
* Probably many others personal to your project...
