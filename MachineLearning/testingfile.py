import json

with open('MachineLearning/TrainingInfo.json') as f:
  data = json.load(f)
f.close()

print(data)
print(data.keys())
print(data["logS"]["scaling"])