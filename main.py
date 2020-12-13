from Final.config import Configuration
from PIL import Image, ImageDraw, ImageFont
import random
import logging
import sys

import time
from datetime import datetime
import RPi.GPIO as GPIO           # import RPi.GPIO module  
GPIO.setmode(GPIO.BCM)            # choose BCM or BOARD  
  


def produceImage(backgroundImage="/home/pi/Final/cool-background.png",arrowImage="/home/pi/Final/Arrow.png",Configuration=None,Readings=None,prevRotation=0):
    
    # get an image
    background = Image.open(backgroundImage).convert("RGBA")
    background=background.resize((480,480))

    # get the rotating arrow
    arrow = Image.open(arrowImage).convert("RGBA")

    arrow = arrow.rotate(prevRotation)

    arrow = arrow.resize((160,160))

    # Merging background and the logo
    background.paste(arrow,(160,160),arrow)

    # get a font
    fnt = ImageFont.truetype("/home/pi/Final/FreeMono.ttf",Configuration["Font Size"])
    # get a drawing context
    d = ImageDraw.Draw(background)

    if Configuration is not None:
        d.text(Configuration['Left-Top-Coordinate'],Configuration['Left-Top'],font=fnt,fill=(255,255,255))
        d.text(Configuration['Left-Bottom-Coordinate'],Configuration['Left-Bottom'],font=fnt,fill=(255,255,255))
        d.text(Configuration['Right-Top-Coordinate'],Configuration['Right-Top'],font=fnt,fill=(255,255,255))
        d.text(Configuration['Right-Bottom-Coordinate'],Configuration['Right-Bottom'],font=fnt,fill=(255,255,255))

    if Readings is not None:
        if Configuration["Left-Top"]!="":
            leftTopText = str(round(Readings[Configuration["Left-Top"]],2))+str(Configuration["Left-Top-Unit"])
            d.text(Configuration["Left-Top-Coordinate-Text"],leftTopText,font=fnt,fill=(255,255,255))
        if Configuration["Left-Bottom"]!="":
            leftBottomText = str(round(Readings[Configuration["Left-Bottom"]],2))+str(Configuration["Left-Bottom-Unit"])
            d.text(Configuration["Left-Bottom-Coordinate-Text"],leftBottomText,font=fnt,fill=(255,255,255))
        if Configuration["Right-Top"]!="":
            RightTopText = str(round(Readings[Configuration["Right-Top"]],2))+str(Configuration["Right-Top-Unit"])
            d.text(Configuration["Right-Top-Coordinate-Text"],RightTopText,font=fnt,fill=(255,255,255))
        if Configuration["Right-Bottom"]!="":
            RightBottomText = str(round(Readings[Configuration["Right-Bottom"]],2))+str(Configuration["Right-Bottom-Unit"])
            d.text(Configuration["Right-Bottom-Coordinate-Text"],RightBottomText,font=fnt,fill=(255,255,255))

    return background

def main(logging, returnImage=False):

    try:
        '''
            Try importing Configuration
        '''
        from config import Configuration

        # for DHT Sensor
        DHT_PIN = Configuration['DHT-Pin']

        # For Ads1015
        CHANNEL = Configuration['CHANNEL']

        # For Vaccum Pump
        GPIO.setup(Configuration["Vaccum-Pump-Pin"], GPIO.OUT) # set a port/pin as an output 

        if DHT_PIN is not None and CHANNEL is not None:
            logging.info("Importing config file success")
        else:
            raise ValueError("Error with Config file..")

    except Exception as error:
        logging.error("Error occured while importing module...",exc_info=True)
    
    try:

        import ST7789 as ST7789
        logging.info('Importing LCD module Success')

        # For Display
        # Create ST7789 LCD display class.
        disp = ST7789.ST7789(
            port=0,
            cs=ST7789.BG_SPI_CS_FRONT,  # BG_SPI_CSB_BACK or BG_SPI_CS_FRONT
            dc=9,
            backlight=19,               # 18 for back BG slot, 19 for front BG slot.
            spi_speed_hz=80 * 1000 * 1000
            )
        # Initialize display.
        WIDTH = disp.width
        HEIGHT = disp.height
        disp.begin()
        logging.info("Initialising Display Successful")
  

    except Exception as error:
        logging.error("Error occured while Initialising LCD module...",exc_info=True)

    try:    
        import Adafruit_DHT
        logging.info("Importing module Adafruit_DHT Success")

        DHT_SENSOR = Adafruit_DHT.DHT22
        humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
        if humidity is not None and temperature is not None:
            logging.info("Initialising and reading from DHT Sensor Success")
        else:
            ValueError("Failed to Initialise and read data from DHT Sensor..")
        
    except Exception as error:
        logging.error("Error occured while importing modules...",exc_info=True)

    try:
        from ads1015 import ADS1015
        logging.info("Importing module ads1015 for Vaccum Sensor Success..")

        ads1015 = ADS1015()
        ads1015.set_mode('single')
        ads1015.set_programmable_gain(Configuration['ADS-Gain'])
        ads1015.set_sample_rate(Configuration['Sample-Rate'])
        reference = ads1015.get_reference_voltage()

        value = ads1015.get_compensated_voltage(channel=CHANNEL, reference_voltage=reference)
        
        if value is not None:
            logging.info("Initialising ADS1015 For Vaccum Sensor Success")
        else:
            raise ValueError("Error Initialising ADS1015 for vaccum sensor")

    except Exception as error:
        logging.error("Error occured while importing modules...",exc_info=True)


    goOn = True
    startMotor = False

    while goOn:
        try:
            humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
            if humidity is None or temperature is None:
                raise ValueError("Error reading values from DHT...")
        
        except:
            logging.error("Failed to read data from temp sensor using dummy values",exc_info=True)
            humidity = 0.9
            temperature=30.92
            
        try:
            
            negPressure = ads1015.get_compensated_voltage(channel=CHANNEL, reference_voltage=reference)
            if negPressure is None:
                raise ValueError('Failed ot read data from Vaccum Sensor')

        except:
            logging.error("Failed to read data from vaccum sensor using dummy values",exc_info=True)
            negPressure = 1.5
            goOn=False

        Readings ={
                "Temperature":temperature,
                "Humidity":humidity,
                "Neg Pressure":negPressure*Configuration["multiplier"]
            }
        logging.info("Temp={}  Humidity={} Neg Pressure={}".format(temperature, humidity,negPressure))
        if negPressure>=Configuration['PressureUpperBound']:
            startMotor = True
            GPIO.output(Configuration["Vaccum-Pump-Pin"], 1)       # set port/pin value to 1/GPIO.HIGH/True  
        if negPressure<=Configuration['PressureLowerBound']:
            startMotor = False
            GPIO.output(Configuration["Vaccum-Pump-Pin"], 0)       # set port/pin value to 0/GPIO.LOW/False 


        arrowRotation=0

        if startMotor:
            arrowRotation=(arrowRotation+10)%360            

        image = None

        try:
            image=produceImage(prevRotation=arrowRotation,Configuration=Configuration,Readings=Readings)
            image.save("Image.png")
            logging.info("Image Produced Successfully")

            if WIDTH is not None and HEIGHT is not None:
                image = image.resize((WIDTH,HEIGHT))
            else:
                image = image.resize((480,480))

            disp.display(image) 
        except:
            logging.error("Error producing or displaying image",exc_info=True)
            goOn=False
        
        time.sleep(1)
        if returnImage:
            return image


if __name__ == "__main__":
    if len(sys.argv)>1 and sys.argv[1]=="-d":
        logging.basicConfig(level=logging.DEBUG,filename='main_app_debug.log', filemode='a', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        logging.info("Starting App in debug mode, everything gets logged")
        main(logging=logging,returnImage=True)
    else:
        logging.basicConfig(level=logging.ERROR,filename='main_app.log', filemode='a', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        logging.info("Starting App in normal model only errors gets logged")
        main(logging=logging)

