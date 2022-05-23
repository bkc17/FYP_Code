import os
import time
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random
import datetime as dt
import threading
import pygatt
import time


file_path = "C:\\Users\\bhara\\workspace_v8\\LabView\\Data\\test.txt"

def get_data():
    x = random.randint(0,10)
    y = random.randint(0, 5)

    return x,y

def follow(thefile):
    '''generator function that yields new lines in a file
    '''
    # seek the end of the file
    thefile.seek(0, os.SEEK_END)
    
    # start infinite loop
    while True:
        # read last line of file
        line = thefile.readline()
        # sleep if file hasn't been updated
        if not line:
            time.sleep(0.01)
            continue
        yield line

def plot_update_file(i, xs, y_rot_speed, y_grad):
    # logfile = open(file_path,"r")
    # line = logfile.readlines()[-1]
    # logfile.close()
    
    # with open(file_path) as f:
    #     for line in f:
    #         pass
    #     last_line = line
    # vdd, temp, rot_speed, grad = last_line.split("\t")[:-1]

    rot_speed, grad = get_data()
    y_rot_speed.append(rot_speed)
    y_grad.append(grad)

    xs.append(dt.datetime.now().strftime('%H:%M:%S.%f')[:-5])
    xs = xs[-10:]
    y_rot_speed = y_rot_speed[-10:]
    y_grad = y_grad[-10:]
    
    ax.clear()
    ax.plot(xs, y_rot_speed)
    ax.tick_params(labelrotation=45)
    ax.set_title('Rotation Speed (rads/sec)')

    ax2.clear()
    ax2.plot(xs, y_grad)
    ax2.tick_params(labelrotation=45)
    ax2.set_title('Gradient (rads/$s^2$)')

    fig.tight_layout()

def main():
    # logfile = open(file_path,"r")
    # loglines = follow(logfile)
    
    # for line in loglines:

    #     vdd, temp, rot_speed, grad = line.split("\t")[:-1]
    xs = []
    y_rot_speed = []
    y_grad = []

    ani = animation.FuncAnimation(fig, plot_update_file, fargs=(xs, y_rot_speed, y_grad), interval=1000)
    
    plt.show()
    
        
if __name__ == '__main__':
    fig = plt.figure(figsize=(10,4))
    ax = fig.add_subplot(1, 2, 1)
    ax2 = fig.add_subplot(1, 2, 2)

    main()
