import pandas as pd
import csv
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt

from analyse import Analyse

sns.set_theme()

class Graph:
    
    def __init__(self,file):
        self.file = file
        self.data = ''
        self.cols_max_min = {}
        
    def get_file_content(self):
        self.data = pd.read_csv(self.file)
        return self.data
        
    def get_max_column_value(self):
        data = self.get_file_content()
        for col in data.columns:
            self.cols_max_min[col + "_max"] = round(data[col],-2).max()
            self.cols_max_min[col + "_min"] = round(data[col],-2).min()
        return self.cols_max_min
        
    def get_x_range(self): 
        self.get_file_content()
        self.get_max_column_value()
        x_max = self.cols_max_min[self.data.columns[0] + "_max"]
        x_min = self.cols_max_min[self.data.columns[0] + "_min"]
        return x_max, x_min
    
    def get_y_range(self):
        self.get_file_content()
        self.get_max_column_value()
        y_max = self.cols_max_min[self.data.columns[1] + "_max"]
        y_min = self.cols_max_min[self.data.columns[1] + "_min"]
        return y_max, y_min
        
        
class HeatMap(Graph):
    
    def __init__(self,file):
        # self.file = file
        super().__init__(file)
        self.x_range = (0,0)
        self.y_range = (0,0)
        self.base_heatmap = np.zeros((1,1))
                
    def create_base_heatmap(self):
        self.x_range = super().get_x_range()
        self.y_range = super().get_y_range()
        number_of_x_blocks = (self.x_range[0] - self.x_range[1])/100
        number_of_y_blocks = (self.y_range[0] - self.y_range[1])/100
        print(number_of_x_blocks,number_of_y_blocks)
        self.base_heatmap = np.full((int(number_of_y_blocks),int(number_of_x_blocks)),0, dtype=int)
        
    def fill_heatmap(self):
        data = super().get_file_content()
        columns = data.columns
        print(f'OLD: {self.base_heatmap}')
        for index, row in data.iterrows():
            x_coord = round(row[columns[0]] - self.x_range[1],-2) / 100 - 1
            y_coord = round(row[columns[1]] - self.y_range[1],-2) / 100 - 1
            # print(f'index: {index}, row: {row[columns[0]]} {row[columns[1]]}, x_coord: {x_coord},y_coord: {y_coord}')
            self.base_heatmap[int(y_coord)][int(x_coord)] += 1
            # break
            # print(round(row[columns[0]],-2), round(row[columns[1]],-2))
        print(f'NEW: {self.base_heatmap}')
        ax = sns.heatmap(self.base_heatmap)
        plt.show()
        
class BarGraph:
    
    def __init__(self, data):
        self.data = data
        
    def draw_bar_graph(self):
        x_ref = list(self.data.keys())
        y_ref = list(self.data.values())
                
        x_pos = [i for i, _ in enumerate(x_ref)]
        plt.bar(x_pos,y_ref,color='green')
        plt.xlabel('Stagnation period (s)')
        plt.ylabel('Frequency')
        plt.xticks(x_pos,x_ref)
        plt.show()
        
mouse_heatmap = HeatMap("./track4.csv")
mouse_heatmap.create_base_heatmap()
mouse_heatmap.fill_heatmap()

analysis = Analyse("./track4.csv")
analysis.get_file_content()

mouse_bar_chart = BarGraph(analysis.get_mouse_movement_duration_by_frequency())
mouse_bar_chart.draw_bar_graph()
