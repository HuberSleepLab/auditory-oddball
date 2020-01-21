import os
from config.configSession import CONF


CONF.update({
    "task": {
        "name": "sample",
    },
    "instructions": {
        "text": "Give instructions",
        "startPrompt": "Press any key to continue. Press q to quit.",
    },
    "pause": {
        "backgroundColor": "black"
    },
    "sounds": {
        "alarm": "horn.wav",
    }
})
