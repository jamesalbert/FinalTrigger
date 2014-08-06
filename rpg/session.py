__author__ = 'jbert'

import pickle

class Session(object):
    def __init__(self, **kwargs):
        self.filename = 'saved_data.conf'
        self.kwargs = kwargs
        self.player = kwargs['player']
    def open(self):
        with open(self.filename, 'rb') as save:
            return pickle.load(save)
    def store(self):
        with open(self.filename, 'wb') as save:
            pick.write(self.player, save)
        return self
    def load(self):
        player = self.open()
    def save(self, **kwargs):
        self.open()
        self.store()