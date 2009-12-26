#!/bin/sh
# ardmake: A command-line Arduino make/build environment.     2009-12-08
# For instructions, run with the argument "help"!
#
# This script is Copyright (c) 2009 Kimmo Kulovesi <http://arkku.com/>.
# Use at your own risk only. Released under GPL, see below for details.
# Please mark any modified copies as such, and retain the original
# copyright notice in all relevant files, usage, and documentation.
#
#
#   INTRODUCTION
#
# This script runs the Makefile included with Arduino to compile and
# upload projects on the command-line. This script sets all
# board-specific variables automatically according to the board type,
# as well as detects and adds libraries automatically based on the
# #include-directives in the program (i.e. with the same convenience
# as the graphical Arduino environment). This script also supports
# burning bootloaders, setting fuses, uploading pre-compiled binaries,
# and using certain external programming devices (e.g. for stand-alone
# microcontrollers).
#
# In short, this script can completely replace the Arduino IDE for
# typical Arduino/ATMega development, and in some cases it can even
# do more than the IDE. The intended user is a relatively experienced
# command-line user, who wants to combine the power of their chosen
# editor and tools with the development speed and convenience of
# the Arduino platform. Beginners will probably be more comfortable
# starting with the simple graphical Arduino IDE.
#
# This script is not an official part of Arduino, but since it is
# in active use by its author, it will probably be rapidly updated
# to support any new Arduino releases (and some care has been
# taken to minimise the changes necessary to support each release).
#
#
#   INSTALLATION
#
# Install Arduino somewhere, e.g. /opt/arduino or ~/arduino. If you
# are using additional core types (e.g. Sanguino) or custom board
# types (e.g. ADABoot), also install them. Custom libraries can be
# installed in e.g. ~/sketchbook/libraries, or anywhere you like.
#
# Install the AVR version of GCC (e.g. package name avr-gcc) and
# AVRDUDE (you can probably use the one bundled with Arduino if you
# prefer). Preferably install versions packaged for your specific
# Linux distribution (e.g. with apt-get install avr-gcc avrdude).
#
# Put this script somewhere along your PATH (e.g. /usr/local/bin,
# ~/bin, or wherever you like to install programs). This script is
# distributed by the author as "arduino_make.sh" due to historical
# reasons, but "ardmake" is the suggested name (shorter to type and
# all). Run this script with the parameter "help" and read about
# configuring and usage (usually only the board type needs to be set
# and you are good to go).
#
#
#   SYSTEM REQUIREMENTS
#
# Last been tested with Arduino version 0017 on Ubuntu 9.04, with
# avr-gcc and avrdude installed from Ubuntu packages. While this script
# should run in non-Linux environments, there are some dependencies to
# GNU tools (e.g. GNU Make), so GNU/Linux should be considered the
# preferred/intended environment for running this.
#
#
#   CHANGES
#
# December 2009     - Added a "serial monitor" (target "serial") with
#                     limited support for serial speed autodetection
#                     from the Arduino program.
#                   - Added support for using the "arduino" protocol
#                     in avrdude when available; this eliminates the
#                     need to reset the device with "stty". The old
#                     behaviour can be restored by using the target
#                     "upload_autoreset" instead of "upload".
#                   - Added support for downloading with external
#                     programmers.
#                   - Added basic support for reading configurations
#                     for external programming devices from the
#                     file hardware/programmers.txt, in addition to
#                     the built-in isp and dragon targets. This should
#                     enable the use of parallel programmers.
#                   - Added target "programmers" for listing supported
#                     external programming devices.
#                   - Don't do autoreset when uploading with external
#                     programmers.
#                   - Removed unnecessary debug outputs. 
#                   - Additional documentation in the script file.
# November 2009     - Major bugfix for boards with CPU frequency other
#                     than 16MHz.
#                   - Possibly fixed the __cxa_pure_virtual issue.
#                   - Forcing user to define ARDUINO_BOARD explicitly
#                     since using an incorrect board type can cause
#                     nasty hidden errors.
#                   - Added reset commands to upload and download
#                     when not using the Makefile.
#                   - Added dependency on the board type, i.e. if the
#                     board type is changed, everything gets rebuilt.
#                   - Added target "boards" to list available boards.
#                   - Changed default library path to include the
#                     "~/sketchbook/libraries" directory, similarly to
#                     the current Arduino IDE.
#                   - Made building locally the default and fixed
#                     the problem of dependency files being built in
#                     the core directory.
#                   - Implemented reading configuration from
#                     ~/.ardmake.conf and ardmake.conf in the
#                     sketch directory.
#                   - Fixed build dependencies with Sanguino.
#                   - Rewrote most of the help texts.
#                   - Fixed compatibility with mawk. Thanks to Tom
#                     Parkin for reporting this!
# October 2009      - Support AVRISP and burning bootloaders.
#                   - Support building object files into the
#                     applet directory instead of the core and
#                     library directories.
#                   - Generate automatic dependecies for libraries
#                   - Support uploading specified .hex or .bin
#                     directly without compiling anything
#                   - Support downloading flash memory from
#                     microcontroller to .hex or .bin file
#                   - Replace the slightly broken build target:
#                       - Proper dependencies
#                       - Show correct file name and line numbers for errors
#                       - Display program size compared to controller capacity
# September 2009    - Support Arduino 017
# March 2009        - Support Arduino 014
# February 2009     - Initial version
#
#
#   FANCY ARDUINO DEVICE NODES ON LINUX
#
# The default port for the Arduino is set to "/dev/arduino", which
# requires udev rules (but avoids the problem of changing ttyUSB names).
# Alternatively, it can be changed in this file. The udev rule that
# works for the Arduino clone that I have is this:
#
# KERNEL=="ttyUSB*", ATTRS{product}=="FT232R USB UART", \
# ATTRS{idProduct}=="6001", ATTRS{idVendor}=="0403", \
# SYMLINK+="arduino arduino_$attr{serial}", GROUP="avrprog", MODE="0660"
#
# You will probably want to change the group to "dialout", or create
# the "avrprog" group on your system (like I did). On Ubuntu Linux, place
# the rule in a file inside "/etc/udev/rules.d", e.g. "80-arduino.rules".
#
# If you have many devices with the same product and vendor ids,
# as may be the case with a popular chip like FT232R, you can
# add the condition "ATTRS{serial}" to your udev rules. You can
# see the serial if you first use the above rules and then look at
# the symlink "arduino_SERIAL" where SERIAL is the serial number
# of that particular device. Then create one rule for each of your
# devices' serial numbers (add ATTRS{serial}=="MySerial", right
# before SYMLINK in the above rules).
#
#
#   COMPILER ERROR ABOUT __cxa_pure_virtual
#
# Some versions of Arduino and avr-gcc cause an error about a missing
# function "__cxa_pure_virtual" in programs where C++ classes are used.
# To fix this problem, add the following line anywhere in your program:
#
#   extern "C" void __cxa_pure_virtual() {}
#
###################################################################################
# This script is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License,
# or (at your option) any later version.
#
# This script is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this script.  If not, see <http://www.gnu.org/licenses/>.
###################################################################################
# Read the configuration file (if any):

CONFNAME="ardmake.conf"
for conf in "./$CONFNAME" "$HOME/.$CONFNAME"; do
    if [ -r "$conf" ]; then
        eval "$(awk -v FS== '{ sub(/^[ \t]*/, ""); sub(/^(set|export)[ ]*/, "");
                      if (/^A(RDUINO_|AVR)[A-Za-z0-9_]*=[^;<>`]*$/) {
                          print "[ -z \"$" $1 "\" ] && " $0
                      }
                      next }' "$conf")"
        #echo "Loaded configuration file \"$conf\"."
    fi
done

###################################################################################
# Defaults configuration:

# Path to avr tools (/usr/bin if installed from Linux distribution packages)
[ -z "$AVR_TOOLS_PATH" ] && AVR_TOOLS_PATH=/usr/bin

# Path to avrdude (/usr/bin if installed from Linux distribution packages)
[ -z "$AVRDUDE_PATH" ] && AVRDUDE_PATH=/usr/bin

# Path to search for additional Arduino libraries (separated by : colons).
# The "official" script directory at hardware/libraries is always searched!

if [ -z "$ARDUINO_LIBRARY_PATH" ]; then
    ARDUINO_LIBRARY_PATH="../libraries:$HOME/sketchbook/libraries"
fi

# Try to figure out Arduino install directory (first from environment
# variable ARDUINO_DIR, then ~/arduino, then opt/arduino)
if [ -n "$ARDUINO_DIR" ]; then
    INSTALL_DIR="$ARDUINO_DIR"
else
    INSTALL_DIR="$HOME/arduino"
    if [ ! -x "$INSTALL_DIR/arduino" -a -x '/opt/arduino/arduino' ]; then
        INSTALL_DIR='/opt/arduino'
    fi
fi

# Build locally unless a shared build is specifically requested:
if [ ! "$ARDUINO_BUILD" = "shared" ]; then
    BUILD_LOCALLY=1
else
    BUILD_LOCALLY=''
fi

# The extension for Arduino program files (.pde at the time of writing, but
# this is the same as for Processing - .ade would be more fitting)
EXT='pde'

# Command to reset serial port:
RESET_COMMAND="stty hupcl; sleep 0.1; true"

###################################################################################

basename="$(basename "$0")"

# Check the configuration:

PROGRAMMERFILE="$INSTALL_DIR/hardware/programmers.txt"
BOARDFILE="$INSTALL_DIR/hardware/boards.txt"
if [ ! -r "$BOARDFILE" ]; then
    cat >&2 <<EOF
ERROR: Could not read "$BOARDFILE".

Please set ARDUINO_DIR correctly so that \$ARDUINO_DIR/hardware/boards.txt
is the location of the boards.txt in your Arduino installation.

You can configure ARDUINO_DIR either in the environment, or in the
configuration file ~/.$CONFNAME, e.g.:
    echo ARDUINO_DIR=$HOME/arduino-0017 >>~/.$CONFNAME

Run "$basename help" for instructions.
EOF
    exit 1
fi

[ ! -x "$AVRDUDE_PATH/avrdude" ] && AVRDUDE_PATH="$INSTALL_DIR/hardware/tools"
[ ! -x "$AVRDUDE_PATH/avrdude" ] && AVRDUDE_PATH="$(dirname $(which avrdude))"
if [ ! -x "$AVRDUDE_PATH/avrdude" ]; then
    cat >&2 <<EOF
ERROR: Could not find an executable avrdude!

Please set AVRDUDE_PATH correctly so that \$AVRDUDE_PATH/avrdude is
the correct avrdude executable. If you do not have avrdude installed,
see if it's available in your system packages, e.g. on Ubuntu Linux
you should be able to use:

    sudo apt-get install avrdude
EOF
    exit 1
fi

AVRDUDE_CONFIG="$AVRDUDE_PATH/avrdude.conf"
[ ! -e "$AVRDUDE_CONFIG" ] && AVRDUDE_CONFIG="/etc/avrdude.conf"
[ ! -e "$AVRDUDE_CONFIG" ] && AVRDUDE_CONFIG="$INSTALL_DIR/hardware/tools/avrdude.conf"

[ ! -x "$AVR_TOOLS_PATH/avr-gcc" ] && AVR_TOOLS_PATH="$INSTALL_DIR/hardware/tools"
[ ! -x "$AVR_TOOLS_PATH/AVR_TOOLS" ] && AVR_TOOLS_PATH="$(dirname $(which avr-gcc))"
if [ ! -x "$AVR_TOOLS_PATH/avr-gcc" ]; then
    cat >&2 <<EOF
ERROR: Could not find an executable avr-gcc!

Please set AVR_TOOLS_PATH correctly so that \$AVR_TOOLS_PATH/avr-gcc is
the correct avr-gcc executable. Other avr build tools (binutils, etc)
should be installed at the same location. If you do not have avr-gcc
installed, see if it's available in your system packages, e.g. on
Ubuntu Linux you should be able to use:

    sudo apt-get install gcc-avr
EOF
    exit 1
fi

# Usage:

if [ "$1" = 'help' -o "$1" = '--help' -o "$1" = '-h' ]; then
    cat | less <<EOF
Command-line Arduino programming helper (make and library handler),
copyright (c) 2009 Kimmo Kulovesi <http://arkku.com/>. This script
is provided as free software under GPL with ABSOLUTELY NO WARRANTY.

Usage: $basename [target] [options for Make]

This script provides a command-line build environment for Arduino,
by wrapping the call to Make and setting parameters for it over those
defined in the Arduino Makefile. Supported features include library
autodetection from #include-directives (just like the graphical IDE),
custom library paths, all board types (including custom ones), external
programming devices, downloading programs from the microcontroller, etc.


Setup and installation:
    1) Install Arduino, e.g.:
        wget http://arduino.googlecode.com/files/arduino-0017.tgz
        tar xvzf arduino-0017.tgz; ln -s arduino-0017 arduino
    2) Install avrdude and GCC for AVR, e.g. on Ubuntu & Debian:
        apt-get install avrdude gcc-avr
    3) Configure your Arduino installation directory, e.g.
        export ARDUINO_DIR=/path/to/arduino
    3) Configure your Arduino board, e.g.:
        export ARDUINO_BOARD=diecimila
    4) Configure your Arduino serial port device, e.g.:
        export ARDUINO_PORT=/dev/ttyUSB0

    The variable ARDUINO_BOARD must be set to the short name of the
    board you are using. To list available board types, use the
    command "$basename boards".

    By default, this script attempts to find an Arduino installation
    in ~/arduino and /opt/arduino. If it's neither of these, specify
    the variable ARDUINO_DIR accordingly.

    The serial device defaults to /dev/<corename> (e.g. /dev/arduino), 
    and to /dev/ttyUSB0 if that is not available. A specific port may
    be configured by setting the variable ARDUINO_PORT. Linux admins
    may wish to specify udev rules so that the port device is constant
    (e.g. /dev/arduino); for details on that, see the comments at the top
    of this script file, i.e. "$0".

Configuring variables:
    The configuration variables for this script (as detailed above)
    can be set in the file ~/.$CONFNAME, e.g.:
        echo ARDUINO_BOARD=atmega328 >~/.$CONFNAME

    To override all or part of this global configuration, a
    program-specific configuration file called $CONFNAME can be
    created inside each sketch directory, if desired. Any settings
    found in the sketch directory $CONFNAME take precedence over
    the settings in the user's ~/.$CONFNAME.

    You may also configure any or all of these variables in the
    environment. Variables configured in the environment take
    precedence over those in any configuration file! This allows
    you to specify variables directly on the command-line, e.g.:
        ARDUINO_DIR=~/arduino-0014 $basename

To create and upload an Arduino sketch:
    1) Create a directory for your program ("sketch"), e.g.
        mkdir -p ~/sketchbook/Blink
    2) Create your program .$EXT inside the directory, e.g.:
        cd ~/sketchbook/Blink; vim Blink.$EXT
    3) Compile your program by running this script:
        $basename
    4) After a succesful compilation, upload to your board:
        $basename upload

    Libraries are automatically detected from the #include-directives
    used. The libraries installed together with your Arduino are
    always available. Custom libraries are searched for in the
    directory ~/sketchbook/libraries and in ../libraries (i.e. in
    the directory libraries in the same directory as your sketch
    directory is in).

    The custom library locations can be overridden by specifying
    the variable ARDUINO_LIBRARY_PATH as a colon-separated list of
    directories, e.g.:
        ARDUINO_LIBRARY_PATH=$HOME/arduino_libs:/opt/arduino_libs


There are also other make targets that you may use instead of 
compile (the default) and upload. The target is specified as the first
command-line argument, and it can be any target in the Makefile. Special
targets handled by $basename are:

compile (default):  Compile the applet (.hex file) ready for uploading.
                    Do this first after making changes to your program!

upload:             Upload the applet to the microcontroller. See above
                    about the configuration variable ARDUINO_PORT. Usage:
                        $basename upload

                    To upload a pre-compiled file to the microcontroller,
                    you can specify a filename after upload on the
                    command line. The file must have the extension
                    .hex for Intel hex format, or the extension .bin
                    for raw binary format. For example:
                        $basename upload myprog.hex

isp:
dragon:             Just like "upload", but an AVRISP (or clone) or
                    an AVRDragon device is used to upload instead. These
                    can be used to upload to a stand-alone microcontroller
                    in ISP mode.
                    
                    The AVRDragon is an USB device and the port is
                    autodetected. For AVRISP and clones, the default
                    ports are /dev/avrisp and /dev/ttyUSB0, but the
                    port can be overridden by setting AVRISP_PORT.

programmer:         Like "isp" and "dragon", except the target must
                    be followed by the short name of a programmer
                    defined in hardware/programmers.txt. This allows
                    you to use any external programmer define there, e.g.:
                        $basename programmer parallel

download:           Download the microcontroller's flash memory to
                    the file specified as the next command line
                    parameter. The file name MUST have either the
                    extension .hex for Intel hex format, or the
                    extension .bin for raw binary format. For example:
                        $basename download backup.bin

                    External programmers can be used by specifying
                    "download" after the programmer, e.g.:
                        $basename isp download backup.hex

serial:             Start a serial monitor on the serial port. The port
                    device defaults to the programming port (ARDUINO_PORT),
                    but it can be specified on the command line. The
                    speed can often be autodetected from the program in
                    the current directory if it uses Serial.begin(speed),
                    but the speed defaults to 9600 and can be specified
                    on the command line. Examples:
                        $basename serial
                        $basename serial 19200
                        $basename serial /dev/ttyS0
                        $basename serial /dev/ttyUSB1 2400

boards:             List available board types.
programmers:        List available external programmer types.
coff:               Build an applet .cof file for debugging/etc.
lss:                Build an applet .lss file to show annotated assembler. 


    Targets for burning a bootloader (requires a programming device!):

bootloader:         Program the fuses and burn a bootloader. The
                    filenames and settings are obtained from the
                    file ARDUINO_DIR/harware/boards.txt according
                    to the board type (ARDUINO_BOARD).

                    The bootloader can only be burned with an external
                    programmer. If the settings in boards.txt are not
                    applicable to your programmer device (as is
                    probably the case), you can specify the external
                    programmer at the end of the command line.

                    For example, to burn the ADABoot bootloader for
                    ATMega168 using an AVRISP device, you would set
                    ARDUINO_BOARD="ADABoot168" and then run:
                        $basename bootloader isp

                    You can also follow the bootloader target with
                    a .bin or .hex filename to burn a custom
                    bootloader without entering it into boards.txt, e.g.:
                        $basename bootloader boot.hex programmer parallel

fuses:              Just program the fuses and set the lock bits
                    to unlock.  For example:
                        $basename fuses isp

EOF
    exit 0
fi

# Display list of available board types if requested:

if [ "$1" = "boards" -o "$1" = "programmers" ]; then
    if [ "$1" = "boards" ]; then
        file="$BOARDFILE"
    else
        file="$PROGRAMMERFILE"
    fi
    echo "Available $1 in $file:"
    awk -v FS== '$1 ~ /\.name/ {
        sub(/\.name$/, "", $1)
        printf("\t%-15s\t\"%s\"\n", $1, $2);
    }' "$file"
    if [ "$1" = "boards" ]; then
        cat <<EOF

To configure your board type, set the variable ARDUINO_BOARD
either in the environment or in ~/.$CONFNAME, or in the
file $CONFNAME inside your program's directory.
EOF
    else
        cat <<EOF

To use an external programming device for uploading, you can use
the target "programmer" followed by the device name (as listed above)
instead of "upload", e.g.
    $basename programmer parallel

Also note that $basename has two built-in programming device types:
1) AVRDragon in ISP mode, which can be invoked as:
    $basename dragon

2) AVRISP and clones (the most common third-party device sold online):
    $basename isp

The AVRDragon device requires no port configuration, nor do many of
the programmers typically defined in hardware/programmers.txt. The
serial port for the built-in AVRISP can be defined as AVRISP_PORT,
while others use ARDUINO_PORT (and default to the /dev/<programmer_name>
or /dev/ttyUSB0 if that is not available).
EOF
    fi
    exit 0
fi

# Die if no board type is set:

if [ -z "$ARDUINO_BOARD" ]; then
    cat <<EOF >&2
ERROR: The variable ARDUINO_BOARD must be set to the type of Arduino
board you are using. Accepted values are those appearing in Arduino's
hardware/boards.txt, e.g. "diecimila", "mega", "lilypad", etc.
The names are case-sensitive.

To save a certain board type as your default, put the setting
in ~/.$CONFNAME, e.g.:
    echo ARDUINO_BOARD=diecimila >>~/.$CONFNAME

To configure a project-specific board type, put the setting
in the file $CONFNAME in the sketch directory, e.g.:
    cd ~/sketchbook/MyProg
    echo ARDUINO_BOARD=mega >>$CONFNAME

Run "$basename help" for instructions.
EOF
    exit 1
fi

# Try to read the hardware configuration for this board:

eval $(awk -v FS== -v board="$ARDUINO_BOARD" '$1 ~ /\.name$/ {
                                if (boardname) { exit 0 }
                                sub(/\.name$/, "", $1)
                                if (board == $1 || board == $2) {
                                    boardname = $2
                                    speed=0; core=""; mcu=""; protocol="";
                                    f_cpu=0; lfuse=""; hfuse=""; efuse="";
                                    unlock_bits=""; lock_bits="";
                                    bootloader_dir=""; bootlader_file="";
                                }
                                next
                            }
                            !boardname { next }
                            $1 ~ /\.upload\.protocol$/ { protocol = $2; next }
                            $1 ~ /\.upload\.speed$/ { speed = $2; next }
                            $1 ~ /\.upload\.maximum_size$/ {
                                max_size = $2; next
                            }
                            $1 ~ /\.build\.core$/ { core = $2; next }
                            $1 ~ /\.build\.f_cpu$/ { f_cpu = $2; next }
                            $1 ~ /\.build\.mcu$/ { mcu = $2; next }
                            $1 ~ /\.bootloader\.low_fuses$/ {
                                lfuse = $2; next
                            }
                            $1 ~ /\.bootloader\.high_fuses$/ {
                                hfuse = $2; next
                            }
                            $1 ~ /\.bootloader\.extended_fuses$/ {
                                efuse = $2; next
                            }
                            $1 ~ /\.bootloader\.unlock_bits$/ {
                                unlock_bits = $2; next
                            }
                            $1 ~ /\.bootloader\.lock_bits$/ {
                                lock_bits = $2; next
                            }
                            $1 ~ /\.bootloader\.path$/ {
                                bootloader_dir = $2; next
                            }
                            $1 ~ /\.bootloader\.file$/ {
                                bootloader_file = $2; next
                            }
                            END {
                                if (boardname) {
                                    print "BOARDNAME=\"" boardname "\""
                                    if (speed) {
                                        gsub(/[^0-9]/, "", speed)
                                        print "UPLOAD_RATE=\"" speed "\""
                                    }
                                    if (f_cpu) {
                                        gsub(/[^0-9]/, "", f_cpu)
                                        print "F_CPU=\"" f_cpu "\""
                                    }
                                    if (core) {
                                        gsub(/[^a-zA-Z0-9_.:-]/, "", core)
                                        print "CORE=\"" core "\""
                                    }
                                    if (mcu) {
                                        gsub(/[^a-zA-Z0-9_.:-]/, "", mcu)
                                        print "MCU=\"" mcu "\""
                                    }
                                    if (protocol) {
                                        gsub(/[^a-zA-Z0-9_.:-]/, "", protocol)
                                        print "AVRDUDE_PROGRAMMER=\"" \
                                            protocol "\""
                                    }
                                    if (max_size) {
                                        gsub(/[^0-9]/, "", max_size)
                                        print "MAX_SIZE=\"" max_size "\""
                                    }
                                    if (hfuse != "") {
                                        gsub(/[^0-9xA-Fa-f]/, "", hfuse)
                                        print "BL_HFUSE=\"" hfuse "\""
                                    }
                                    if (lfuse != "") {
                                        gsub(/[^0-9xA-Fa-f]/, "", lfuse)
                                        print "BL_LFUSE=\"" lfuse "\""
                                    }
                                    if (efuse != "") {
                                        gsub(/[^0-9xA-Fa-f]/, "", efuse)
                                        print "BL_EFUSE=\"" efuse "\""
                                    }
                                    if (lock_bits != "") {
                                        gsub(/[^0-9xA-Fa-f]/, "", lock_bits)
                                        print "BL_LOCK=\"" lock_bits "\""
                                    }
                                    if (unlock_bits != "") {
                                        gsub(/[^0-9xA-Fa-f]/, "", unlock_bits)
                                        print "BL_UNLOCK=\"" unlock_bits "\""
                                    }
                                    if (bootloader_dir && bootloader_file) {
                                        gsub(/["]/, "\\\"", bootloader_dir)
                                        gsub(/["]/, "\\\"", bootloader_file)
                                        print "BL_PATH=\"" bootloader_dir "/" \
                                                           bootloader_file "\""
                                    }
                                }
                            }' "$BOARDFILE")

# Die if the board configuration was not found:

if [ -z "$F_CPU" ]; then
    cat <<EOF >&2
ERROR: The board "$ARDUINO_BOARD" was not found in the configuration
file "$BOARDFILE". The variable ARDUINO_BOARD
must be set to the (case-sensitive) short name of the board,
e.g. "diecimila" or "atmega328".

Run "$basename boards" to list known board types, or
"$basename help" for general instructions.
EOF
    exit 1
fi

# Some defaults for board types, e.g. if the user has placed a custom
# board in boards.txt and didn't define everything:

[ -z "$CORE" ] && CORE=arduino
[ -z "$MAX_SIZE" ] && MAX_SIZE=14336
[ -z "$MCU" ] && MCU="$ARDUINO_BOARD"
[ -z "$AVRDUDE_PROGRAMMER" ] && AVRDUDE_PROGRAMMER=stk500v1
[ -z "$UPLOAD_RATE" ] && UPLOAD_RATE=19200
UPLOAD_DELAY=""

# Set some helper variables based on the Arduino location:

MAKEFILE="$INSTALL_DIR/hardware/cores/$CORE/Makefile"
[ ! -e "$MAKEFILE" ] && MAKEFILE="$INSTALL_DIR/hardware/cores/arduino/Makefile"
ARDUINO="$INSTALL_DIR/hardware/cores/$CORE"
LIBRARY_DIR="$INSTALL_DIR/hardware/libraries"

# Check for the wiring_serial.c bug in some versions of Arduino:

if grep -q -s -F 'wiring_serial.c' "$MAKEFILE"; then
    if [ ! -e "$ARDUINO/wiring_serial.c" ]; then
        echo '/* Empty file created due to bug in Arduino Makefile */' \
            >"$ARDUINO/wiring_serial.c"
        if [ ! -e "$ARDUINO/wiring_serial.c" ]; then
            cat <<EOF >&2

WARNING: The file "$ARDUINO/wiring_serial.c" is referred to in
the Makefile, but it does not exist. This is a bug in some Arduino
versions, and will probably lead to failed builds. To remedy, please
create the file (it can be empty) or remove the reference from the
Makefile ("$MAKEFILE").

EOF
        fi
    fi
fi

# Correct the programmer "stk500" specified for pretty much every
# Arduino board to "stk500v1" (which is the correct, more specific
# option for avrdude):
[ "$AVRDUDE_PROGRAMMER" = "stk500" ] && AVRDUDE_PROGRAMMER='stk500v1'

# Configure the programmer port location:

if [ -n "$ARDUINO_PORT" ]; then
    PORT="$ARDUINO_PORT"
else
    PORT="/dev/$CORE"
    if [ ! -e "$PORT" ]; then
        PORT="/dev/$ARDUINO_BOARD"
        if [ ! -e "$PORT" ]; then
            PORT='/dev/avr'
            [ ! -e "$PORT" ] && PORT='/dev/ttyUSB0'
        fi
    fi
fi

# Serial monitor:

if [ "$1" = "serial" ]; then
    shift
    if [ -c "$1" ]; then
        PORT="$1"
        shift
    fi
    if [ ! -e "$PORT" ]; then
        cat >&2 <<EOF
ERROR: Serial port device "$PORT" not found.

You can either specify the port as the variable ARDUINO_PORT, or give an
alternative port on the command line, e.g.:
    $basename serial /dev/ttyUSB1

The speed of the serial port is normally autodetected from typical
programs using the Arduino Serial library, but it can be specified
on the command line, e.g. for 9600 bps:
    $basename serial /dev/ttyUSB0 9600
EOF
        exit 1
    fi
    TARGET="$(basename "$(pwd)").$EXT"
    if [ -n "$1" ]; then
        SPEED="$1"
    elif [ -r "$TARGET" ]; then
        SPEED=$(awk -v baud="${ARDUINO_BAUD:-9600}" '/Serial[0-9]*\.begin/ {
                        sub(/^.*Serial[^0-9]*/, "");
                        sub(/[^0-9].*$/, "");
                        if ($0 != "" && $0 > 0) { baud = $0; exit }
                     }
                     END { print baud }' "$TARGET")
    else
        SPEED="${ARDUINO_BAUD:-9600}"
    fi
    if tty >/dev/null 2>&1; then
        cat >&2 <<EOF
Starting serial monitor on port $PORT at $SPEED bps.
Your input will be sent to the serial port. Press Ctrl-C to stop.

EOF
    fi
    stty -F "$PORT" ospeed "$SPEED" ispeed "$SPEED" \
         cs8 -ignpar -cstopb -hupcl -echo
    cat <"$PORT" &
    catpid=$!
    trap '[ -n "$catpid" ] && kill $catpid; catpid=""' EXIT INT QUIT TERM
    set noclobber 2>/dev/null
    cat >"$PORT"
    exit 0
fi

# Display verification that the correct board was selected:

cat <<EOF
Read settings for ARDUINO_BOARD="$ARDUINO_BOARD":
    $BOARDNAME

EOF

# Configure AVRDUDE here, since the Makefile included with Arduino
# has non-working paths hard-coded:

AVRDUDE_MCU=$(echo "$MCU" | awk '
    $1 ~ /^atmega/ { sub(/^atmega/, "m", $1); print $1; exit }
    $1 ~ /^attiny/ { sub(/^attiny/, "t", $1); print $1; exit }
    $1 ~ /^at90s/ { sub(/^at90s/, "t", $1); print $1; exit }
    $1 ~ /^at90pwm/ { sub(/^at90/, "t", $1); print $1; exit }')

AVRDUDE_FLAGS="-F -D -p $AVRDUDE_MCU -v -v"

# Allow targets "bootloader" and "fuses" for burning the bootloader
# or setting the fuses, respectively, e.g. for preparing a DIY
# Arduino clone with a blank ATMega device.

burn_bootloader=''
program_fuses=''
if [ "$1" = "bootloader" -o "$1" = "fuses" ]; then
    program_fuses='yes'
    [ "$1" = "bootloader" ] && burn_bootloader='yes'
    shift
    [ ! -x "$AVRDUDE_PATH/avrdude" ] && AVRDUDE_PATH=''

    if [ -z "$BL_HFUSE" -o -z "$BL_LFUSE" -o -z "$BL_EFUSE" -o \
         -z "$BL_UNLOCK" -o -z "$BL_PATH" ]
    then
        cat >&2 <<EOF
ERROR: boards.txt did not define the information necessary for burning
a bootloader and/or setting the fuses. You must ensure that the file
$INSTALL_DIR/hardware/boards.txt is available and contains the following
settings for your board type (currently "$ARDUINO_BOARD"):

$ARDUINO_BOARD.bootloader.low_fuses=0x??
$ARDUINO_BOARD.bootloader.high_fuses=0x??
$ARDUINO_BOARD.bootloader.extended_fuses=0x??
$ARDUINO_BOARD.bootloader.unlock_bits=0x??
$ARDUINO_BOARD.bootloader.lock_bits=0x??
$ARDUINO_BOARD.bootloader.file=filename.hex
$ARDUINO_BOARD.bootloader.path=dirname

Aborting...
EOF
        exit 1
    fi
    BOOTLOADER_FILE="$INSTALL_DIR/hardware/bootloaders/$BL_PATH"
    if [ -n "$1" -a -r "$1" ] && echo "$1" | grep -E -q -s '\.(hex|bin)$' ; then
        BOOTLOADER_FILE="$1"
        shift
    elif [ ! -r "$BOOTLOADER_FILE" ]; then
        echo "ERROR: Bootloader file "$BOOTLOADER_FILE" is not readable!" >&2
        exit 1
    fi
    cat <<EOF
This command will set the following:

EOF
    [ -n "$burn_bootloader" ] && echo "Bootloader: $BOOTLOADER_FILE"
    cat <<EOF
Fuses: high=$BL_HFUSE low=$BL_LFUSE extended=$BL_EFUSE

    WARNING!

Burning a bootloader and/or setting the fuse bits is potentially
dangerous and incorrect settings can make your device stop working!
Note that an external programmer is required for this operation,
i.e. you can't burn the bootloader via Arduino's own USB.

Press Return to continue (at your own risk), or Ctrl-C to cancel!

EOF
    read press_enter >/dev/null 2>&1
fi

# Change the target "dragon" to "upload", but perform the upload using
# the AVRDragon in ISP mode instead of the instead of the typical Arduino
# programming method (e.g. for DIY projects using the same microprocessor
# as an Arduino but not having the programming capability themselves).
#
# Similarly change the target "isp" to "upload", but perform the upload
# using an AVRISP (or clone thereof).

if [ -n "$1" ]; then
    if [ "$1" = "dragon" ]; then
        # Uploading with the AVR Dragon:

        AVRDUDE_PROGRAMMER='dragon_isp'
        PORT='usb'
        UPLOAD_RATE=''
        target='upload'
        if [ "$2" = "download" ]; then target="$2"; shift; fi
    elif [ "$1" = "isp" ]; then
        # Uploading via AVRISP with the stk500v2 protocol:
        if [ -n "$AVRISP_PORT" ]; then
            PORT="$AVRISP_PORT"
        elif [ -e '/dev/avrisp' ]; then
            PORT='/dev/avrisp'
        else
            PORT='/dev/ttyUSB0'
        fi
        AVRDUDE_PROGRAMMER='stk500v2'
        UPLOAD_RATE="$AVRISP_BAUD"
        target='upload'
        if [ "$2" = "download" ]; then target="$2"; shift; fi
    elif [ "$1" = "programmer" ]; then
        shift
        AVRDUDE_PROGRAMMER="$1"

        if [ -z "$AVRDUDE_PROGRAMMER" ]; then
            echo "ERROR: No programming device specified on the command-line!" >&2
            exit 1
        fi
        if [ ! -r "$PROGRAMMERFILE" ]; then
            echo "ERROR: Could not read \"$PROGRAMMERFILE\"!" >&2
            exit 1
        fi

        # Read custom configuration for an external programming device:

        eval $(awk -v FS== -v prog="$AVRDUDE_PROGRAMMER" '$1 ~ /\.name$/ {
                        if (progname) { exit 0 }
                        sub(/\.name$/, "", $1)
                        if (prog == $1 || prog == $2) {
                            progname = $2; communication="";
                            protocol=""; delay=""; port="";
                        }
                        next
                    }
                    !progname { next }
                    $1 ~ /\.communication$/ { communication = $2; next }
                    $1 ~ /\.protocol$/ { protocol = $2; next }
                    $1 ~ /\.delay$/ { delay = $2; next }
                    END {
                        if (progname) {
                            print "AVRDUDE_PROGRAMMER_NAME=\"" progname "\""
                            gsub(/[^a-zA-Z0-9_.:-]/, "", communication)
                            print "AVR_COMMUNICATION=\"" communication "\""
                            gsub(/[^0-9]/, "", delay)
                            print "UPLOAD_DELAY=\"" delay "\""
                            if (protocol) {
                                gsub(/[^a-zA-Z0-9_.:-]/, "", protocol)
                                print "AVRDUDE_PROGRAMMER=\"" protocol "\""
                            }
                        }
                    }' "$PROGRAMMERFILE")

        # Die if the specified programmer was not found in programmers.txt:
        if [ -z "$AVRDUDE_PROGRAMMER_NAME" ]; then
            cat >&2 <<EOF
ERROR: "$AVRDUDE_PROGRAMMER" not found in "$PROGRAMMERFILE". You can
view a list of the available programmer types with the command:
    $basename programmers
EOF
            exit 1
        fi

        # Set up the ports according to means of communication:
        if [ "$AVR_COMMUNICATION" = 'usb' ]; then
            PORT='usb'
            UPLOAD_RATE=''
        else
            if [ "$AVR_COMMUNICATION" = 'serial' ]; then
                if [ ! "$PORT" = "$ARDUINO_PORT" -o ! -e "$PORT" ]; then
                    if [ -e "/dev/$AVRDUDE_PROGRAMMER" ]; then
                        PORT="/dev/$AVRDUDE_PROGRAMMER"
                    elif [ ! -e "$PORT" ]; then
                        PORT='/dev/ttyUSB0'
                    fi
                fi
                UPLOAD_RATE="$AVRISP_BAUD"
            else
                # DEBUG: Specifying port for parallel programmers?
                PORT=''
                UPLOAD_RATE=''
            fi
        fi

        target='upload'
        if [ "$2" = "download" ]; then target="$2"; shift; fi
        echo "    Programming device..... $AVRDUDE_PROGRAMMER_NAME"
    elif [ '(' "$1" = "upload" -o "$1" = "download" ')' \
           -a "$AVRDUDE_PROGRAMMER" = "stk500v1" ]
    then
        if "$AVRDUDE_PATH/avrdude" ${AVRDUDE_CONFIG:+-C "$AVRDUDE_CONFIG"} \
            -c list_all 2>&1 | grep -q -s '^ *arduino *= .*conf'; then
            # Use the "arduino" programmer with autoreset built in,
            # if it's available in the avrdude version we are using.
            AVRDUDE_PROGRAMMER='arduino'
            target="$1"
        else
            target="$1_autoreset"
        fi
    else
        target="$1"
    fi
    shift
else
    target='compile'
fi
AVRDUDE_FLAGS="$AVRDUDE_FLAGS${PORT:+ -P $PORT} -c $AVRDUDE_PROGRAMMER${UPLOAD_RATE:+ -b $UPLOAD_RATE}${UPLOAD_DELAY:+ -i $UPLOAD_DELAY}"

# Show the configuration:

cat <<EOF
    Core................... $CORE
    Core directory......... $ARDUINO
    Microcontroller........ $MCU ($AVRDUDE_MCU)
    Clock frequency........ $(echo "$F_CPU" | sed 's/UL$//') Hz
    Programming protocol... $AVRDUDE_PROGRAMMER
    Port................... ${PORT:-(unspecified)}
    Maximum upload size.... ${MAX_SIZE:-?} bytes

EOF

# Program the fuses (usually as the first step for burning a bootloader):

if [ -n "$program_fuses" ]; then
    "$AVRDUDE_PATH/avrdude" ${AVRDUDE_CONFIG:+-C "$AVRDUDE_CONFIG"} \
        $AVRDUDE_FLAGS -e -U "lock:w:$BL_UNLOCK:m" \
        -U "efuse:w:$BL_EFUSE:m" -U "hfuse:w:$BL_HFUSE:m" \
        -U "lfuse:w:$BL_LFUSE:m" || exit 1
    cat <<EOF

Programmed fuses: high=$BL_HFUSE low=$BL_LFUSE extended=$BL_EFUSE
Setting lock bits to unlock: $BL_UNLOCK
EOF
fi

# Burn the bootloader:

if [ -n "$burn_bootloader" ]; then
cat <<EOF

Burning bootloader: $BOOTLOADER_FILE

EOF
    sleep 5
    exec "$AVRDUDE_PATH/avrdude" ${AVRDUDE_CONFIG:+-C "$AVRDUDE_CONFIG"} \
          $AVRDUDE_FLAGS -e -U "flash:w:$BOOTLOADER_FILE:a" -U "lock:w:$BL_LOCK:m"
elif [ -n "$program_fuses" ]; then
    exit 0
fi

# Upload custom file (.hex or .bin) with compiling:

if [ '(' "$target" = "upload" -o "$target" = "upload_autoreset" ')' \
     -a -r "$1" ] && echo "$1" | grep -E -q -s '\.(hex|bin)$' ; then
    echo "Uploading file '$1' to microcontroller..."
    if [ "$target" = "upload_autoreset" ]; then
        ( eval "$RESET_COMMAND" ) <"$PORT" 2>/dev/null
    fi
    exec "$AVRDUDE_PATH/avrdude" ${AVRDUDE_CONFIG:+-C "$AVRDUDE_CONFIG"} \
          $AVRDUDE_FLAGS -U "flash:w:$1:a"
fi

# Download flash to file (.hex or .bin, Intel Hex or raw binary format):

if [ '(' "$target" = "download" -o "$target" = "download_autoreset" ')' \
    -a -n "$1" ] && \
    echo "$1" | grep -E -q -s '\.(hex|bin)$' ; then
    echo "Downloading flash memory to file '$1'..."
    if [ "$target" = "download_autoreset" ]; then
        ( eval "$RESET_COMMAND" ) <"$PORT" 2>/dev/null
    fi
    exec "$AVRDUDE_PATH/avrdude" ${AVRDUDE_CONFIG:+-C "$AVRDUDE_CONFIG"} \
          $AVRDUDE_FLAGS \
          -U "flash:r:$1:$(echo "$1" | sed 's/^.*hex$/i/; s/^.*bin$/r/')"
fi

# Escape AVRDUDE_CONFIG path for the Makefile:

[ -n "$AVRDUDE_CONFIG" ] && AVRDUDE_FLAGS="-C \"$AVRDUDE_CONFIG\" $AVRDUDE_FLAGS"

# Try to discover the program name:

TARGET=$(basename "$(pwd)")
for f in *.$EXT; do
    TARGET=$(echo "$f" | sed "s/\.$EXT$//")
    break
done
if [ ! -e "./$TARGET.$EXT" ]; then
    cat >&2 <<EOF
ERROR: No sketch found! To create a program, make a directory with the
program name, e.g. MyProg, and write the program code inside that
directory in a file with the same name but with the extension ".$EXT".
For example:
    mkdir MyProg; cd MyProg; vim MyProg.$EXT
    $basename

Run "$basename help" for instructions!
EOF
    exit 1
fi

# Figure out what libraries are being used:

LIBRARIES_DIR="\$(INSTALL_DIR)/hardware/libraries"
LIBSRC=''
LIBASRC=''
LIBCXXSRC=''
CINCS=''
CXXINCS='$(CINCS)'
LIBCHECK_FILES=' '

ARDUINO_LIBRARY_PATH=$(echo "$ARDUINO_LIBRARY_PATH" | \
                       sed 's/ /\\ /g; s/[^+-9:=@A-Z_a-z!]//g; s/:/ /g')

echo 'Looking for libraries in these directories:'
for libpath in $ARDUINO_LIBRARY_PATH "$LIBRARY_DIR"; do
    echo "    $libpath/"
done
echo

# Check an included header for matching .c, .cpp and/or .S files
# (simply by filename) and add any of those to the sources.

check_header () {
    local libname="$1"
    local base="$2"
    local inlib="$3"
    local pfx="$base/$libname"
    [ ! -e "$pfx.h" ] && return 1

    check_for_libraries "$pfx.h"

    local makepfx="$pfx"
    if [ "$base" = "$ARDUINO" ]; then
        # Beautify the Arduino directory path
        makepfx="\$(ARDUINO)/$libname"
    elif [ -n "$inlib" ]; then
        # Beautify the Arduino library directory path
        if echo "$base" | grep -q -s -F "$LIBRARY_DIR/$inlib/utility"
        then
            makepfx="\$(LIBRARIES_DIR)/$inlib/utility/$libname"
        elif echo "$base" | grep -q -s -F "$LIBRARY_DIR/$inlib"
        then
            makepfx="\$(LIBRARIES_DIR)/$inlib/$libname"
        fi
    fi

    if [ -e "$pfx.c" ]; then
        check_for_libraries "$pfx.c" "$inlib" && \
            LIBSRC="$LIBSRC $makepfx.c"
    fi
    if [ -e "$pfx.cpp" ]; then
        check_for_libraries "$pfx.cpp" "$inlib" && \
            LIBCXXSRC="$LIBCXXSRC $makepfx.cpp"
    fi
    [ -e "$pfx.S" ] && LIBASRC="$LIBASRC $makepfx.S"

    return 0
}

# Check a file for new libraries we need to include. This is done simply
# by locating the #include-lines in the C/C++ sources. Obviously no
# pre-processor conditionals or such are supported, but for simple purposes
# this seems to work reasonably well. (All examples included with Arduino
# version 013 compile correctly.)

check_for_libraries () {
    [ ! -r "$1" ] && return 1
    if echo "$LIBCHECK_FILES" | grep -q -s -F " |$1| "; then
        return 1
    fi
    LIBCHECK_FILES="${LIBCHECK_FILES}|$1| "
    local basedir=$(dirname "$1")
    local inlib="$2"

    # Note: Print.cpp is a standard dependency for Arduino programs, but
    # the dependency was not included in the official Makefile up to and
    # including version 0014. If this script is used with old versions of
    # Arduino, compilation may fail due to missing Print.cpp. The suggested
    # solution is to update Arduino, but if that is not possible you can
    # add "Print" after the closing ")" on the line before "do":

    for lib in $(awk -F '[<>"]' '/^[ ]*#include [<"]/ { sub(/\.h[p]*$/, "", $2);
                                    gsub(/[^a-zA-Z0-9_.:/-]/, "", $2);
                                    print $2; next }' "$1" 2>/dev/null)
    do
        local found=''
        local libpath=''
        local libname="$lib"
        local header="$ARDUINO/$libname.h"
        local base=''

        for libpath in $ARDUINO_LIBRARY_PATH "$LIBRARY_DIR"; do
            local libdir="$libpath/$libname"

            if [ -e "$libdir" ]; then
                if check_for_libraries "$libdir/$libname.h" "$libname"; then
                    if [ "$libpath" = "$LIBRARY_DIR" ]; then
                        echo "Including Arduino library: $libname"
                        CINCS="$CINCS -I\$(LIBRARIES_DIR)/$libname"
                        [ -e "$libdir/utility" ] && \
                            CINCS="$CINCS -I\$(LIBRARIES_DIR)/$libname/utility"
                    else
                        echo "Including local library: $libname"
                        CINCS="$CINCS -I$libdir"
                        [ -e "$libdir/utility" ] && \
                            CINCS="$CINCS -I$libdir/utility"
                    fi
                fi
                check_header "$libname" "$libdir" "$libname"
                found=1
                break
            fi
        done

        if [ -z "$found" ]; then
            for base in "$ARDUINO" "$basedir" "$basedir/utility"; do
                check_header "$libname" "$base" "$inlib" && break
            done
        fi
    done
    return 0
}

check_for_libraries "$TARGET.$EXT"

# Ensure the applet directory exists:

 [ ! -d applet ] && mkdir applet

if [ -e 'applet/board' -a ! "$BOARDFILE" -nt "applet/board" ]; then
    configured_board="$(head -n 1 'applet/board')"
else
    configured_board=''
fi
[ ! "$configured_board" = "$ARDUINO_BOARD" ] && echo "$ARDUINO_BOARD" >'applet/board'

# Display library settings to the user:

old_CINCS="$CINCS"
CINCS="-I. -I./utility -I\$(ARDUINO)$CINCS"
if [ -n "$old_CINCS" ]; then
    echo
    echo "Includes = $CINCS"
    #[ -n "$LIBSRC" ] && echo "LIBSRC =$LIBSRC"
    #[ -n "$LIBASRC" ] && echo "LIBASRC =$LIBASRC"
    #[ -n "$LIBCXXSRC" ] && echo "LIBCXXSRC =$LIBCXXSRC"
    echo
fi
unset old_CINCS

# Set the compiler options to better match the IDE:

CTUNING='-ffunction-sections -fdata-sections -fshort-enums'
CFLAGS='$(CDEFS) $(CINCS) -O$(OPT) $(CWARN) $(CTUNING) $(CEXTRA) $(CDEBUG)'
CXXFLAGS='$(CDEFS) $(CINCS) -O$(OPT) -fno-exceptions $(CTUNING)'

# Create the Makefile:

if [ ! -e 'applet/Makefile' -o 'applet/board' -nt 'applet/Makefile' \
     -o "$0" -nt 'applet/Makefile' ]; then
    # Change the Make default target to our own:
    echo 'compile: do_compile' >applet/Makefile

    # Take the original Makefile, but remove the built-in dependency
    # includes (so we can override them) and the original .elf target
    # which we are replacing below:
    sed '/^include $[(][^)]*\.d[)]/ d;
         /^applet\/$[(]TARGET[)]\.elf: / d;
         /^[ \t]*#/ d;
         s/\.pde/\.$(EXT)/g' "$MAKEFILE" >>applet/Makefile

    # Now the dirty parts, featuring some rather explicit Make:
    echo -e 'do_compile: do_build show_size
do_build: applet/$(TARGET).hex
applet/$(TARGET).hex: applet/$(TARGET).elf

ARDMAKE_BOARD=applet/board

applet/$(TARGET).elf: applet/$(TARGET).cpp applet/core.a
\t$(CXX) $(ALL_CXXFLAGS) -Wl,--gc-sections $(LDFLAGS) -L. -Lapplet/ -o $@ $< applet/core.a
\t@chmod a-x $@ >/dev/null 2>&1 || true

applet/$(TARGET).cpp: $(TARGET).$(EXT) $(ARDUINO)/main.cxx $(ARDUINO)/WProgram.h $(ARDMAKE_BOARD)
\techo '\''#include "WProgram.h"'\'' >$@
\t@echo '\''#line 1 "$<"'\'' >>$@
\tcat $(TARGET).$(EXT) >>$@
\t@echo '\''#line 1 "$(ARDUINO)/main.cxx"'\'' >>$@
\tcat $(ARDUINO)/main.cxx >>$@

show_size:
\t@echo
\t@echo Program size:
\t@$(HEXSIZE) | awk -v m="$(MAX_SIZE)" '\''{print;if(NR^1){s=$$4}} \\
    END {printf("\\n%d/%d bytes (%.1f%% of capacity, %d bytes left)\\n\\n",\\
    s,m,s*100.0/m,m-s);}'\''

upload_autoreset: do_autoreset upload unreset

do_autoreset:
\t@echo Sending reset to prepare for upload...
\t( '"$RESET_COMMAND"' ) <$(PORT) 2>/dev/null
\t@echo

unreset:
\t@stty -hupcl <$(PORT) 2>/dev/null || true

$(OBJ): $(ARDMAKE_BOARD)
$(DEPS): $(ARDMAKE_BOARD)

$(APPC): applet/%.o: %.c
\t$(CC) -c $(ALL_CFLAGS) -o $@ $<

$(APPCXX): applet/%.o: %.cpp
\t$(CXX) -c $(ALL_CXXFLAGS) -o $@ $<

$(APPA): applet/%.o: %.S
\t$(CC) -c $(ALL_ASFLAGS) -o $@ $<

$(APPC:.o=.d): applet/%.d: %.c
\t$(CC) -M $(ALL_CFLAGS) $< | sed '\''s;^[^:]*:;applet/$*.o applet/$*.d:;'\'' >$@

$(APPCXX:.o=.d): applet/%.d: %.cpp
\t$(CXX) -M $(ALL_CXXFLAGS) $< | sed '\''s;^[^:]*:;applet/$*.o applet/$*.d:;'\'' >$@

$(APPA:.o=.d): applet/%.d: %.S
\t$(CC) -M $(ALL_ASFLAGS) $< | sed '\''s;^[^:]*:;applet/$*.o applet/$*.d:;'\'' >$@

applet/$(TARGET).d: applet/$(TARGET).cpp

vpath %.c applet/ $(sort $(dir $(OBJC)))
vpath %.cpp applet/ $(sort $(dir $(OBJCXX)))
vpath %.S applet/ $(sort $(dir $(OBJA)))

include $(DEPS)' >>applet/Makefile

    # Ensure applet/core.a gets re-built every time, because otherwise
    # we won't get the correct dependencies:
    if [ -z "$target" -o "$target" = "compile" -o "$target" = "all" ]; then
        if [ -w "applet/core.a" ]; then
            echo "rm -f applet/core.a"
            rm -f "applet/core.a"
        fi
    fi
fi

# Don't do autoreset if we don't have a serial port:

[ "$target" = "upload_autoreset" -a ! -c "$PORT" ] && target=upload

# Substitute the Makefile "clean" target:

if [ "$target" = "clean" ]; then
    echo "Cleaning up..."
    for ext in d o cpp h elf hex a s S lss cof; do
        rm -f applet/*.$ext 2>/dev/null
    done
    rm -f applet/Makefile applet/board 2>/dev/null
    # If we are building locally, do not try to clean inside Arduino dir:
    [ -n "$BUILD_LOCALLY" ] && exit 0
fi

# Finally, execute Make:

exec make -f applet/Makefile \
    MAKEFILE='applet/Makefile' LIBRARIES_DIR="$LIBRARIES_DIR" \
    AVRDUDE_FLAGS="$AVRDUDE_FLAGS" AVRDUDE_PROGRAMMER="$AVRDUDE_PROGRAMMER" \
    TARGET="$TARGET" PORT="$PORT" MCU="$MCU" F_CPU="$F_CPU" MAX_SIZE="$MAX_SIZE" \
    AVR_TOOLS_PATH="$AVR_TOOLS_PATH" INSTALL_DIR="$INSTALL_DIR" EXT="$EXT" \
    AVRDUDE_PATH="$AVRDUDE_PATH" UPLOAD_RATE="$UPLOAD_RATE" ARDUINO="$ARDUINO" \
    LIBSRC="$LIBSRC" LIBASRC="$LIBASRC" LIBCXXSRC="$LIBCXXSRC" \
    CINCS="$CINCS" CXXINCS="$CXXINCS" AVRDUDE='$(AVRDUDE_PATH)/avrdude' \
    CTUNING="$CTUNING" CFLAGS="$CFLAGS" CXXFLAGS="$CXXFLAGS" \
    OBJC='$(sort $(SRC:.c=.o) $(abspath $(LIBSRC:.c=.o)))' \
    OBJCXX='$(sort $(CXXSRC:.cpp=.o) $(abspath $(LIBCXXSRC:.cpp=.o)))' \
    OBJA='$(sort $(ASRC:.S=.o) $(abspath $(LIBASRC:.S=.o)))' \
    OBJARDUINODIR='$(OBJC) $(OBJCXX) $(OBJA)' \
    APPC='$(addprefix applet/,$(notdir $(OBJC)))' \
    APPCXX='$(addprefix applet/,$(notdir $(OBJCXX)))' \
    APPA='$(addprefix applet/,$(notdir $(OBJA)))' \
    OBJAPPDIR='$(APPC) $(APPCXX) $(APPA)' \
    OBJ='$(if $(BUILD_LOCALLY),$(OBJAPPDIR),$(OBJARDUINODIR))' \
    DEPS='$(OBJ:.o=.d) applet/$(TARGET).d' LST='$(OBJ:.o=.lst)' \
    $target ${BUILD_LOCALLY:+BUILD_LOCALLY=1} "$@"
