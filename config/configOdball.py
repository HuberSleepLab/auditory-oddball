import os
from config.configSession import CONF


CONF.update({
    "task": {
        "name": "oddball",
        "percentTarget": .20,
        "totTrials": 20,
        "ISI": [1.8, 2.2],  # min and max of interstimulus interval
        "backgroundColor": "#999999",
        "minTargetGap": 3,  # minimum number of non targets between targets
    },
    "instructions": {
        "text": "Instructor gives instructions (no visuals!)",
        "startPrompt": "Press any key to continue. Press q to quit.",
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
    }
})
