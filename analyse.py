import pandas as pd
import csv
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
import math

class Analyse:

    def __init__(self,file):
        self.file = file
        self.data = ''
        self.gradient = []

    def get_file_content(self):
        self.data = pd.read_csv(self.file)
        return self.data

    def get_gradient(self):
        x_coords = self.data[self.data.columns[0]].to_numpy()
        y_coords = self.data[self.data.columns[1]].to_numpy()
        for i in range(len(x_coords) - 1):
            if i+1 <= len(x_coords):
                if (y_coords[i+1] - y_coords[i]) == 0:
                    self.gradient.append(0)
                else:
                    gradient = (y_coords[i+1] - y_coords[i])/(x_coords[i+1] - x_coords[i])
                    self.gradient.append(gradient)
        # print(f'gradient: {self.gradient[:10]}, max: {max(self.gradient)}, min: {min(self.gradient)}')
        return self.gradient

    def get_gradient_count_by_type(self):
        self.get_gradient()
        negative_gradients, neutral_gradients, positive_gradients = [], [], []
        for i in self.gradient:
            if i < 0:
                negative_gradients.append(i)
            elif i == 0:
                neutral_gradients.append(i)
            else:
                positive_gradients.append(i)
        print(f'neg: {len(negative_gradients)}, neu: {len(neutral_gradients)}, pos: {len(positive_gradients)}')
        return len(negative_gradients), len(neutral_gradients), len(positive_gradients)

    def get_negative_gradients(self):
        negative_gradients = [i for i in self.gradient if i < 0]
        return negative_gradients

    def get_neurtal_gradients(self):
        neutral_gradients = [i for i in self.gradient if i == 0]
        return neutral_gradients

    def get_positive_gradients(self):
        positive_gradients = [i for i in self.gradient if i > 0]
        return positive_gradients

    def compute_magnitude(self, delta_x, delta_y):
        magnitude = math.sqrt(delta_x**2 + delta_y**2)
        return magnitude

    def compute_direction(self, delta_x, delta_y):
        direction_rad = math.atan(abs(delta_y)/abs(delta_x))
        direction_deg = direction_rad*180/math.pi % 360
        return {"rad":direction_rad, "deg":direction_deg}

    def get_movement_direction(self):
        """
        Computes the magnitude and direction of the mouse movement with the starting point as the origin,
        using trigonometry
        """
        magnitude = []
        direction = []
        x_coords = self.data[self.data.columns[0]].to_numpy()
        y_coords = self.data[self.data.columns[1]].to_numpy()
        for i in range(len(x_coords) -1):
            delta_x = x_coords[i+1] - x_coords[i]
            delta_y = y_coords[i+1] - y_coords[i]
            if delta_x == 0 and delta_y == 0:
                magnitude.append(0)
                direction.append(0)
                continue
            elif delta_x == 0 and delta_y < 0:
                magnitude.append(abs(delta_y))
                direction.append(90)
                continue
            elif delta_x == 0 and delta_y > 0:
                magnitude.append(delta_y)
                direction.append(270)
                continue
            elif delta_x < 0 and delta_y == 0:
                magnitude.append(abs(delta_x))
                direction.append(180)
                continue
            elif delta_x > 0 and delta_y == 0:
                magnitude.append(delta_x)
                direction.append(0)
                continue
            elif delta_x > 0 and delta_y < 0:
                direction.append(self.compute_direction(delta_x,delta_y)["deg"])
            elif delta_x < 0 and delta_y < 0:
                direction.append(180 - self.compute_direction(delta_x,delta_y)["deg"])
            elif delta_x < 0 and delta_y > 0:
                direction.append(180 + self.compute_direction(delta_x,delta_y)["deg"])
            else:
                direction.append(360 - self.compute_direction(delta_x,delta_y)["deg"])
            magnitude.append(self.compute_magnitude(delta_x,delta_y))
        '''
        If change in y = 0 and change in x = 0 then angle = 0
        if change in y = 0 and change in x != 0 then angle = 180
        if change in x is > 0 and change in y < 0 then angle is between 0 and 90
        if change in x is < 0 and change in y < 0  then angle is between 90 and 180
        if change in x is < 0 and change in y > 0 then angle is between 90 and 270
        if change in x is > 0 and chang ein y > 0 then angle is between 270 and 360
        Will have to find out x,y of each corner of screen
        '''
        return {"magnitude":magnitude, "direction":direction}

    def get_magnitude_by_frequency(self):
        """
        Group the mouse movements by magnitude

        Returns:
            frequency (dict): Frequency of mouse movement by magnitude,
            eg: {'+0': 395, '+100': 129, '+1000': 44, '+2000': 38}
        """
        frequency = {"+0": 0, "+100": 0, "+1000": 0, "+2000": 0}
        magnitude = self.get_movement_direction()["magnitude"]
        for i in magnitude:
            if i >= 2000:
                frequency["+2000"] += 1
            elif i >= 1000:
                frequency["+1000"] += 1
            elif i >= 100:
                frequency["+100"] += 1
            else:
                frequency["+0"] += 1
        print(frequency)
        return frequency

    def get_direction_by_frequency(self):
        """
        Group the mouse movements by direction

        Returns:
            frequency (dict): Frequency of mouse movement by direction,
            eg: {'+0': 453, '+90': 38, '+180': 83, '+270': 32}
        """
        frequency = {"+0": 0, "+90": 0, "+180": 0, "+270": 0}
        direction = self.get_movement_direction()["direction"]
        for i in direction:
            if i >= 270:
                frequency["+270"] += 1
            elif i >= 180:
                frequency["+180"] += 1
            elif i >= 90:
                frequency["+90"] += 1
            else:
                frequency["+0"] += 1
        print(frequency)
        return frequency


    def get_mouse_movement_duration_by_frequency(self):
        """
        Group mouse movement by stagnant duration, ie how long does the mouse stay at the same position?
        
        Returns:
            frequency (dict): Frequency of mouse stagnation by time,
            eg: {'+0': 312, '+2': 53, '+4': 29, '+6': 18, '+8': 10, '+10': 5, '>10': 21}
        """
        frequency = {"+0": 0, "+2": 0, "+4": 0, "+6": 0, "+8": 0, "+10": 0, ">10": 0}
        x_coords = self.data[self.data.columns[0]].to_numpy()
        y_coords = self.data[self.data.columns[1]].to_numpy()
        time = 0
        
        for i in range(len(x_coords)):
            if i < len(x_coords) - 1 and (x_coords[i + 1] == x_coords[i]) and (y_coords[i + 1] == y_coords[i]):
                time += 1
            else:
                if time == 0: 
                    frequency["+0"] += 1
                elif time == 1: 
                    frequency["+2"] += 1
                elif time == 2:
                    frequency["+4"] += 1
                elif time == 3:
                    frequency["+6"] += 1
                elif time == 4:
                    frequency["+8"] += 1
                elif time == 5:
                    frequency["+10"] += 1
                else:
                    frequency[">10"] += 1
                time = 0
        print(f'freq: {frequency}')
        return frequency

analyse = Analyse("./TRACK_FOREVER.csv")
analyse.get_file_content()
analyse.get_gradient_count_by_type()
# analyse.get_magnitude_by_frequency()
# analyse.get_direction_by_frequency()
# analyse.get_mouse_movement_duration_by_frequency()