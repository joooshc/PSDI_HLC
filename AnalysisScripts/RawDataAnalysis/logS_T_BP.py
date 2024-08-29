import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("Data/Combined/0.0.0-hasTemperature.csv")
df.dropna(subset=["Temperature"], inplace=True)
df = df[df["Temperature"] < 200]

df.dropna(subset=["BoilingPoint/C"], inplace=True)
df = df[df["BoilingPoint/C"]<600]

df.dropna(subset=["logS"], inplace=True)
df = df[df["logS"] != "TolError"]


temps = df["Temperature"].values.astype(float)
bp = df["BoilingPoint/C"].values.astype(float)
logS = df["logS"].values.astype(float)

fig = plt.figure(figsize=(8, 8))
ax = fig.add_subplot(projection='3d')
ax.scatter(temps, bp, logS, marker='o', alpha=0.6, cmap="viridis", c=logS)
plt.ylabel("Boiling Point"); plt.xlabel("Temperature"); ax.set_zlabel("logS")
ax.set_box_aspect(None, zoom = 0.9)
plt.title("logS vs Temperature vs Boiling Point")
plt.show()

# Try clustering on this one