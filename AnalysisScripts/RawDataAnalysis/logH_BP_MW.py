import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("Data/Combined/0.0.1-hT_withRDKitDesc.csv")
df.dropna(subset=["MolWt"], inplace=True)
df = df[df["MolWt"] < 1000]

df.dropna(subset=["logHenry"], inplace=True)

df.dropna(subset=["BoilingPoint/C"], inplace=True)
df = df[df["BoilingPoint/C"]<600]


MolWt = df["MolWt"].values.astype(float)
logH = df["logHenry"].values.astype(float)
bp = df["BoilingPoint/C"].values.astype(float)

fig = plt.figure(figsize=(8, 8))
ax = fig.add_subplot(projection='3d')
ax.scatter(MolWt, logH, bp, marker='o', alpha=0.6, cmap="viridis", c=bp)
plt.xlabel("Molecular Weight"); plt.ylabel("logHenry"); ax.set_zlabel("Boiling Point")
ax.set_box_aspect(None, zoom = 0.9)
plt.title("Boiling Point vs Molecular Weight vs logHenry")
plt.show()