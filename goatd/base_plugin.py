from abc import ABCMeta, abstractmethod


class BasePlugin(object):
    __metaclass__ = ABCMeta

    def __init__(self, config, goatd):
        self.config = config
        self.goatd = goatd
        self.running = False

    def start(self):
        self.running = True
        self.main()

    @abstractmethod
    def main(self):
        '''
        The main method for a plugin. This should contain a loop if the plugin
        is intended to be long-running.
        '''
        pass
