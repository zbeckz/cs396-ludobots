import numpy as np
import matplotlib.pyplot as plt
import os

# get all the files containing data
files = os.listdir("FitnessData")
if len(files) == 0:
    print("NO DATA TO ANALYZE")
    exit()

firstBlue = True
firstGreen = True
firstRed = True
firstYellow = True

# loop through the filenames
for file in files:
    
    # get the metadata for the legend
    numLegs = file.split("_")[2]
    label = numLegs + " Legs"

    # read the data in
    with open(f"FitnessData/{file}") as f:
        data = []
        for line in f:
            num = line.split("\n")[0]
            if num != '':
                data.append(float(num))
        if numLegs == '2':
            color = "b-"
            if firstBlue:
                plt.plot(data, color, label=label)
                firstBlue = False
            else:
                plt.plot(data, color)
        elif numLegs == '4':
            color = "g-"
            if firstGreen:
                plt.plot(data, color, label=label)
                firstGreen = False
            else:
                plt.plot(data, color)
        elif numLegs == '6':
            color = "r-"
            if firstRed:
                plt.plot(data, color, label=label)
                firstRed = False
            else:
                plt.plot(data, color)
        else:
            color = "y-"
            if firstYellow:
                plt.plot(data, color, label=label)
                firstYellow = False
            else:
                plt.plot(data, color)
        

# format and plot
plt.ylabel("Fitness")
plt.xlabel("Generation Number")
plt.title("25 Creature, 200 Generation Fitness Curves")
plt.legend()

# save the figure
figNumber = len(os.listdir("FitnessCurves")) + 1
plt.savefig(f"FitnessCurves/Curve{figNumber}.png")