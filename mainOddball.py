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

from pupil_labs import PupilCore
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

# needs to be first, so that if it doesn't succeed, it doesn't freeze everything
eyetracker = PupilCore(ip=CONF["pupillometry"]
                       ["ip"], port=CONF["pupillometry"]["port"], shouldRecord=CONF["recordEyetracking"])

trigger = Trigger(CONF["trigger"]["serial_device"],
                  CONF["sendTriggers"], CONF["trigger"]["labels"])

screen = Screen(CONF)

datalog = Datalog(OUTPUT_FOLDER=os.path.join(
    'output', CONF["participant"] + "_" + CONF["session"], datetime.datetime.now(
    ).strftime("%Y-%m-%d")), CONF=CONF)  # This is for saving data

kb = keyboard.Keyboard()

mainClock = core.MonotonicClock()  # starts clock for timestamping events

alarm = sound.Sound(os.path.join('sounds', CONF["sounds"]["alarm"]),
                    stereo=True)
scorer = Scorer()

tones = Tones(CONF)

logging.info('Initialization completed')

#########################################################################


def quitExperimentIf(shouldQuit):
    "Quit experiment if condition is met"

    if shouldQuit:
        trigger.send("Quit")
        scorer.getScore()
        logging.info('quit experiment')
        trigger.reset()
        eyetracker.stop_recording()
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
if CONF["showInstructions"]:
    screen.show_instructions()
    key = event.waitKeys()
    quitExperimentIf(key[0] == 'q')


# Cue start of the experiment
screen.show_cue("START")
trigger.send("Start")
core.wait(CONF["timing"]["cue"])

screen.show_blank()
core.wait(1)


####################
# Fixation eyes open
####################


if CONF["includeRest"]:
    # start recording and set destination folder
    eyetracker.start_recording(os.path.join(
        CONF["participant"], CONF["session"], "fixation"))

    # give starting instructions
    tones.instructions("fixation", 0)

    trigger.send("StartFix")
    fixationTimer = core.CountdownTimer(CONF["fixation"]["duration"])
    logging.info("starting fixation")
    pupilSizes = []
    while fixationTimer.getTime() > 0:
        #  Record any extra key presses during wait
        key = kb.getKeys()
        if key:
            quitExperimentIf(key[0].name == 'q')

        pupilSizes.append(
            [eyetracker.getPupildiameter(), mainClock.getTime()])
        core.wait(1)

    trigger.send("StopFix")
    tones.instructions("fixation", 1)

    datalog["pupilSizesFixation"] = pupilSizes
    datalog.flush()

    # wait for keypress before starting next task
    screen.show_secret_instructions()
    eyetracker.stop_recording()
    key = event.waitKeys()

    quitExperimentIf(key[0] == 'q')


#################
# Main experiment
#################

# start recording and set destination folder
eyetracker.start_recording(os.path.join(
    CONF["participant"], CONF["session"], "oddball"))

screen.show_blank()

##########################
# establish pool of trials

totTargets = math.floor(CONF["task"]["percentTarget"]
                        * CONF["task"]["totTrials"])

targets = [(CONF["stimuli"]["standard"])] * \
    CONF["task"]["minTargetGap"] + [CONF["stimuli"]
                                    ["target"]]  # little list of target and padding

totStandards = CONF["task"]["totTrials"] - totTargets * \
    len(targets)  # remaining standard elements

allStimuli = [targets, ] * \
    totTargets, [[CONF["stimuli"]["standard"], ]]*totStandards  # list of lists
# TODO: get rid of this extra step at some point
allStimuli = list(itertools.chain(*allStimuli))

random.shuffle(allStimuli)  # randomize

stimuli = list(itertools.chain(*allStimuli))  # restore as a single list


# appropriate labels:
triggerLabels = [0, 0]
# TODO: see with simone if there's a better way
triggerLabels[CONF["stimuli"]["target"]] = "Target"
triggerLabels[CONF["stimuli"]["standard"]] = "Standard"


######################
# loop through stimuli

# give starting instructions
tones.instructions("oddball", 0)
tones.play(CONF["stimuli"]["tone"][0])
core.wait(3)

missingTot = 0

for indx, stimulus in enumerate(stimuli):

    # start trial
    datalog["trialID"] = trigger.sendTriggerId()
    eyetracker.send_trigger(
        "StartTrial", {"trialID": indx})
    core.wait(0.1)
    logging.info("Trial: %s", CONF["stimuli"]["tone"][stimulus])

    preTonePupil = [eyetracker.getPupildiameter(), mainClock.getTime()]

    trigger.send(triggerLabels[stimulus])
    eyetracker.send_trigger("Tone", {"id:": indx, "stimulus": stimulus})
    toneTime = mainClock.getTime()
    tones.play(CONF["stimuli"]["tone"][stimulus])

    postTonePupil = [eyetracker.getPupildiameter(), mainClock.getTime()]

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
            quitExperimentIf(key[0].name == 'q')
            trigger.send("Response")
            eyetracker.send_trigger("Response", {"stimulus": stimulus})
            keys.append([key[0].name, key[0].rt])
            missing = False
            missingTot = 0

    # log
    datalog["keyPresses"] = keys
    datalog["condition"] = triggerLabels[stimulus]
    datalog["ISI"] = isi
    datalog["tone"] = {
        "prePupil": preTonePupil,
        "postPupil": postTonePupil,
        "toneTime": toneTime
    }
    scorer.scores["tot"] += 1

    if missing and stimulus == CONF["stimuli"]["target"]:
        missingTot += 1
        scorer.scores["missed"] += 1

        # play alarm if participant hasn't given a response in a while
        if missingTot >= CONF["task"]["maxMissing"]:

            trigger.send("ALARM")
            core.wait(0.05)
            alarm.play()
            datalog["ALARM!"] = mainClock.getTime()
            eyetracker.send_trigger("Alarm")

    elif not missing and not stimulus == CONF["stimuli"]["target"]:
        scorer.scores["incorrect"] += 1

    elif not missing and stimulus == CONF["stimuli"]["target"]:
        scorer.scores["correct"] += 1

    datalog.flush()

eyetracker.stop_recording()

tones.instructions("oddball", 1)
screen.show_secret_instructions()
key = event.waitKeys()

quitExperimentIf(key[0] == 'q')


######################
# Standing eyes closed
######################


if CONF["includeRest"]:
    # give starting instructions
    tones.instructions("standing", 0)

    trigger.send("StartStand")
    fixationTimer = core.CountdownTimer(CONF["fixation"]["duration"])
    logging.info("starting fixation")
    while fixationTimer.getTime() > 0:
        #  Record any extra key presses during wait
        key = kb.getKeys()
        if key:
            quitExperimentIf(key[0].name == 'q')

        core.wait(1)

    trigger.send("StopStand")
    tones.instructions("standing", 1)

    datalog.flush()


###########
# Concluion
###########


# End main experiment
screen.show_cue("DONE!")
trigger.send("End")
core.wait(CONF["timing"]["cue"])


logging.info('Finished')
scorer.getScore()
trigger.reset()
