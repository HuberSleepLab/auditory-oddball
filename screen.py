import random
import os
import numpy as np
import random

from psychopy import visual, core, event, monitors
from psychopy.hardware import keyboard
from psychopy.visual import textbox


class Screen:
    def __init__(self, CONF):
        self.CONF = CONF

        # set monitor parameters
        mon = monitors.Monitor('tesfgft')  # random string name
        mon.setWidth(CONF["screen"]["size"][0])
        mon.setSizePix(CONF["screen"]["resolution"])

        self.window = visual.Window(
            size=CONF["screen"]["resolution"],
            color=CONF["task"]["backgroundColor"] or "black",
            monitor=mon,
            fullscr=CONF["screen"]["full"],
            allowGUI=True,
            units="cm"
        )

        # set up instructions and overview
        self.task = visual.TextStim(self.window,
                                    text=CONF["task"]["name"],
                                    alignHoriz='center',
                                    alignVert='center',
                                    height=CONF["instructionSizes"]["taskHeight"],
                                    pos=CONF["instructionSizes"]["taskPos"],
                                    units="cm"
                                    )
        self.session = visual.TextStim(self.window,
                                       text="P" + CONF["participant"] +
                                       " Session " +
                                       CONF["session"] + " " + CONF["version"],
                                       pos=CONF["instructionSizes"]["sessionPos"],
                                       height=CONF["instructionSizes"]["sessionHeight"],
                                       alignHoriz='center',
                                       alignVert='center',
                                       units="cm"
                                       )

        self.instructions = visual.TextStim(
            self.window, text=CONF["instructions"]["text"], height=CONF["instructionSizes"]["instructionsHeight"], units="cm")

        self.startPrompt = visual.TextStim(
            self.window, text=CONF["instructions"]["startPrompt"], height=CONF["instructionSizes"]["startPromptHeight"], units="cm", pos=(0, -CONF["screen"]["size"][1]/2+3))

        self.cue = visual.TextStim(self.window)

    def show_overview(self):
        self.task.draw()
        self.session.draw()
        self.window.flip()

    def show_instructions(self):
        self.session.pos = (0, self.CONF["screen"]["size"][1]/2-1)
        self.session.draw()
        self.instructions.draw()
        self.startPrompt.draw()
        self.window.flip()

    def show_blank(self):
        self.window.flip()

    def show_cue(self, word):
        self.cue.setText(word)
        self.cue.draw()
        self.window.flip()

    def show_secret_instructions(self):
        self.startPrompt.color = self.CONF["instructions"]["darkColor"]
        self.startPrompt.draw()
        self.window.flip()
