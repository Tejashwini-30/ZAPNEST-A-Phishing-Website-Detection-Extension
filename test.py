import pandas as pd
df = pd.read_csv("backend/data/PhiUSIIL_Phishing_URL_Dataset.csv")
print(df["label"].value_counts())
print(df.head(5)[["URL","label"]])
