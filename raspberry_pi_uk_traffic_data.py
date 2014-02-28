# raspberry_pi_uk_traffic_data.py

from __future__ import print_function
import xml.etree.ElementTree as etree
import webbrowser
import urllib
import RPi.GPIO as GPIO
import time
import sys

GreenLED = 21
YellowLED = 18
RedLED = 17
MaxDelta = -1000000
YellowMin = 120
RedMin = 300

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(GreenLED, GPIO.OUT)
GPIO.setup(YellowLED, GPIO.OUT)
GPIO.setup(RedLED, GPIO.OUT)

GPIO.output(GreenLED, True)
time.sleep(0.25)
GPIO.output(GreenLED, False)
GPIO.output(YellowLED, True)
time.sleep(0.25)
GPIO.output(YellowLED, False)
GPIO.output(RedLED, True)
time.sleep(0.25)
GPIO.output(RedLED, False)

ns = '{http://datex2.eu/schema/1_0/1_0}'

sections_of_interest = [ 'Section10225', 'Section10711', 'Section10187'  ]
section_descriptions = { 'Section10225' : 'A404 - M4 J8/9 to M40 J4',
                         'Section10711' : 'M4 J8/9 (A404) to J13 (A34)',
                         'Section10187' : 'M40 J4 (A404) to J9 (A34)' }

def FindMaxDelta( Del, MaxDel ):
    if Del > MaxDelta:
        return Del
    else:
        return MaxDel

while True:
    u = urllib.urlopen('http://hatrafficinfo.dft.gov.uk/feeds/datex/England/JourneyTimeData/content.xml')
    tree = etree.parse(u)

    # tree = etree.parse('JourneyTimeData_20140214_1647.xml')

    MaxDelta = -1000000
    GPIO.output(GreenLED, False)
    GPIO.output(YellowLED, False)
    GPIO.output(RedLED, False)

    for elaboratedData in tree.iter(ns + 'elaboratedData'):
        for predefinedLocationReference in elaboratedData.iter(ns + 'predefinedLocationReference'):
            if predefinedLocationReference.text in sections_of_interest:
                for travelTime in elaboratedData.iter(ns + 'travelTime'):
                    travelTimestr = travelTime.text
                    travelTimef = float( travelTime.text )
                for freeFlowTravelTime in elaboratedData.iter(ns + 'freeFlowTravelTime'):
                    freeFlowTravelTimestr = freeFlowTravelTime.text
                for normallyExpectedTravelTime in elaboratedData.iter(ns + 'normallyExpectedTravelTime'):
                    normallyExpectedTravelTimestr = normallyExpectedTravelTime.text
                    normallyExpectedTravelTimef = float( normallyExpectedTravelTime.text )
                freeFlowTravelTime = elaboratedData.iter(ns + 'freeFlowTravelTime')
                normallyExpectedTravelTime = elaboratedData.iter(ns + 'normallyExpectedTravelTime')
                travelTimef = float( travelTime.text )
                
                Delta = travelTimef - normallyExpectedTravelTimef
                print( '***************************' )
                print( section_descriptions[ predefinedLocationReference.text ] )
                print( '***************************' )
                print( 'Current time : ' + travelTimestr + ' seconds' )
                print( 'Freeflow time: ' + freeFlowTravelTimestr + ' seconds' )
                print( 'Expected time: ' + normallyExpectedTravelTimestr + ' seconds' )
                if travelTimef != -1:
                    print( 'Delta (Current - Expected): ' + str(Delta) + ' seconds' )
                    MaxDelta = FindMaxDelta(Delta, MaxDelta)
                print( '***************************' )

    print( 'Max Delta: ' + str(MaxDelta) )

    for publicationTime in tree.iter(ns + 'publicationTime'):
        date_str = publicationTime.text[ : publicationTime.text.find('T') ]
        time_str = publicationTime.text[ publicationTime.text.find('T') + 1 : -1 ]
        print( 'Updated: ' + time_str + ' ' + date_str )

    for periodDefault in tree.iter(ns + 'periodDefault'):
        print( 'Update frequency: ' +  periodDefault.text + ' seconds' )

    if MaxDelta > RedMin:
        GPIO.output(RedLED, True)
    elif MaxDelta > YellowMin:
        GPIO.output(YellowLED, True)
    else:
        GPIO.output(GreenLED, True)

    if float(periodDefault.text) >= 1.0:
        secondsToUpdate = float(periodDefault.text)
        while secondsToUpdate > 0.0:
            print( 'Next update in ' + str(secondsToUpdate) + ' seconds   ', end='\r' )
            sys.stdout.flush()
            secondsToUpdate -= 1.0
            time.sleep( 1 )

    print( "Updating now...                 " )
