import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("Data/Combined/LargeFiles/HasDescriptors/0.0.0-hT_withRDKitDesc.csv")
df.dropna(subset=["logHenry"], inplace=True)

df.dropna(subset=["logS"], inplace=True)
df = df[df["logS"] != "TolError"]

df.dropna(subset=["MolLogP"], inplace=True)

logP = df["MolLogP"].values.astype(float)
logH = df["logHenry"].values.astype(float)
logS = df["logS"].values.astype(float)

fig = plt.figure(figsize=(8, 8))
ax = fig.add_subplot(projection='3d')
ax.scatter(logP, logH, logS, marker='o', alpha=0.6, cmap="viridis", c=logS)
plt.xlabel("logP"); plt.ylabel("logHenry"); ax.set_zlabel("logS")
ax.set_box_aspect(None, zoom = 0.9)
plt.title("logS vs logP vs logHenry")
plt.show()