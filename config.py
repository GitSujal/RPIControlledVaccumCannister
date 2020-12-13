'''
    Check the pin numbers from the schematic and update here.
'''
Configuration={
    "Font Size":25,
    'Scaling Factor':50,
    "Left-Top-Coordinate":(10,10),
    "Left-Bottom-Coordinate":(10,425),
    "Right-Top-Coordinate":(270,10),
    "Right-Bottom-Coordinate":(270,425),
    
    "Left-Top-Coordinate-Text":(10,50),
    "Left-Bottom-Coordinate-Text":(10,450),
    "Right-Top-Coordinate-Text":(270,50),
    "Right-Bottom-Coordinate-Text":(270,450),

    "Left-Top":"Temperature",
    "Right-Top":"Humidity",
    "Left-Bottom":"Neg Pressure",
    "Right-Bottom":"",

    "Left-Top-Unit":"*c",
    "Right-Top-Unit":"%",
    "Left-Bottom-Unit":"psi",
    "Right-Bottom-Unit":"",

    "ADS-Gain":2.048,
    "CHANNEL":'in0/ref',
    "Sample-Rate":1600,
    "DHT-Pin":4,

    "PressureLowerBound":7,
    "PressureUpperBound":11,
    "multiplier":11.84,
}