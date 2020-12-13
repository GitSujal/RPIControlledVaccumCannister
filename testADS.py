import logging
import time
logging.basicConfig(level=logging.DEBUG,filename='testADS.log', filemode='a', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

try:
    from config import Configuration
    channel = Configuration['CHANNEL']
    logging.debug("Importing Config success")

    from ads1015 import ADS1015
    logging.debug("Importing ADS1015 Success")

    ads1015 = ADS1015()
    ads1015.set_mode('single')
    ads1015.set_programmable_gain(Configuration['ADS-Gain'])
    ads1015.set_sample_rate(Configuration['Sample-Rate'])
    reference = ads1015.get_reference_voltage()
    logging.debug("Initialising ADS1015 Success")    
    while True:   
        value = ads1015.get_compensated_voltage(channel=channel, reference_voltage=reference)
        if value is not None:
            str = "Read Value Successfully: The value is {}".format(value)
            logging.info(str)
            print(str)
        else:
            raise ValueError("Error Initialising ADS1015 for vaccum sensor")
        time.sleep(0.5)

except Exception as e:
    logging.error("Error in process: ",exc_info=True)
