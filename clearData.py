import os

# get all the files containing data
for file in os.listdir("FitnessData"):
    os.system(f"del FitnessData\{file}")

for file in os.listdir("FitnessCurves"):
    os.system(f"del FitnessCurves\{file}")