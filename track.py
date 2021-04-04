from pymouse import PyMouse
import csv
import time
import os.path
import keyboard
import string
import multiprocessing

class Track:

    def __init__(self,period,storage_type,forever,mouse_file_path=None,keyboard_file_path=None):
        self.period = period
        self.storage_type = storage_type
        self.forever = forever
        if storage_type == 'file':
            self.mouse_file_path = mouse_file_path
        self.keyboard_file_path = keyboard_file_path

    def track_mouse(self):
        """
        Tracks your mouse movement every 'given' time period and saves in a csv
        """
        m = PyMouse()
        while(self.forever):
            file = open(self.mouse_file_path,'a',newline='')
            header = ['x','y']
            writer = csv.DictWriter(file,fieldnames=header)
            with file:
                if os.path.exists(self.mouse_file_path) == False:
                    # header = ['x','y']
                    # writer = csv.DictWriter(file,fieldnames=header)
                    writer.writeheader()
                writer.writerow({'x':m.position()[0], 'y':m.position()[1]})
            print(f'Tracking your mouse movement every {self.period} seconds')
            time.sleep(self.period)

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


if __name__ == '__main__':
    track = Track(3,'file',True,'/home/doug/Desktop/track/track.csv','/home/doug/Desktop/track/keys.txt')
    mouse_process = multiprocessing.Process(name='mouse_process', target=track.track_mouse)
    keyboard_process = multiprocessing.Process(name='keyboard_process', target=track.track_keyboard)
    mouse_process.start()
    keyboard_process.start()
