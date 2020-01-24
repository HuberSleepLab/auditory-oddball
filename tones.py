import os

from psychopy import sound, core


class Tones:
    def __init__(self, CONF):
        self.CONF = CONF
        # TODO: record audio, see if its around .01s
        # self.tone = sound.Sound(secs=CONF["stimuli"]["duration"])
        self.tone = sound.Sound()
        self.voice = sound.Sound()

    def play(self, tone):
        self.tone.setSound(tone, secs=self.CONF["stimuli"]["duration"])
        self.tone.play()
        core.wait(self.CONF["stimuli"]["duration"])

    def instructions(self, task, isEnd):
        sound = os.path.join("sounds", self.CONF["instructions"][task][isEnd])
        self.voice.setVolume(0.5)
        self.voice.setSound(
            sound, secs=self.CONF["instructions"]["instructionDuration"])
        self.voice.play()
        core.wait(self.CONF["instructions"]["instructionDuration"])
