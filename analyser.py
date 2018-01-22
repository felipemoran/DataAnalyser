from __future__ import division
import csv
import time
from collections import namedtuple


def us2string(us):
    hours, rem = divmod(us/1000000, 3600)
    minutes, seconds = divmod(rem, 60)
    return"{:0>2}h{:0>2}m{:02.6f}s".format(int(hours), int(minutes), seconds)


class Symbol:
    def __init__(self, value, duration):
        self.value = value
        self.duration = duration

    def is_partial(self):
        if self.value == "00" or self.value == "11":
            return False
        else:
            return True


SequenceResult = namedtuple("SequenceResult", ["is_invalid", "duration"])


class Sequence:
    def __init__(self):
        self.list = []

    def __str__(self):
        return_str = ""
        for item in self.list:
            return_str += "(" + item.value + ": " + str(item.duration) + ") "
        return return_str

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

            return SequenceResult(None, None)

        # first check if symbol is equal
        if symbol.value == self.get_last().value:
            # if so, update its duration
            symbol.duration += self.get_last().duration
            self.set_last(symbol)

            return SequenceResult(None, None)
        else:
            # otherwise add it to the list
            self.list.append(symbol)

        # if symbol is partial, do nothing. Wait for the next
        if symbol.is_partial():
            return SequenceResult(None, None)

        # if it has something, then get the delay!
        delay = self.analyse()

        # reset the list with the last element added, which will became the first
        self.list = [self.list[-1]]

        return delay

    def analyse(self):
        if len(self.list) == 2:
            return SequenceResult(False, 0)
            # instantaneous change! Unless the function add did something wrong and these 2 symbols are not terminals and not the same
        elif len(self.list) == 3:
            # must be a delay or inconsistent transition
            if self.list[0].value == self.list[-1].value:
                # shit, inconsistent. I should raise something
                return SequenceResult(True, None)

            signal = 1
            if self.list[0].value == "00" and self.list[1].value == "01":
                signal = -1
            elif self.list[0].value == "11" and self.list[1].value == "10":
                signal = -1

            return SequenceResult(False, signal * self.list[1].duration)

        else: # wow, we had two or more partial symbols between full symbols! This is not good, return nothing
            return SequenceResult(True, None)


class Analyser:
    unit_conversion = {
        'Mn': 0,  # use 0 to discard values in this scale
        's': 10 ** 6,
        'ms': 10 ** 3,
        'us': 10 ** 0,
        'ns': 10 ** (-3),
    }

    def __init__(self, filename, state_columns, duration_column, unit_column, has_header=True):
        self.filename = filename
        self.state_columns = state_columns
        self.duration_column = duration_column
        self.unit_column = unit_column

        self.sequences = {}
        self.results = {}

        for column in state_columns:
            self.sequences[column] = Sequence()
            self.results[column] = []

    def run(self):
        start = time.time()

        with open(self.filename, 'r') as raw_file:
            reader = csv.DictReader(raw_file)
            accumulated_duration = 0
            row_counter = 0
            # TODO: change double loop by single loop with product(rows, columns)

            counter_invalid = {}
            counter_total = {}
            for column in state_columns:
                counter_invalid[column] = 0
                counter_total[column] = 0


            for row in reader:
                row_counter += 1
                duration = float(row[self.duration_column]) * self.unit_conversion[row[self.unit_column]]
                accumulated_duration += duration

                for column in self.state_columns:
                    symbol = Symbol(row[column], duration)
                    result = self.sequences[column].add_and_analyse(symbol)
                    if result.is_invalid:
                        counter_invalid[column] += 1
                        counter_total[column] += 1

                        # print("Invalid sequence! Column {}".format(column))
                        # for column in self.state_columns:
                        #     print("{} {}/{} : {:.2f}%  ".format(column, counter_invalid[column], counter_total[column], counter_invalid[column]/counter_total[column]*100), end='')
                        # print()

                    elif result.duration is not None:
                        counter_total[column] += 1
                        self.results[column].append(result.duration)

                        # Debugging
                if column == "tsch_arduino":
                    if int(len(self.results["tsch_arduino"])) == 109694:
                        break
                        print("Row {} : {}".format(row["Sample#"], us2string(accumulated_duration)))
                        #
                        #     if int(len(self.results["gps_arduino"])) == 3925:
                        #         # break
                        #         print("Row {} : {}".format(row["Sample#"], us2string(accumulated_duration)))
                        #
                        #     if int(len(self.results["gps_arduino"])) == 7800:
                        #         # break
                        #         print("Row {} : {}".format(row["Sample#"], us2string(accumulated_duration)))
                        #
                        #     if int(len(self.results["gps_arduino"])) == 8200:
                        #         # break
                        #         print("Row {} : {}".format(row["Sample#"], us2string(accumulated_duration)))

                # Debugging
                # if int(row["Sample#"]) == 650400:
                #     print("--- Row {} : {}".format(row["Sample#"], us2string(accumulated_duration)))
                #     # break
                # if len(self.results["tsch_arduino"]) == 106000:
                #     break

            for column in self.state_columns:
                self.write_list_to_file(self.filename, column, self.results[column])

        elapsed = time.time() - start
        print("{} rows processed in {:.2f} seconds".format(row_counter, elapsed))

        for column in self.state_columns:
            print("Column {} has {} samples".format(column, len(self.results[column])))

        print("Total test duration: {}".format(us2string(accumulated_duration)))

    @staticmethod
    def write_list_to_file(filename, title, list):
        filename = filename.rsplit(".", 1)
        filename = filename[0] + "." + title + "." + filename[1]

        with open(filename, 'w') as outputfile:
            writer = csv.writer(outputfile)

            for row in list:
                writer.writerow((row,))


if __name__ == "__main__":
    filename = "Data/2018-1-22_1.csv"
    # state_columns = ["gps_pure", "gps_rpi", "tsch_arduino", "mote"]
    state_columns = ["tsch_arduino"]
    duration_column = "SampleTime"
    unit_column = "units"

    analyser = Analyser(filename, state_columns, duration_column, unit_column)
    analyser.run()