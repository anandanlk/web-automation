import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))
from libraries.core.SeleniumInterface import SeleniumInterface


class Sample:
    def __init__(self):
        self.s_handle = SeleniumInterface()

    def sample1(self):
        self.s_handle.open_browser()
        self.s_handle.navigate("welcome")
