from pymouse import PyMouse
import csv
import time
import os.path
import keyboard
import string
import multiprocessing
import redis
import json

class Track:
    
    def __init__(self,period,storage_type,forever,mouse_file_path=None,keyboard_file_path=None,track_duration_per_dataset=1000,track_cycle_count=10):
        self.period = period
        self.storage_type = storage_type
        self.forever = forever
        if storage_type == 'file':
            self.mouse_file_path = mouse_file_path
        if storage_type == 'db':
            self.redis_client = redis.StrictRedis(host='localhost', port=6379)
        self.keyboard_file_path = keyboard_file_path
        self.track_duration_per_dataset = track_duration_per_dataset #Not in seconds but in numeber of rows
        self.track_cycle_count = track_cycle_count

    def store_mouse_data(self,suffix,redis_active=False, postgres_active=False):
        """
        Stores your mouse movement data every given time period and saves in a csv
        """
        m = PyMouse()

        if redis_active or postgres_active:
            
            if redis_active:

                # Convert the data to a string
                if self.redis_client.get('mouse') is not None:
                    print(f'redis: {json.loads(self.redis_client.get("mouse"))}')
                    mouse_data = json.loads(self.redis_client.get('mouse'))
                    mouse_data_x = mouse_data['x']
                    mouse_data_y = mouse_data['y']
                    print(f'x0: {mouse_data_x}, y0: {mouse_data_y}')
                    
                    mx = m.position()[0]
                    my = m.position()[1]
                    print(f'mx: {mx}, my: {my}')
                    print(mouse_data_x, mouse_data_x.append(mx))

                    data_cache = {}
                    mouse_data_x.append(mx)
                    data_cache['x'] = [m.position()[0]]
                    data_cache['y'] = [m.position()[1]]
                    print(f'x1: {data_cache["x"]}, y1: {data_cache["y"]}, data_cache: {data_cache}')
                    self.redis_client.set('mouse', json.dumps(data_cache))
                else:
                    print("B")
                    data_cache = {}
                    data_cache['x'] = [m.position()[0]]
                    data_cache['y'] = [m.position()[1]]
                    self.redis_client.set('mouse', json.dumps(data_cache))

                

                print(f'Tracking your mouse movement every {self.period} seconds, in memory')
        else:
            file = open(self.mouse_file_path + str(suffix) + ".csv",'a',newline='')
            header = ['x','y']
            writer = csv.DictWriter(file,fieldnames=header)
            with file:
                if os.path.exists(self.mouse_file_path + str(suffix) + ".csv") == False:
                    # header = ['x','y']
                    # writer = csv.DictWriter(file,fieldnames=header)
                    writer.writeheader()
                writer.writerow({'x':round(m.position()[0]), 'y':round(m.position()[1])})
            print(f'Tracking your mouse movement every {self.period} seconds, in csv format')
        time.sleep(self.period)
        
    def track_mouse(self, redis_active=False, postgres_active=False):
        """
        Tracks your mouse movement every so often based on the options you've set
        Defaults to 1 data point for every 2 seconds until 1000 data points and 
        repeats 10 times, ie total tracking time of approximately 5.5h
        """
        if (self.forever == True):
            while(self.forever):
                self.store_mouse_data("FOREVER",redis_active,postgres_active)
        else:
            for cycle in range(self.track_cycle_count):
                for count in range(self.track_duration_per_dataset):
                    self.store_mouse_data(cycle)
            
    def track_keyboard(self):
        """
        Tracks your keyboard presses in the given file.
        """
        while (self.forever):
            #Instead of writing to a file, write to RAM (redis) and then copy to file every so often
            file = open(self.keyboard_file_path,'a')
            file.write(keyboard.read_key() + ',')
            file.close()
            print(f'You clicked the key {keyboard.read_key()}')

    @staticmethod
    def test():
        print("Tracking Test")

if __name__ == '__main__':
    track = Track(2,'db',True,'/Users/markshaio/Desktop/TRACK_','/Users/markshaio/Desktop/KEYS.txt')
    mouse_process = multiprocessing.Process(name='mouse_process', target=track.track_mouse(redis_active=True, postgres_active=False))
    keyboard_process = multiprocessing.Process(name='keyboard_process', target=track.track_keyboard)
    mouse_process.start()
    keyboard_process.start()
