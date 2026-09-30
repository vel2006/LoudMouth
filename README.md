# LoudMouth

By: That1EthicalHacker

LoudMouth is a suite of WiFi attack scripts, ranging from a scanner to attempting to take over the entire network.

## Usage

Using LoudMouth is quite simple, there are two main ways to use it.

The first and most simple is to run the "main.py" file within the project's root directory, this will load all parts of the suite and allow the user to use any.

The second is explained more indepth later within this README, in this way you run the file(s) within each tool's directory.
As an example, the scanner would be found under the 'Scanner' directory and is called 'scanner.py'.

The third and final way is to use the files like modules within Python, which this suite was designed around.

## Design

This project was designed so that you can take the file / module and use it within an automation Python script or any other script / program.

However each file / module also works by itself, meaning you do not need to run the main LoudMouth script to use any part of the suite as outlined within the "Usage" section.

The reason for this, is because different parts of the suite will use each other, this also allows for the script to work well with other scripts indirectly.

## Files / modules

As a useful note, this README / documentation will at times be technical and at other times be very high level.

It is recommended that you, the reader, learn the basics of both wired and wireless networking, as both will be covered within this suite.

However due to the nature of WiFi, most of the script and documentation with be a layer 2, with hints of layer 3 so don't fear if you are not CCIE certified.

While in most scripts there is a check for NetworkManager and it's random MAC address assignment, it is recomended that you disable it yourself as to be sure, below are steps to do exactly that.

1) Open /etc/NetworkManager/NetworkManager.conf

2) Find or add Device section (declared as [device])

3) Append "wifi.scan-rand-mac-address=no"

4) Save file and restart NetworkManager

It should also be noted that this suite is designed to work on UNIX or UNIX based systems (Linux, MacOS, BSD). There is no testing done on Windows, meaning you should assume it does not work on this platform.

### Utils

This is nothing more than a file for handling lots of the repeatable code.

It can't be ran like a normal module for LoudMouth, instead modules call functions within the Utils file.

### Scanner

Scanner is the most basic of all the tools within this suite, it is also the first that was developed as everything else is built off of it.

Scanner works by sniffing a WiFi interface's traffic to find Broadcast frames, these are then saved and used as a way to log nearby networks.

## Modules To Come

Drop      - Deauth entire target network

Twin      - Converts the target interface into an evil twin

List      - Create a list of every client and AP on target network

Surf      - Deauth every network

Halt      - Deauth spesific client devices

Takeover  - Attempts to take over a target network via ARP poisoning

Invisible - Deauth only IP cameras

Eavesdrop - Attempts to decrypt data sent on a network if outdated encryption is used
