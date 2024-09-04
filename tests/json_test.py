import pandas as pd

df = pd.read_csv('../joyinst/curriculum.csv', header=None)

# df_filtered = df.dropna(how='any')
# df = df.stack().unstack()
# print(df.values.tolist())

reader = df.values.tolist()

import csv

# with open('../joyinst/curriculum.csv', mode='r') as infile:
#     reader = csv.reader(infile, dialect='excel', skipinitialspace=True)
#     # print(reader)
learning_dict = []
for rows in reader:
    level_notes = []
    for note in rows:
        if note == note:
            level_notes.append(note)
    learning_dict.append(level_notes)
    # print(level_notes)
print(learning_dict)
# for level in learning_dict:
#     print(level)