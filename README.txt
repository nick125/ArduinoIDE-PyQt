Dawn
------------------
This project is to develop the next-generation of Arduino and others IDE. 

Dependencies
------------
* Python
* Qt/PyQt 4
* QScintilla

For debian we'd need the following packaged apt-get
gcc avr python pyqt pyqt-text 


Getting Started
---------------
Coming Soon, but for now check the TODO.txt


Project hosting, wiki, issues at Google
http://code.google.com/p/arduino-pyqt/

Source code is at
http://github.com/nick125/ArduinoIDE-PyQt

ArduinoIDE#irc.freenode.net


== The Vision ==
To create a integrated IDE for arduino
* full text editor, with autocompletion 
* Integrated help browser and api documentation 
* Ability to monitor a serial in a seperate window
* speak and code more than one arduino session at a time

Sessions
Ability to "bookmark a session", such as open code, and the help pages, forum topics.


== Work In Progress ==

One of the benefits to Arduino would be the necessity of this project to create the API documentation.

Current scenariio is that a website must be browsed, and autocomplete is independant.

The solution is to document the api's which are stored as yaml. If utulised then this will hopefully feed its
way into the arduino mother project. There is a simple interface to document the api.

The yaml solutions serves a simple purpose.

For autocompletion to work, the following would be simple:

pinMode(pin, mode) set pin to INPUT or OUTPUT mode

However for Serial.write the following sould be needed
Serial.write() write to serial port
write() write an blank line
write(foo) write foo
write(foo, HEX) write HEX as x y z

1) documents a "function", or class, arduino itself is a "core" class whilst "servo" is standard, and other contrib. This means function are on demand (antone remember the MSDN documentation....) ie only there when required
2) a list of keywords such as INPUT, OUTPUT so it hightlights (to research is internal functions)
3) a one liner of its functionallity



== Thoughts ==

Use google appengine to distribute the documantation and libs.. an distribution machine for all of us.

