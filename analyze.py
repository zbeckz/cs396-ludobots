import numpy as np
import matplotlib.pyplot as plt
import os

# get all the files containing data
files = os.listdir("FitnessData")
if len(files) == 0:
    print("NO DATA TO ANALYZE")
    exit()

# set up dictionaries for appropriate plotting
plotSpecs = {
    '2': {
        'color': 'b-',
        'first': True,
        'vals': []
    },
    
    '4': {
        'color': 'g-',
        'first': True,
        'vals': []
    },
}

# loop through the filenames
for file in files:
    
    # get the metadata for the legend
    splitFile = file.split("_")
    numLegs = splitFile[2]
    numGenerations = int(splitFile[1])
    label = numLegs + " Legs"

    # open the file
    with open(f"FitnessData/{file}") as f:
        data = np.zeros(numGenerations + 1)
        i = 0
        
        # read the data in
        for line in f:
            num = line.split("\n")[0]
            if num != '':
                data[i] = float(num)
                i += 1

        plotSpecs[numLegs]['vals'].append(data[numGenerations])

        # plot
        if plotSpecs[numLegs]['first']:
            plt.plot(data, plotSpecs[numLegs]['color'], label=label, linewidth=0.5)
            plotSpecs[numLegs]['first'] = False
        else:
            plt.plot(data, plotSpecs[numLegs]['color'], linewidth=0.5)

# construct confidence intervals
for n in ['2', '4']:
    if not plotSpecs[n]['first']:
        data = plotSpecs[n]['vals']
        mean = np.mean(data)
        std = np.std(data)

        # print statistics
        print(f"{n} Legs Mean:               {mean}")
        print(f"{n} Legs Standard Deviation: {std}\n")

        # plot confidence interval
        plt.plot(np.full(numGenerations + 1, mean + 1.96*std/np.sqrt(len(data))), f"{plotSpecs[n]['color']}-", alpha=0.5, linewidth=1.5, label=f"{n} Legs Confidence Interval")
        plt.plot(np.full(numGenerations + 1, mean - 1.96*std/np.sqrt(len(data))), f"{plotSpecs[n]['color']}-", alpha=0.5, linewidth=1.5)

# format
plt.ylabel("Fitness")
plt.xlabel("Generation Number")
plt.title(input("Enter Plot Title: "))
plt.legend()

# save the figure
figNumber = len(os.listdir("FitnessCurves")) + 1
plt.savefig(f"FitnessCurves/Curve{figNumber}.png")