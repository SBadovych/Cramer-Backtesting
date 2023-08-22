import pandas as pd
import os

directory = r'C:\Users\Steven\PycharmProjects\InverseCramer\CSV Files'

files = [os.path.join(directory, file) for file in os.listdir(directory)]

df1 = pd.concat(map(pd.read_csv, files), ignore_index=True)

df1.to_csv('CramerCalls.csv', index=False)

print("CSV files combined successfully. Output file created: CramerCalls.csv")