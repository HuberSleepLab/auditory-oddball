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

##########################
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

print(stimuli)

# appropriate labels:
triggerLabels = [0, 0]
# TODO: see with simone if there's a better way
triggerLabels[CONF["stimuli"]["target"]] = "Target"
triggerLabels[CONF["stimuli"]["standard"]] = "Standard"


######################
# loop through stimuli

missingTot = 0

for indx, stimulus in enumerate(stimuli):

    # start trial
    datalog["trialID"] = trigger.sendTriggerId()
    logging.info("Trial: %s", CONF["stimuli"]["tone"][stimulus])

    # play tone
    tones.play(CONF["stimuli"]["tone"][stimulus])
    # this might not even be necessary, double check
    print(triggerLabels[stimulus], CONF["trigger"]["labels"])
    trigger.send(triggerLabels[stimulus])
    # TODO: get pupil size

    # wait a jittered delay
    isi = random.uniform(
        CONF["task"]["ISI"][0], CONF["task"]["ISI"][1])

    isiTimer = core.CountdownTimer(isi)
    keys = []
    missing = True
    logging.info("tone delay of %s", isi)

    while isiTimer.getTime() > 0:
        #  Record any extra key presses during wait
        key = kb.getKeys()
        if key:
            # TODO: make seperate function that also keeps track of q, make q in config
            quitExperimentIf(key[0].name == 'q')
            trigger.send("Response")
            keys.append(key[0])
            missing = False
            missingTot = 0

    # log
    datalog["keyPresses"] = keys
    datalog["condition"] = triggerLabels[stimulus]
    datalog["ISI"] = isi
    # save pupil size! before and after tone

    if missing and stimulus == CONF["stimuli"]["target"]:
        missingTot += 1

        # play alarm if participant hasn't given a response in a while
        if missingTot > CONF["task"]["maxMissing"]:
            Alarm.play()
            trigger.send("ALARM")
            datalog["ALARM!"] = mainClock.getTime()

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
