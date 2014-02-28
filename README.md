Raspberry_Pi_UK_Traffic_Data
============================

Python script for the Raspberry Pi to read live traffic information for UK roads and report current and expected journey times.

As part of the UK government's open data initiative a number of datasets relating to traffic are published. One such dataset contains regularly updated journey information for sections of the UK's motorways and major roads network. This dataset provides, per road section, the current journey time, expected journey time and freeflow journey time in seconds.

This Raspberry Pi Python program reads this journey time feed and displays the information for pre-selected road sections and then lights one of 3 LEDS (red, orange or green) depending on the worst case delta between the expected journey time and the current journey time for all sections of interest.

The program is run from a terminal window using:

sudo python raspberry_pi_uk_traffic_data.py

The feed also supplies the update rate for the dataset, typically 300 seconds, and so the program waits for this time to elapse before running again. A coutdown to the next update is given.

Information on the feeds can be found at:

http://data.gov.uk/dataset/live-traffic-information-from-the-highways-agency-road-network

The program as supplied monitors 3 sections of the UK road network. The sections that are monitored are controlled by the below list:

sections_of_interest = [ 'Section10225', 'Section10711', 'Section10187'  ]

More human friendly descriptions are contained in the dictionary initialised as shown below:

section_descriptions = { 'Section10225' : 'A404 - M4 J8/9 to M40 J4',
                         'Section10711' : 'M4 J8/9 (A404) to J13 (A34)',
                         'Section10187' : 'M40 J4 (A404) to J9 (A34)' }

It is expected that the user will want to monitor different road sections. The section names and descriptions along with lat/lon data can be obtained from the feed below:

http://hatrafficinfo.dft.gov.uk/feeds/datex/England/PredefinedLocationJourneyTimeSections/content.xml

As with the journey time feed the data is contained within an XML file. A simple text search in an editor is all that is needed to find the roads and sections of interest which can then be placed in the list and dictionary.

The pins used for the LEDs can easily be modified by changing the code shown below:

GreenLED = 21
YellowLED = 18
RedLED = 17

The thresholds, in seconds, for turning on the various LEDs are contained in:

YellowMin = 120
RedMin = 300

I have used this program on my Raspberry Pi sat on my desk at work as a visual warning of delays on my journey home.
