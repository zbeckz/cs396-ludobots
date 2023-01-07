import numpy as np
import matplotlib.pyplot

backLegSensorValues = np.load("data/backLegSensorValues.npy")
matplotlib.pyplot.plot(backLegSensorValues)
matplotlib.pyplot.show()