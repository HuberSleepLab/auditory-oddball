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
from psychopy import core, event, sound
from psychopy.hardware import keyboard

from datalog import Datalog
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

Alarm = sound.Sound(os.path.join('sounds', CONF["sounds"]["alarm"]),
                    stereo=True)
scorer = Scorer()

trigger = Trigger(CONF["trigger"]["serial_device"],
                  CONF["sendTriggers"], CONF["trigger"]["labels"])

tones = Tones(CONF)
logging.info('Initialization completed')

#########################################################################


def quitExperimentIf(shouldQuit):
    "Quit experiment if condition is met"

    if shouldQuit:
        trigger.send("Quit")
        scorer.getScore()
        logging.info('quit experiment')
        sys.exit(2)


def onFlip(stimName, logName):
    "send trigger on flip, set keyboard clock, and save timepoint"
    trigger.send(stimName)
    kb.clock.reset()  # this starts the keyboard clock as soon as stimulus appears
    datalog[logName] = mainClock.getTime()


##############
# Introduction
##############


# Display overview of session
screen.show_overview()
core.wait(CONF["timing"]["overview"])

# Optionally, display instructions

# if CONF["showInstructions"]:
#     screen.show_instructions()
#     key = event.waitKeys()
#     quitExperimentIf(key[0] == 'q')

# # Blank screen for initial rest
# screen.show_blank()
# logging.info('Starting blank period')

# trigger.send("StartBlank")
# core.wait(CONF["timing"]["rest"])
# trigger.send("EndBlank")

# # Cue start of the experiment
# screen.show_cue("START")
# trigger.send("Start")
# core.wait(CONF["timing"]["cue"])


#################
# Main experiment
#################

screen.show_blank()
core.wait(1)

# establish pool of trials
totTargets = math.floor(CONF["task"]["percentTarget"]
                        * CONF["task"]["totTrials"])

targets = [CONF["stimuli"]["target"]] + \
    [(CONF["stimuli"]["standard"])] * \
    CONF["task"]["minTargetGap"]  # little list of target and padding


totStandards = CONF["task"]["totTrials"] - totTargets * \
    len(targets)  # remaining standard elements

allStimuli = [targets, ] * \
    totTargets, [[CONF["stimuli"]["standard"], ]]*totStandards  # list of lists
# TODO: get rid of this extra step at some point
allStimuli = list(itertools.chain(*allStimuli))
random.shuffle(allStimuli)  # randomize
stimuli = list(itertools.chain(*allStimuli))  # restore as a single list

for indx, stimulus in enumerate(stimuli):
    tones.play(CONF["stimuli"]["tones"][stimulus])
    trigger.send("Stim")  # this might not even be necessary, double check

    isi = random.uniform(
        CONF["tones"]["minTime"], CONF["tones"]["maxTime"])
    isiTimer = core.CountdownTimer(isi)
    extraKeys = []
    logging.info("tone delay of %s", isi)
    while isiTimer.getTime() > 0:

        #  Record any extra key presses during wait
        key = kb.getKeys()
        if key:
            # TODO: make seperate function that also keeps track of q, make q in config
            quitExperimentIf(key[0].name == 'q')
            trigger.send("BadResponse")
            extraKeys.append(mainClock.getTime())

            # Flash the fixation box to indicate unexpected key press
            screen.flash_fixation_box()
        # TODO: save response not extra keys!


# TODO: make trigger timing exact!

###########
# Concluion
###########

# End main experiment
screen.show_cue("DONE!")
trigger.send("End")
core.wait(CONF["timing"]["cue"])

# Blank screen for final rest
screen.show_blank()
logging.info('Starting blank period')

trigger.send("StartBlank")
core.wait(CONF["timing"]["rest"])
trigger.send("EndBlank")


logging.info('Finished')
scorer.getScore()
trigger.reset()
