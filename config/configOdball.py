from config.updateConfig import UpdateConfig

oddballCONF = {
    "includeRest":  {"versionMain": True, "versionDemo": False, "versionDebug": True},
    "task": {
        "name": "oddball",
        "percentTarget": .20,
        "totTrials": {"versionMain": 200, "versionDemo": 10, "versionDebug": 20},
        "ISI": [1.8, 2.4],  # min and max of interstimulus interval
        "backgroundColor":  "black",   # 999999",
        "minTargetGap": 3,  # minimum number of non targets between targets
        "maxMissing": 4,
        "prePupilGap": 0.05,  # in seconds
    },
    "instructions": {
        "text": "Instructor gives instructions (no visuals!)",
        "startPrompt": "Press any key to continue. Press q to quit.",
        "darkColor": {"versionMain": "#040029", "versionDemo": "blue", "versionDebug": "white"},
        "fixation": ["startFixationLong.wav", "endFixation.wav"],
        "instructionDuration": 5,
        "oddball": ["startOddball.wav", "endOddball.wav"],
        "standing": ["startStanding.wav"]
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
        "duration": {"versionMain": 60*7, "versionDemo": 5, "versionDebug": 5},
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
