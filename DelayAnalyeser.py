from __future__ import division
import csv
import time


STATE_0 = 0
STATE_1 = 1
STATE_2 = 2
STATE_3 = 3
STATE_INCONSISTENT = 4

ACTION_GOING_UP_LATE      = 10
ACTION_GOING_UP_FORWARD   = 11
ACTION_GOING_DOWN_LATE    = 12
ACTION_GOING_DOWN_FORWARD = 13
ACTION_PASS               = 14
ACTION_ALERT              = 15

UP = "up"
DOWN = "down"
LATE = 1
FORWARD = -1
PASS = 0

SKIP_FIRST_ROWS = True
ROWS_TO_SKIP = 10

# Usage: new_state = state_transition_table[previous_state][new_reading]
state_transition_table = [[STATE_0,            STATE_1,            STATE_2,            STATE_INCONSISTENT],
                          [STATE_0,            STATE_1,            STATE_INCONSISTENT, STATE_3],
                          [STATE_0,            STATE_INCONSISTENT, STATE_2,            STATE_3],
                          [STATE_INCONSISTENT, STATE_1,            STATE_2,            STATE_3],
                          [STATE_0,            STATE_INCONSISTENT, STATE_INCONSISTENT, STATE_3]]

# Usage: new_action = action_table[previous_state][new_state]
action_table = [[ACTION_PASS, ACTION_GOING_UP_LATE,      ACTION_GOING_UP_FORWARD, ACTION_PASS, ACTION_ALERT],
                [ACTION_PASS, ACTION_PASS,               ACTION_PASS,             ACTION_PASS, ACTION_ALERT],
                [ACTION_PASS, ACTION_PASS,               ACTION_PASS,             ACTION_PASS, ACTION_ALERT],
                [ACTION_PASS, ACTION_GOING_DOWN_FORWARD, ACTION_GOING_DOWN_LATE,  ACTION_PASS, ACTION_ALERT],
                [ACTION_PASS, ACTION_PASS,               ACTION_PASS,             ACTION_PASS, ACTION_ALERT]]

unit_conversion = {
    'Mn': 0,  # use 0 to discard values in this scale
    's': 10 ** 6,
    'ms': 10 ** 3,
    'us': 10 ** 0,
    'ns': 10 ** (-3),
}



if __name__ == "__main__":
    start = time.time()

    input_filename = 'Data/ubuntu_night_gologic.csv'
    output_filename = input_filename.rsplit('.',1)
    output_filename[0] += '_output'
    output_filename_alt = output_filename[0] + '_alt.csv'
    output_filename = output_filename[0] + '-2.0.csv'

    previous_state = STATE_INCONSISTENT

    with open(input_filename, 'r') as raw_file, open(output_filename, 'w') as output_file, open(output_filename_alt, 'w') as output_file_alt:
        reader = csv.reader(raw_file)
        writer = csv.writer(output_file)
        alt_writer = csv.writer(output_file_alt)
        next(reader) # skip header row

        writer.writerow(['delay_us', 'accumulated_us'])
        alt_writer.writerow(['previous_state', 'new_reading', 'new_state', 'new_action', 'accumulated_us', 'timing', 'duration', 'alert_counter'])

        previous_state = STATE_INCONSISTENT
        accumulated_us = 0

        row_counter = 0
        alert_counter = 0
        for row in reader:
            row_counter += 1

            if SKIP_FIRST_ROWS and row_counter < ROWS_TO_SKIP:
                continue

            new_reading = int(row[1])
            new_state = state_transition_table[previous_state][new_reading]
            new_action = action_table[previous_state][new_state]

            previous_state = new_state
            duration = float(row[2])*unit_conversion[row[3]]

            if (new_reading == 1 or new_reading == 2) and duration == 0:
                print("Fuck")


            if new_action == ACTION_GOING_UP_LATE:
                direction = UP
                timing = LATE
            elif new_action == ACTION_GOING_UP_FORWARD:
                direction = UP
                timing = FORWARD
            elif new_action == ACTION_GOING_DOWN_LATE:
                direction = DOWN
                timing = LATE
            elif new_action == ACTION_GOING_DOWN_FORWARD:
                direction = DOWN
                timing = FORWARD
            elif new_action == ACTION_ALERT:
                alert_counter += 1
                print("Going to inconsistent state! Instant {}, counter {}/{}, new_state {}".format(accumulated_us, alert_counter, row_counter, new_state))
                timing = None
            elif new_action == ACTION_PASS:
                timing = None

            alt_writer.writerow([previous_state, new_reading, new_state, new_action, accumulated_us, timing, duration, alert_counter])

            accumulated_us += duration

            if new_action == ACTION_PASS or new_action == ACTION_ALERT:
                continue

            delay_us = timing * duration

            # if delay_us < 1 and delay_us > -1:
            #     print(delay_us)

            writer.writerow([delay_us, accumulated_us])




    elapsed = time.time() - start
    print("{} rows processed in {} seconds".format(row_counter, elapsed))
