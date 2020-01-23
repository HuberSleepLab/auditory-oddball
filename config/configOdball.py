from config.updateConfig import UpdateConfig

oddballCONF = {
    "task": {
        "name": "oddball",
        "percentTarget": .20,
        "totTrials": {"versionMain": 200, "versionDemo": 10, "versionDebug": 20},
        "ISI": [1.8, 2.4],  # min and max of interstimulus interval
        "backgroundColor":  "black",   # 999999",
        "minTargetGap": 3,  # minimum number of non targets between targets
        "maxMissing": 4,
    },
    "instructions": {
        "text": "Instructor gives instructions (no visuals!)",
        "startPrompt": "Press any key to continue. Press q to quit.",
        "darkColor": {"versionMain": "#040029", "versionDemo": "blue", "versionDebug": "white"},
    },
    "stimuli": {
        "duration": .06,  # in seconds
        "tone": [660, 440],
        "target": 0,  # TODO: counterbalance selection!!
        "standard": 1,  # TODO, make this automatically determined
    },
    "sounds": {
        "alarm": "horn.wav",
    },
    "fixation": {
        "duration": {"versionMain": 60*7, "versionDemo": 1, "versionDebug": 1},
    },
}

oddballTriggers = {
    "Target": 10,
    "Standard": 11,
    "StartFix": 12,
    "StopFix": 13,
    "StartStand": 14,
    "StopStand": 15,
}


updateCofig = UpdateConfig()
updateCofig.addContent(oddballCONF)
updateCofig.addTriggers(oddballTriggers)

CONF = updateCofig.getConfig()
