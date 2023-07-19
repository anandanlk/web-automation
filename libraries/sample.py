from core import seleniuminterface

class Sample:
    def __init__(self):
        self.s_handle = seleniuminterface.SeleniumInterface()

    def sample1(self):
        self.s_handle.open_browser()
        self.s_handle.navigate('google.com')

