import logging
import os
import git


CONF = {
    "participant": os.environ.get("participant", "00"),
    "session": os.environ.get("session", "0"),
    "version": ["main", "demo", "debug"][1],
    "screen": {
        # screen size when fullscreen
        "resolution": [3840, 2160],
        "size": [34.4, 19.3],
        "units": "cm",
        "full": True,
    },
    "timing": {
        "overview": 1,
        "cue": 1,
        "rest": 60
    },
    "trigger": {
        # this is computer and OS and port and random specific. see readme on how to get
        "serial_device": "COM3",  # COM3 for windows
        "labels": {
            "Start": 0x01,
            "End": 0x02,
            "Stim": 0x03,
            "Response": 0x04,
            "BadResponse": 0x05,
            "StartBlank": 0x06,
            "EndBlank": 0x07,
            "ALARM": 0x08,
            "Quit": 0x09,
        }
    }
}

# get current git
repo = git.Repo(search_parent_directories=True)
CONF["gitHash"] = repo.head.object.hexsha

# Settings based on version
if CONF["version"] == "main":
    CONF.update({
        "showInstructions": True,
        "sendTriggers": True,
        "loggingLevel": logging.WARNING})

elif CONF["version"] == "demo":
    CONF.update({
        "showInstructions": True,
        "sendTriggers": False,
        "loggingLevel": logging.WARNING})
    CONF["screen"]["full"] = True
    CONF["timing"]["rest"] = 1
else:
    CONF.update({
        "showInstructions": False,
        "sendTriggers": False,
        "logginLevel": logging.INFO})
    CONF["screen"]["full"] = True
    CONF["timing"]["rest"] = 1
    CONF["screen"]["resolution"] = [1000, 1000],
    CONF["screen"]["size"] = [10, 10],
