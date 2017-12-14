from __future__ import division
import csv
import time


def us2string(us):
    hours, rem = divmod(us/1000000, 3600)
    minutes, seconds = divmod(rem, 60)
    return"{:0>2}h{:0>2}m{:02.0f}s".format(int(hours), int(minutes), seconds)


STATE_INCONSISTENT = 4

ACTION_GOING_UP_LATE      = 10
ACTION_GOING_UP_EARLY     = 11
ACTION_GOING_DOWN_LATE    = 12
ACTION_GOING_DOWN_EARLY   = 13
ACTION_PASS               = 14
ACTION_ALERT              = 15
ACTION_TRANSITION         = 16

UP    = "up"
DOWN  = "down"
LATE  = 1
EARLY = -1
PASS  = 0

SKIP_FIRST_ROWS = True
ROWS_TO_SKIP = 10

action_decision_table = []
for i in range(4):
    action_decision_table.append([])
    for j in range(4):
        action_decision_table[i].append([])
        for k in range(4):
            action_decision_table[i][j].append(ACTION_ALERT)

action_decision_table[0][1][3] = ACTION_GOING_UP_EARLY
action_decision_table[0][2][3] = ACTION_GOING_UP_LATE
action_decision_table[3][2][0] = ACTION_GOING_DOWN_EARLY
action_decision_table[3][1][0] = ACTION_GOING_DOWN_LATE

action_decision_table[1][0][1] = ACTION_TRANSITION
action_decision_table[1][0][2] = ACTION_TRANSITION
action_decision_table[2][0][1] = ACTION_TRANSITION
action_decision_table[2][0][2] = ACTION_TRANSITION

action_decision_table[1][3][1] = ACTION_TRANSITION
action_decision_table[1][3][2] = ACTION_TRANSITION
action_decision_table[2][3][1] = ACTION_TRANSITION
action_decision_table[2][3][2] = ACTION_TRANSITION


unit_conversion = {
    'Mn': 0,  # use 0 to discard values in this scale
    's': 10 ** 6,
    'ms': 10 ** 3,
    'us': 10 ** 0,
    'ns': 10 ** (-3),
}


def process_gologic_csv(filename):
    start = time.time()

    input_filename = 'Data/' + filename + '_gologic.csv'
    output_filename = input_filename.rsplit('.', 1)
    output_filename[0] += '_output'
    output_filename = output_filename[0] + '-3.0.csv'

    with open(input_filename, 'r') as raw_file, open(output_filename, 'w') as output_file:
        reader = csv.reader(raw_file)
        writer = csv.writer(output_file)
        next(reader)  # skip header row

        writer.writerow(['delay_us', 'accumulated_us'])

        accumulated_us = 0

        previous_row = next(reader)
        reading_history = [0, 0, 0, 0]

        late_counter = 0
        early_counter = 0
        row_counter = 0
        alert_counter = 0

        for row in reader:
            row_counter += 1

            reading_history.append(int(row[1]))
            reading_history.pop(0)

            new_action = action_decision_table[reading_history[1]][reading_history[2]][reading_history[3]]

            if SKIP_FIRST_ROWS and row_counter < ROWS_TO_SKIP:
                continue

            duration = float(previous_row[2])*unit_conversion[previous_row[3]]
            previous_row = row

            if new_action == ACTION_GOING_UP_LATE or new_action == ACTION_GOING_DOWN_LATE:
                timing = LATE
                late_counter += 1
            elif new_action == ACTION_GOING_UP_EARLY or new_action == ACTION_GOING_DOWN_EARLY:
                timing = EARLY
                early_counter += 1

            elif new_action == ACTION_TRANSITION:
                if reading_history[0] == reading_history[2]:
                    # seems to be some inconsistent data. I'll just flag as it was
                    new_action = ACTION_ALERT
                else:
                    new_action = ACTION_PASS

            if new_action == ACTION_ALERT:
                alert_counter += 1
                text = "Going to inconsistent state! Instant {}, counter {}/{} ({:.2f}%), history 0:{} 1:{} 2:{} ".format(us2string(accumulated_us), alert_counter, row_counter, alert_counter/row_counter*100, reading_history[0], reading_history[1], reading_history[2])
                print(text)
                timing = None
            elif new_action == ACTION_PASS:
                timing = None

            accumulated_us += duration

            if timing is None:
                continue

            delay_us = timing * duration
            writer.writerow([delay_us, accumulated_us])

    elapsed = time.time() - start
    print("{} rows processed in {:.2f} seconds".format(row_counter, elapsed))

if __name__ == "__main__":
    process_gologic_csv('gps_mote_long')
