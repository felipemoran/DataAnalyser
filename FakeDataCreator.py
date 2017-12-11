import csv


with open("Data/fake_raw.csv", 'w') as fake_file:
    writer = csv.writer(fake_file)

    writer.writerow(['Sample#','group1','SampleTime','units'])
    counter = 0

    for i in range(10):
        writer.writerow([counter, 0, 499.5, 'ms'])
        counter += 1
        writer.writerow([counter, 1, 500, 'us'])
        counter += 1
        writer.writerow([counter, 3, 499.5, 'ms'])
        counter += 1
        writer.writerow([counter, 2, 500, 'us'])
        counter += 1


    for i in range(10):
        writer.writerow([counter, 0, 499.5, 'ms'])
        counter += 1
        writer.writerow([counter, 2, 500, 'us'])
        counter += 1
        writer.writerow([counter, 3, 499.5, 'ms'])
        counter += 1
        writer.writerow([counter, 1, 500, 'us'])
        counter += 1
