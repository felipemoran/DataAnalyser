import csv
import time

unit_conversion = {
    'Mn': 0,  # use 0 to discard values in this scale
    's': 10 ** 6,
    'ms': 10 ** 3,
    'us': 10 ** 0,
    'ns': 10 ** (-3),
}


def us2string(us):
    hours, rem = divmod(us/1000000, 3600)
    minutes, seconds = divmod(rem, 60)
    return"{:0>2}h{:0>2}m{:02.6f}s".format(int(hours), int(minutes), seconds)


def write_list_to_file(filename, title, data):
    filename = filename.rsplit(".", 1)
    filename = filename[0] + "." + title + "." + filename[1]

    with open(filename, "w") as f:
        writer = csv.writer(f)
        writer.writerows(list(map(list, zip(*data))))


def analyse(filename):
    start = time.time()
    duration_column = "SampleTime"
    unit_column = "units"

    stored_delays = [[], []]

    with open(filename, 'r') as raw_file:
        reader = csv.DictReader(raw_file)
        accumulated_duration = 0
        row_counter = 0

        last_state = {
            "gps": None,
            "arduino": [None, None]
        }

        last_gps_reference = None

        for row in reader:
            this_state = {
                "gps": int(row["gps"]),
                "arduino": [int(row["arduino"]) & 0b01, (int(row["arduino"]) & 0b10) >> 1]
            }


            # Check for delays
            if last_gps_reference is not None:
                for i in range(len(this_state["arduino"])):
                    if last_state["arduino"][i] == 1 and this_state["arduino"][i] == 0:
                        # detected arduino rising edge!
                        delay = accumulated_duration - last_gps_reference
                        stored_delays[i].append(delay)
                        print("ARD{}: {} -> {}".format(i, accumulated_duration, delay))

            # Check for new GPS reference
            if last_state["gps"] is not None and \
                            last_state["gps"] == 1 and this_state["gps"] == 0:  # falling edge detected!
                last_gps_reference = accumulated_duration
                print("GPS:  {}".format(last_gps_reference))


            last_state["gps"] = this_state["gps"]
            for index, value in enumerate(this_state["arduino"]):
                last_state["arduino"][index] = value



            row_counter += 1
            duration = float(row[duration_column]) * unit_conversion[row[unit_column]]
            accumulated_duration += duration

    write_list_to_file(filename, "delays_gps_reference", stored_delays)

    elapsed = time.time() - start
    print("{} rows processed in {:.2f} seconds".format(row_counter, elapsed))

    for i in range(len(stored_delays)):
        print("Column {} has {} samples".format(i, len(stored_delays[i])))

    print("Total test duration: {}".format(us2string(accumulated_duration)))



if __name__ == "__main__":
    analyse("old_data/2018-1-23_6.csv")