import logging
import os
import random
import time
import datetime
import sys
import math
import itertools

from screen import Screen
from scorer import Scorer
from trigger import Trigger
from tones import Tones
from datalog import Datalog

from capturePupil import CapturePupil as cp
from psychopy import core, event, sound
from psychopy.hardware import keyboard


from config.configOdball import CONF

#########################################################################

######################################
# Initialize screen, logger and inputs

logging.basicConfig(
    level=CONF["loggingLevel"],
    format='%(asctime)s-%(levelname)s-%(message)s',
)  # This is a log for debugging the script, and prints messages to the terminal

screen = Screen(CONF)

datalog = Datalog(OUTPUT_FOLDER=os.path.join(
    'output', datetime.datetime.now(
    ).strftime("%Y-%m-%d")), CONF=CONF)  # This is for saving data

kb = keyboard.Keyboard()

mainClock = core.MonotonicClock()  # starts clock for timestamping events

#Alarm = sound.Sound(os.path.join('sounds', CONF["sounds"]["alarm"]),
                    #stereo=True)
scorer = Scorer()

trigger = Trigger(CONF["trigger"]["serial_device"],
                  CONF["sendTriggers"], CONF["trigger"]["labels"])

tones = Tones(CONF)

if CONF["version"] == "main":
    pupil = cp()  # TODO: find a better way!

logging.info('Initialization completed')

#########################################################################

 

##############
# Introduction
##############
tones.instructions("fixation", 0)
#tones.play(CONF["stimuli"]["tone"][1])
core.wait(1)


####################
# Fixation eyes open
####################
