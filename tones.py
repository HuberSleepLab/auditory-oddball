

from psychopy import sound


class Tones:
    def __init__(self, CONF):
        self.CONF = CONF
        # TODO: record audio, see if its around .01s
        # self.tone = sound.Sound(secs=CONF["stimuli"]["duration"])
        self.tone = sound.Sound()

    def play(self, tone):
        self.tone.setSound(tone, secs=self.CONF["stimuli"]["duration"])
        self.tone.play()  # TODO: make timing more precess with trigger! Maybe insert onflip here?
