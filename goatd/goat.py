class Goat(object):
    '''The goat itself. Most of the work is done by the active driver'''
    def __init__(self, driver):
        self.driver = driver

    def __getattr__(self, name):
        '''Return the requested attribute from the currently loaded driver'''
        return self.driver.handlers.get(name)
