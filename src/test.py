import pandas as pd
import numpy as np
from final_model import DEnsembleModel

df = pd.read_csv(
    "/Users/zed/AI_Lab/DoubleEnsembleML/Data/data_factor/BTC_fac.csv")
df = df.drop(["Target_value", "Date"], axis=1)


model = DEnsembleModel()
model.fit(df)

model.predict(df)
