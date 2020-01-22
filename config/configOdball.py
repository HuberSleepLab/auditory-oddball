import os
from config.configSession import CONF


CONF.update({
    "task": {
        "name": "oddball",
        "percentTarget": .20,
        "totTrials": 200,
        "ISI": [1.8, 2.2],  # min and max of interstimulus interval
        "backgroundColor":  "black",   # 999999",
        "minTargetGap": 3,  # minimum number of non targets between targets
        "maxMissing": 4,
    },
    "instructions": {
        "text": "Instructor gives instructions (no visuals!)",
        "startPrompt": "Press any key to continue. Press q to quit.",
        "darkColor": "#040029",
    },
    "stimuli": {
        "duration": .06,  # in seconds
        "tone": [660, 440],
        "target": 0,  # TODO: counterbalance selection!!
        "standard": 1,  # TODO, make this automatically determined
        "ramp": .01,  # if possible include a ramp
    },
    "sounds": {
        "alarm": "horn.wav",
    },
    "fixation": {
        "duration": 60*.1,  # 60*7,
    }
})

CONF["trigger"]["labels"]["Target"] = 0x0A
CONF["trigger"]["labels"]["Standard"] = 0x0B
CONF["trigger"]["labels"]["StartFix"] = 0x0C
CONF["trigger"]["labels"]["StopFix"] = 0x0D
CONF["trigger"]["labels"]["StartStand"] = 0x0E
CONF["trigger"]["labels"]["StopStand"] = 0x0F
