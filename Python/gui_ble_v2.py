import multiprocessing as mp
import time
from turtle import color
import pygatt
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

# Fixing random state for reproducibility
np.random.seed(19680801)


class ProcessPlotter:
    def __init__(self):
        self.x = []
        self.y = []

    def terminate(self):
        plt.close('all')

    def call_back(self):
        while self.pipe.poll():
            command = self.pipe.recv()
            if command is None:
                self.terminate()
                return False
            else:
                self.x.append(datetime.now())
                self.y.append(command)
                self.ax.plot(self.x, self.y, color = "blue")
        self.fig.canvas.draw()
        return True

    def __call__(self, pipe):
        print('starting plotter...')

        self.pipe = pipe
        self.fig, self.ax = plt.subplots()
        timer = self.fig.canvas.new_timer(interval=1000)
        timer.add_callback(self.call_back)
        timer.start()

        print('...done')
        plt.show()

class NBPlot:
    def __init__(self):
        self.plot_pipe, plotter_pipe = mp.Pipe()
        self.adapter = pygatt.BGAPIBackend(serial_port = "COM3")
        self.adapter.start()
        print("Successfully connected to BLED112 adapter at COM3 port")
        self.device = self.adapter.connect("B0:91:22:0C:61:84")
        print("Connected to turbine!")


        self.plotter = ProcessPlotter()
        self.plot_process = mp.Process(
            target=self.plotter, args=(plotter_pipe,), daemon=True)
        self.plot_process.start()

    def plot(self, finished=False):
        send = self.plot_pipe.send
        if finished:
            send(None)
        else:
            # data = np.random.random(2)
            rot = int(self.device.char_read("F000BEEF04514000B000000000000000").decode())
            print(rot)
            send(rot)


def main():
    pl = NBPlot()
    for ii in range(100000):
        pl.plot()
        time.sleep(1)
    pl.plot(finished=True)


if __name__ == '__main__':
    if plt.get_backend() == "MacOSX":
        mp.set_start_method("forkserver")
    main()