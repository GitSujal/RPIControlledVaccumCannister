import logging
import time
logging.basicConfig(level=logging.DEBUG,filename='testLCD.log', filemode='a', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


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

    import ST7789 as ST7789
    logging.info('Importing LCD module Success')

except Exception as error:
    logging.error("Error occured while importing LCD module",exc_info=True)

try:
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
    
    from PIL import Image
    image_file = "/home/pi/Final/tick.png"

    # Load an image.
    print('Loading image: {}...'.format(image_file))
    image = Image.open(image_file)

    # Resize the image
    image = image.resize((WIDTH, HEIGHT))

    # Draw the image on the display hardware.
    print('Drawing image')

    disp.display(image)
    logging.info("Displaying image successful")
    time.sleep(10)


except Exception as error:
    logging.error("Error occured while displaying image in LCD module...",exc_info=True)