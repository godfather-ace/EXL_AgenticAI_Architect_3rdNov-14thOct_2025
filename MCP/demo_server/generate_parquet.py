import pandas as pd

df = pd.read_csv("data/sample.csv")

df.to_parquet("data/sample.parquet", index = False)