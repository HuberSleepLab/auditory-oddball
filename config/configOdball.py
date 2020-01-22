import os
import logging
import git
import json
# from configSession import CONF


def selectByVersion(data, version="main"):
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


CONF = {}

CONFIG_SESSION_PATHS = [
    '../configSession.json',
    '~/configSession.json',
    '~/Projects/lsm-tasks/configSession.json',
    './config/configSession.json'
]

for path in CONFIG_SESSION_PATHS:
    if CONF:  # we already loaded a config
        continue

    path = os.path.expanduser(path)
    if not os.path.isfile(path):
        continue

    with open(path, 'r+') as f:
        CONF = json.load(f)
        logging.info("Taking json config from: %s", path)
        CONF['confJsonPath'] = path

print(CONF)
CONF = selectByVersion(CONF, CONF["version"])
print("=" * 80)
print(CONF)


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

CONF["trigger"]["labels"]["Target"] = 0x0A
CONF["trigger"]["labels"]["Standard"] = 0x0B
CONF["trigger"]["labels"]["StartFix"] = 0x0C
CONF["trigger"]["labels"]["StopFix"] = 0x0D
CONF["trigger"]["labels"]["StartStand"] = 0x0E
CONF["trigger"]["labels"]["StopStand"] = 0x0F

repo = git.Repo(search_parent_directories=True)
CONF["gitHash"] = repo.head.object.hexsha

if CONF["version"] == "main":
    CONF["loggingLevel"] = logging.WARNING
elif CONF["version"] == "demo":
    CONF["loggingLevel"] = logging.INFO
else:
    CONF["loggingLevel"] = logging.INFO
