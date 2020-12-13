import logging
import time

logging.basicConfig(level=logging.DEBUG,filename='testDHT.log', filemode='a', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

try:
    '''
        Try importing Configuration
    '''
    from config import Configuration
    # for DHT Sensor
    DHT_PIN = Configuration['DHT-Pin']

    logging.debug("Importing config file success")

except Exception as error:
    logging.error("Error occured while importing config...",exc_info=True)

try:    
    import Adafruit_DHT
    logging.info("Importing module Adafruit_DHT Success")
    

except Exception as error:
    logging.error("Error occured while importing modules...",exc_info=True)

try:
    DHT_SENSOR = Adafruit_DHT.DHT22
    humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
    if humidity is not None and temperature is not None:
        message = "Initialising and reading from DHT Sensor Success; " + "Temp={}  Humidity={} Neg Pressure={}".format(temperature, humidity)
        logging.info(message)
    else:
        raise ValueError("Failed to Initialise and read data from DHT Sensor..")
        
except Exception as error:
    logging.error("Error occured while reading from DHT ",exc_info=True)