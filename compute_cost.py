import numpy as np
import pandas as pd

INPUT = 0.0015
OUPUT = 0.002
US_TO_RMB = 7.2

df = pd.read_csv("openai_usage.txt", names=['input', 'output', 'timestamps'])
df = df.drop(columns=['timestamps'])
data = df.values

total_in = np.sum(data[:, 0])
total_out = np.sum(data[: 1])
total_cost = (total_in * INPUT + total_out * OUPUT) / 1000

print(f'Prompt Tokens: {total_in}\n' +
      f'Completion Tokens: {total_out}\n' +
      f'USD: {total_cost}\n' +
      f'RMB: {total_cost * US_TO_RMB}')
