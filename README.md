# auditory-oddball

This is an implementation of a simple auditory oddball. It presents tones at irregular intervals, and a certain percentage of those will be "target" tones, after which the participant has to push a button. The reaction times, false alarms and missed responses will be saved in a JSON. The task further allows synchronization via triggers with EEG (currently configured with BrainAmp) and pupillometry. Optionally, this task will record resting wake EEG prior to the oddball (see [Snipes et al. 2023, iScience](http://dx.doi.org/10.1016/j.isci.2023.107138)). Verbal instructions are provided for the participant.

## Design

Part 1: Fixation. Participant must fixate on a point for a certain amount of time. Instructions are provided as audio, and the timing is taken care of by the scripts.

Part 2: Oddball. Participant listens to tones, and pushes a button whenever a target tone is played. Like Part 1, the timing is all determined by the script and neither the experimenter nor participant controls it.

Part 3: Questionnaire. Participants are informed they need to fill out a questionnaire (provided externally from this library). The script pauses, and then the experimenter needs to push a button to indicate that the questionnaire has been filled, and the participant has been set up to stand for the final standing recording.

Part 4: Standing with eyes closed. Participants must stand (leaning against a wall for balance) with their eyes closed for a set amount of time. The start is triggered by the experimenter pushing a button (to delineate the end of the questionnaire-filling period and the start of the standing), and after a set amount of time, informs the participant that the time is up. This task was particular for the Local Sleep Marker experiment for Snipes et al., and can be deactivated at will.

The experiment design is very flexible, and can be configured in ConfigOddball.py and ConfigSession.json.
Important configurations include:
- the total number of trials
- the percentage of those trials that should be targets
- The interstimulus intervals (ISI), min and max
- Minimum number of standard tones between targets
- Maximum number of missing tones before an alarm sounds to wake up the participant
- Stimulus / target tone frequencies

To run this experiment, make sure you have everything downloaded and set up in the configurations (see instructions below). The experiment can be run in three modes:

#### DEBUG Mode
This setting plays the task very briefly, just enough to see if everything is working. The experimenter can decide which aspects of the task should be played in debug mode.

#### DEMO Mode
This is to demonstrate to the participant how the task works. Like this, they can try a few trials, get used to the instructions, but not have to go through the whole experiment. The demo does not send triggers to any external devices.

#### MAIN Mode
This is how the experiment runs. It lasts for the full number of requested trials

## Output
The results of the task get saved in a folder in this repo: output, which saves a copy of the configurations (including participant ID), and then a log file with a line like so for each trial:

`{"trialID": {"id": 9, "triggers": [201], "duration": 0.01}, "keyPresses": [], "condition": "Standard", "ISI": 2.2, "tone": {"prePupil": [0, 31.9], "postPupil": [0, 32.0], "toneTime": 31.9}}`

It therefore keeps track of every key press, the trial information, etc. The filename is saved as `{Participant ID}_{Session ID}_{timestamp}.log` so even if the IDs are incorrect, there will always be a unique filename and can be traced back based on when it was recorded.

# Scripts

## Configurations
There are two configuration files: `configOddball.py` which sets up the experiment, and should remain the same for each participant / recording; `configSession.json` which should be adapted before each recording.

### configOddball
This is a python script because it could in theory to fancy things (I don't think it does for this task, but it's been a while...). Here, all the parameters of the task are set, and so it should remain the same for the whole experiment.

### configSession
In the repository, this is saved as `configSession_template.json`, but should be re-saved as `configSession.json` once it has been configured. Here, the experimenter can specify participant ID, session number, and importantly, whether to run the debug, demo or main mode. Many of the settings are actually meant to be configured just once, but they have to be in this script for how the configurations gets read. Sorry about that.


## Code

### mainOddball.py

This file dictates the sequence of events in the task. To run the experiment, you need to run this script.

### screen

This is a class that takes care of ALL screen related activity, initializing all the visual components, and then providing clean functions for showing different setups. For this auditory oddball, none of it is particularly important.

### datalog

This is a class that takes care of saving the data to an output folder, grouped by day. It saves the configuration in its entirety, and a second file that saves a dictionary with anything the main.py file dumps into it.

### trigger

This is a class that takes care of all the technical details of sending triggers. See trigger section below.

### scorer

This lets you easily keep track of participant performance, so that you can spit out the result in the terminal at the end, or whenver you quit.

### tones

This is a class for preparing and playing tones, based on PsychoPy library.



# SETUP

## Setup Instructions - Linux

### Setting up env

Copy local env:

1. Run within current folder: `cp {env} .`
2. Run `pyvenv env`

Make env (recommended into a general projects folder so can use for other experiments):

1. Create in folder `pyvenv psychopyEnv`
2. Activate with `source psychopyEnv/bin/activate`
3. Install requirements: `pip install -r requirements.txt`

If psychopy has problems, just download all of these:

`sudo apt install python3-dev libx11-dev libasound2-dev portaudio19-dev libusb-1.0-0-dev libxi-dev build-essential libgtk-3-dev gtk3.0 python3-wxgtk3.0`

and if you need more:

`sudo apt-get install libjpeg-dev libtiff-dev libgtk2.0-dev libsdl1.2-dev freeglut3 freeglut3-dev libnotify-dev libgstreamerd-3-dev`

Create requirements:

`pip freeze > requirements.txt`

### Give account access to ports for triggers (and for shortcuts ?)

1. Add you user to the riht group: `sudo uermod -a -G dialout $USER`
2. Identify the name of the port, and save as "serial_device" in CONF: `ls /dev/tty{USB,ACM}*`, only one should show up.

### Create starting shortcut

This is needed so you can start the experiment from wherever in the terminal.

1. Make sure there is the file exp-sample
2. Run `code ~/.bashrc` in terminal
3. Add at the bottom: `export PATH=~/Projects/sample_psychopy/:$PATH` and save
4. Give permission to use that file: `chmod +x Projects/sample_psychopy/exp-sample`
5. Start a new window to see if it worked

Then from a new terminal, you can run directly `exp-match2sample` and it starts!

### Get monitor settings


1. Run `xrandr` in terminal

## Windows

1. Install old version of psychopy: https://github.com/psychopy/psychopy/releases/tag/3.2.4



## Triggers (EEG)
Digital triggers are sent 

### Trigger code

- 1 - Start
- 2 - End
- 4 - Response
- 8 - Alarm
- 9 - Quit (user quit the experiment)
- 10 - Target tone
- 11 - Standard tone
- 12 - Start fixation period
- 13 - Stop fixation period
- 14 - Start standing period
- 15 - End standing period
- 192 > - Every trial is marked with either one, two, or three triggers in quick succession as a unique identifier (there's only so many numbers that can be sent, thus multiple triggers account for larger trial numbers). Since triggers are sent at exatly the tone onset, these are just a backup in case the trigger system gets disconnected, some triggers are lost, and the total number of stimulus triggers does not line up with the stimuli presented.

### How to use / setup (Brainamp)

1. Install the [TriggerBox Test IO](https://www.brainproducts.com/downloads/more-software/#triggerbox-test-io) which installs drivers that are needed to send triggers via USB. More instructions here: https://pressrelease.brainproducts.com/triggerbox-tips/. 

2. In ConfigSession.json, it specifies `serial_device`, which should be `COM3`; if it's not, change it to whatever COM this TriggerBox software has chosen.

3. Connect via USB the computer running the auditory oddball task to the EEG TriggerBox.

## Pupillometry
May the Lord be with you...

This script can work together with PupilCapture software from PupilLabs. It sentds triggers either over ethernet connection or wifi so that the pupil size recordings can be synchronized to the tones and the EEG. I forgot how it works, sorry.


# How to run

### Linux

From within folder:

1. Enter psychopy environment in terminal, either using shortcut `psyEnv` or `source ~/Projects/psychopyEnv/bin/activate`
2. Then run with `python3 main.py`

From anywhere (needs to setup shortcut first):

1. Configure participant and session: `export participant=P00 session=0`
2. Run specific task: `exp-sample`

### Windows (GUI)

1. Open psychopy (version 3)
2. Open visual studio code (or similar)
   - modify participant ID and session, save
3. Open "main.py" for this experiment in psychopy
4. Click the green run button in the psychopy interface

### Windows (Powershell)

1. Open PowerShell
2. cd into code directory
3. Run ` & 'C:\Program Files\PsychoPy3\python.exe' .\mainOddball.py`

## Credits:

Sounds:

- horn.wav: https://freesound.org/people/mcpable/sounds/131930/
- speech (https://www.ibm.com/watson/services/text-to-speech/): https://text-to-speech-demo.ng.bluemix.net/?cm_mc_uid=32181889639815798809160&cm_mc_sid_50200000=71278021579880916114&cm_mc_sid_52640000=72232831579880916152

# TODO:

- Make compatible with more recent versions of libraries
- create a more specific requirements lists

