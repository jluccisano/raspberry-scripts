#!/usr/bin/python
#import RPi.GPIO as GPIO
import logging
import datetime
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.clock import Clock
from kivy.properties import BooleanProperty, StringProperty
from kivy.lang import Builder


LOG_FORMAT = ('%(levelname) -10s %(asctime)s %(name) -30s %(funcName) '
              '-35s %(lineno) -5d: %(message)s')
LOGGER = logging.getLogger(__name__)


Builder.load_string("""
<MainLayout>:
    Spinner:
        text: 'Select Zone'
        values: ['Zone A', 'Zone B', 'Zone C', 'Zone D']
    Button:
        id: startButton
        text: 'Start'
        on_press: root.toggle()
    AnchorLayout:
        Label:
            text: "%s:%s" % (root.minutes, root.seconds)
            font_size: 120
""")
class MainLayout(GridLayout):

    #logging.basicConfig(filename='/var/log/gpio/sprinkler.log',level=LOGGER.DEBUG,format='%(asctime)s %(message)s')

    minutes = StringProperty()
    seconds = StringProperty()
    running = BooleanProperty(False)

    def __init__(self):
        super(MainLayout, self).__init__()
        self.cols = 2
        self.delta = datetime.datetime.now()+datetime.timedelta(0, 60*5)
        self.update()

    def toggle(self):
        if self.running:
            print('stop zone: %s')
            self.stop()
        else:
            print('start zone: %s')
            self.start()

    def start(self):
        if not self.running:
            self.running = True
            Clock.schedule_interval(self.update, 0.05)
            print("start scheduling")

    def stop(self):
        if self.running:
            self.running = False
            Clock.unschedule(self.update)

    def update(self, *kwargs):
        delta = self.delta - datetime.datetime.now()
        self.minutes, seconds = str(delta).split(":")[1:]
        self.seconds = seconds[:5]

        if int(self.minutes) == 0:
            if int(self.seconds.split(".")[0]) == 0:
                if int(self.seconds.split(".")[1]) < 20:
                    self.seconds = "00.00"
                    self.button.background_color = (1,0,0,1)
                    self.stop()

'''
    class GPIO():

    def __init__(self, **kwargs):
        super(GPIO, self).__init__(**kwargs)

        logging.basicConfig(filename='/var/log/gpio/sprinkler.log',level=LOGGER.DEBUG,format='%(asctime)s %(message)s')

        LOGGER.info('version: %s' , GPIO.VERSION)
        LOGGER.info('revision: %s' ,  GPIO.RPI_INFO['P1_REVISION'])

        #init
        GPIO.setmode(GPIO.BOARD)
        chan_list = [11,12,13,14] #list of output pin
        GPIO.setup(chan_list, GPIO.OUT, initial=GPIO.LOW)


    def toggleOuput(self, outputNumber):
        GPIO.output(outputNumber, not GPIO.input(outputNumber))

    def cleanup(self):
        LOGGER.info('Cleanup')
        GPIO.cleanup()
'''

class SprinklerControl(App):


    def build(self):
        return MainLayout()


if __name__ == '__main__':
    SprinklerControl().run()