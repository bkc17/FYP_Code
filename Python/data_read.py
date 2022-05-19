import os
import time
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random
import datetime as dt
import pygatt
import time


file_path = "C:\\Users\\bhara\\workspace_v8\\LabView\\Data\\test.txt"

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

def plot_update_file(i, xs, ys):
    # logfile = open(file_path,"r")
    # line = logfile.readlines()[-1]
    # logfile.close()
    
    with open(file_path) as f:
        for line in f:
            pass
        last_line = line
    vdd, temp, rot_speed, grad = last_line.split("\t")[:-1]
    ys.append(temp)
    xs.append(dt.datetime.now().strftime('%H:%M:%S.%f')[:-5])
    xs = xs[-20:]
    ys = ys[-20:]
    ax.clear()
    ax.plot(xs, ys)
    plt.xticks(rotation=45, ha='right')
    plt.subplots_adjust(bottom=0.30)
    plt.ylabel('Rotation Speed (rads/sec)')
    

def main():
    # logfile = open(file_path,"r")
    # loglines = follow(logfile)
    
    # for line in loglines:

    #     vdd, temp, rot_speed, grad = line.split("\t")[:-1]  

    ani = animation.FuncAnimation(fig, plot_update_file, fargs=(xs, ys), interval=1000)
    plt.show()
    
        
if __name__ == '__main__':
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    xs = []
    ys = []
    
    main()
