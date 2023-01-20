import numpy as np
import constants as c
import pyrosim.pyrosim as pyrosim

class SENSOR:

    def __init__(self, linkName):
        self.linkName = linkName
        self.Prepare_To_Sense()

    def Prepare_To_Sense(self):
        self.values = np.zeros(c.iterations)

    def Get_Value(self, step, counter):
        self.values[step] = pyrosim.Get_Touch_Sensor_Value_For_Link(self.linkName)

        # this is to induce oscillatory behavior
        if c.oscillatory and counter == 1: # 1 because that means this is the torso sensor
            self.values[step] = np.sin(c.x * step)

    def Save_Values(self):
        np.save("data/" + self.linkName + "SensorValues", self.values)