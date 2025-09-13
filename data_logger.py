import csv
from datetime import datetime

def append_event(csv_path, row):
    with open(csv_path, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(row)

if __name__ == '__main__':
    # Example: append a new event
    sample = [
        datetime.now().isoformat(), 'u1', 't999', 'exercise', 'completed',
        datetime.now().isoformat(), 20, '{}'
    ]
    append_event('user_behavior_log.csv', sample)
    print('Appended sample event')