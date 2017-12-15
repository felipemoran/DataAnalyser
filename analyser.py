from __future__ import division
import csv
import time


def us2string(us):
    hours, rem = divmod(us/1000000, 3600)
    minutes, seconds = divmod(rem, 60)
    return"{:0>2}h{:0>2}m{:02.0f}s".format(int(hours), int(minutes), seconds)


class Symbol:
    def __init__(self, value, duration):
        self.value = value
        self.duration = duration

    def is_partial(self):
        if self.value == "00" or self.value == "11":
            return False
        else:
            return True


class Sequence(object):
    def __init__(self):
        self.list = []

    def get_last(self):
        if len(self.list) != 0:
            return self.list[-1]
        else:
            return None

    def set_last(self, symbol):
        self.list[-1] = symbol

    def add_and_analyse(self, symbol):
        # if list is empty and symbol is partial, throw it away, otherwise add it an return
        if len(self.list) == 0:
            if not symbol.is_partial():
                self.list.append(symbol)

            return None

        # first check if symbol is equal
        if symbol.value == self.get_last().value:
            # if so, update its duration
            symbol.duration += self.get_last().duration
            self.set_last(symbol)

            return None
        else:
            # otherwise add it to the list
            self.list.append(symbol)

        # if symbol is partial, do nothing. Wait for the next
        if symbol.is_partial():
            return None

        # if it has something, then get the delay!
        delay = self.analyse()

        # reset the list with the last element added, which will became the first
        self.list = [self.list[-1]]

        return delay

    def analyse(self):
        if len(self.list) == 2:
            return 0
            # instantaneous change! Unless the function add did something wrong and these 2 symbols are not terminals and not the same
        elif len(self.list) == 3:
            # must be a delay or inconsistent transition
            if self.list[0].value == self.list[-1].value:
                # shit, inconsistent
                return None

            return self.list[1].duration

        else: # wow, we had two or more partial symbols between full symbols! This is not good, return nothing
            return None


