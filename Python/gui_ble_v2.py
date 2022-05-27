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
        self.y_rot = []
        self.y_grad = []

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
                self.y_rot.append(command[2])
                self.y_grad.append(command[3])
                x = self.x[-10:]
                # self.ax1.set_xlim(x[0], x[-1])
                # self.ax2.set_xlim(x[0], x[-1])
                y_rot = self.y_rot[-10:]
                y_grad = self.y_grad[-10:]
                self.ax1.plot(x, y_rot, color = "blue")

                self.ax2.plot(x, y_grad, color = "blue")

        self.fig.canvas.draw()
        return True

    def __call__(self, pipe):
        print('starting plotter...')

        self.pipe = pipe
        self.fig, (self.ax1, self.ax2) = plt.subplots(1,2,figsize=(14,7))
        self.ax1.grid()
        self.ax1.set_ylim(100, 200)
        self.ax1.tick_params(labelrotation=45)
        self.ax2.grid()
        self.ax2.tick_params(labelrotation=45)
        self.ax2.set_ylim(-20, 20)
        timer = self.fig.canvas.new_timer(interval=200)
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
            temp = round((1035 - float(self.device.char_read("F000BEF104514000B000000000000000").decode()))/5.5,2)
            rot_speed = int(self.device.char_read("F000BEEF04514000B000000000000000"))
            grad = int(self.device.char_read("F000BEF004514000B000000000000000"))
            vdd = float(self.device.char_read("F000BEF204514000B000000000000000").decode())/1000
            data = np.array([vdd, temp, rot_speed, grad])
            send(data)


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