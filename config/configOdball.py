import os
from config.configSession import CONF


CONF.update({
    "task": {
        "name": "oddball",
        "percentTarget": 20,
        "totTrials": 200,
        "ISI": [1.8, 2.2],  # min and max of interstimulus interval
        "backgroundColor": "#999999",
        "minTargetGap": 3,  # minimum number of non targets between targets
    },
    "instructions": {
        "text": "Give instructions",
        "startPrompt": "Press any key to continue. Press q to quit.",
    },
    "stimuli": {
        "duration": .06,  # in seconds
        # pitch of tones, should be counterbalanced, but for now, randomized
        "tones": [660, 440],
        "ramp": .01,  # if possible include a ramp
    },
    "sounds": {
        "alarm": "horn.wav",
    }
})
