import os
import logging
import git
import json

###################################################################

################################################
# get common configuration values from json file
################################################


def selectByVersion(data, version="main"):
    "Runs through json and selects variables that has multiple options for different versions."
    if type(data) == dict:
        if "versionMain" in data:
            version = "version" + version[0].upper() + version[1:]
            if version in data:
                return data[version]
            else:
                return data["versionMain"]
        else:
            for key in data:
                data[key] = selectByVersion(data[key], version)
    elif type(data) == list:
        for i, elem in enumerate(data):
            data[i] = selectByVersion(elem, version)
    return data


# start configuration
CONF = {}

########################
# look for configuration in possible locations (in order of choice)

CONFIG_SESSION_PATHS = [
    '../configSession.json',
    '~/configSession.json',
    './config/configSession.json'
]

for path in CONFIG_SESSION_PATHS:
    # stop searching once CONF found
    if CONF:
        break

    path = os.path.expanduser(path)
    if not os.path.isfile(path):
        continue

    # load CONF when found
    with open(path, 'r+') as f:
        CONF = json.load(f)

        # log
        logging.info("Taking json config from: %s", path)
        CONF['confJsonPath'] = path

CONF = selectByVersion(CONF, CONF["version"])

# save the git version of the experiment
repo = git.Repo(search_parent_directories=True)
CONF["gitHash"] = repo.head.object.hexsha

# set the logging level
loggingLevels = {
    "debug": logging.DEBUG,
    "info": logging.INFO,
    "warning": logging.WARNING,
    "error": logging.ERROR,
    "fatal": logging.FATAL
}

CONF["loggingLevel"] = loggingLevels[CONF["loggingLevel"]]


#################################################################

#############################
# Task specific configuration
#############################

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
    },

})

# add more triggers
CONF["trigger"]["labels"]["Target"] = 10
CONF["trigger"]["labels"]["Standard"] = 11
CONF["trigger"]["labels"]["StartFix"] = 12
CONF["trigger"]["labels"]["StopFix"] = 13
CONF["trigger"]["labels"]["StartStand"] = 14
CONF["trigger"]["labels"]["StopStand"] = 15
