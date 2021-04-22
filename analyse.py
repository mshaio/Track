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
        print(self.data.head())
        print(len(self.data))
        x_coords = self.data[self.data.columns[0]].to_numpy()
        y_coords = self.data[self.data.columns[1]].to_numpy()
        for i in range(len(x_coords) - 1):
            if i+1 <= len(x_coords):
                if (y_coords[i+1] - y_coords[i]) == 0:
                    self.gradient.append(0)
                else:
                    gradient = (x_coords[i+1] - x_coords[i])/(y_coords[i+1] - y_coords[i])
                    self.gradient.append(gradient)
        print(f'gradient: {self.gradient[:10]}, max: {max(self.gradient)}, min: {min(self.gradient)}')
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
    
    def get_movement_direction(self):
        """
        Computes the magnitude and direction of the mouse movement with the starting point as the origin
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
            elif delta_x != 0 and delta_y == 0:
                magnitude.append(delta_x)
                pass
            
            if delta_x > 0 and delta_y < 0:
                magnitude.append()
        '''
        If change in y = 0 and change in x = 0 then angle = 0
        if change in y = 0 and change in x != 0 then angle = 180
        if change in x is > 0 and change in y < 0 then angle is between 0 and 90
        if change in x is < 0 and change in y < 0  then angle is between 90 and 180
        if change in x is < 0 and change in y > 0 then angle is between 90 and 270
        if change in x is > 0 and chang ein y > 0 then angle is between 270 and 360
        Will have to find out x,y of each corner of screen
        '''
        return
        
    def compute_magnitude(self, delta_x, delta_y):
        magnitude = math.sqrt(delta_x**2 + delta_y**2)
        return magnitude
    
    def compute_direction(self, delta_x, delta_y):
        direction_rad = math.tan(delta_y/delta_x)
        direction_deg = direction_rad*180/math.pi
        return direction_rad, direction_deg
            
    def get_mouse_movement_duration(self):
        """
        Computes the mouse movement duration, including move up/down, 
        """
        pass
        
analyse = Analyse("./track.csv")
analyse.get_file_content()
analyse.get_gradient_count_by_type()