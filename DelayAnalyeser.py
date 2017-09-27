from __future__ import division
import csv


STATE_0 = 0
STATE_1 = 1
STATE_2 = 2
STATE_3 = 3
STATE_INCONSISTENT = 4

ACTION_GOING_UP_LATE = "up_late"
ACTION_GOING_UP_FORWARD = "up_forward"
ACTION_GOING_DOWN_LATE = "down_late"
ACTION_GOING_DOWN_FORWARD = "down_forward"
ACTION_PASS = "pass"

UP = "up"
DOWN = "down"
LATE = 1
FORWARD = -1

# Usage: new_state = state_transition_table[previous_state][new_reading]
state_transition_table = [[STATE_0, STATE_1, STATE_2, STATE_INCONSISTENT],
                          [STATE_0, STATE_1, STATE_INCONSISTENT, STATE_3],
                          [STATE_0, STATE_INCONSISTENT, STATE_2, STATE_3],
                          [STATE_INCONSISTENT, STATE_1, STATE_2, STATE_3],
                          [STATE_0, STATE_INCONSISTENT, STATE_INCONSISTENT, STATE_3]]

# Usage: new_action = action_table[previous_state][new_state]
action_table = [[ACTION_PASS, ACTION_GOING_UP_LATE, ACTION_GOING_UP_FORWARD, ACTION_PASS, ACTION_PASS],
                [ACTION_PASS, ACTION_PASS, ACTION_PASS, ACTION_PASS, ACTION_PASS],
                [ACTION_PASS, ACTION_PASS, ACTION_PASS, ACTION_PASS, ACTION_PASS],
                [ACTION_PASS, ACTION_GOING_DOWN_FORWARD, ACTION_GOING_DOWN_LATE, ACTION_PASS, ACTION_PASS],
                [ACTION_PASS, ACTION_PASS, ACTION_PASS, ACTION_PASS, ACTION_PASS]]

unit_conversion = {
    'Mn': 0,  # use 0 to discard values in this scale
    's': 10 ** 6,
    'ms': 10 ** 3,
    'us': 10 ** 0,
    'ns': 10 ** (-3),
}



if __name__ == "__main__":

    input_filename = 'Data/long_test_4.csv'
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

        previous_state = STATE_INCONSISTENT

        for row in reader:
            new_reading = int(row[1])
            new_state = state_transition_table[previous_state][new_reading]
            new_action = action_table[previous_state][new_state]

            previous_state = new_state

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

            if new_action != ACTION_PASS:
                delay_us = timing * float(row[2])*unit_conversion[row[3]]
                writer.writerow([delay_us])


        # for row in reader:
        #     if row[1] == '1':
        #         direction = POSITIVE
        #         alt = False
        #     elif row[1] == '2':
        #         direction = NEGATIVE
        #         alt = False
        #     elif row[1] == '3':
        #         direction = POSITIVE
        #         alt = True
        #     elif row[1] == '0':
        #         direction = NEGATIVE
        #         alt = True
        #     else:
        #         direction = PASS
        #         alt = 0
        #
        #
        #     if direction == POSITIVE or direction == NEGATIVE:
        #         delay_us = direction*float(row[2])*unit_conversion[row[3]]
        #         print("{} -> {}".format(row, delay_us))
        #
        #         if alt:
        #             alt_writer.writerow([delay_us])
        #         else:
        #             writer.writerow([delay_us])
        #
        #     else:
        #         print("{}".format(row))
        #
        #         # with open('output_filename', 'r') as output_file:
        #         #     reader = csv.reader(output_file)
        #         #     for row in reader:
        #         #         print row
