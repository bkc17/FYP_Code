from multiprocessing import connection
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from datetime import datetime, timedelta
import matplotlib.dates as mdates
import random
import pygatt
import numpy as np

class ble():
    def __init__(self, serial_port, connection_address):
        try:
            self.adapter = pygatt.BGAPIBackend(serial_port = serial_port)
            self.adapter.start()
            print(f"Successfully connected to BLED112 adapter at {serial_port} port")
        except:
            raise Exception(f"Could not detect BLED112 adapter at {serial_port} port")

        try:
            self.device = self.adapter.connect(connection_address)
            print("Connected to turbine!")
            
        except:
            raise Exception("Could not connect to turbine")

        # print(float(self.device.char_read("F000BEF204514000B000000000000000").decode())/1000)
    
    # def new_device(self, connection_address):
    #     # try:
    #     device = self.adapter.connect(connection_address)
    #     print("Successfully connected to device!")
    #     return device
    #     # except:
    #     #     raise Exception(f"Could not connect to device at address {connection_address}")

    def ble_read_data(self):
        vdd = float(self.device.char_read("F000BEF204514000B000000000000000").decode())/1000
        temp = round((1035 - float(self.device.char_read("F000BEF104514000B000000000000000").decode()))/5.5,2)
        rot_speed = int(self.device.char_read("F000BEEF04514000B000000000000000"))
        grad = int(self.device.char_read("F000BEF004514000B000000000000000"))
        return vdd, temp, rot_speed, grad


class GraphPage(tk.Frame):

    def __init__(self, parent, num_points):  
        tk.Frame.__init__(self, parent)

        # matplotlib figure
        self.figure = Figure(figsize=(5, 5), dpi=100)
        self.ax = self.figure.add_subplot(111)
        self.ax.tick_params(labelrotation=45)

        # format the x-axis to show the time
        myFmt = mdates.DateFormatter("%H:%M:%S")
        self.ax.xaxis.set_major_formatter(myFmt)

        # initial x and y data
        dateTimeObj = datetime.now() + timedelta(seconds=-num_points)
        self.x_data = [dateTimeObj + timedelta(seconds=i) for i in range(num_points)]
        self.y_data = [0 for i in range(num_points)]

        # create the plot
        self.plot = self.ax.plot(self.x_data, self.y_data, label='Rotation Speed')[0]
        self.ax.set_ylim(100, 200)
        self.ax.set_xlim(self.x_data[0], self.x_data[-1])
        self.ax.grid()

        label = tk.Label(self, text="Live Data Plotting")
        label.pack(pady=10, padx=10)
        self.canvas = FigureCanvasTkAgg(self.figure, self)
        self.canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

    def animate(self):

        #Read BLE Data from the device
        vdd, temp, rot_speed, grad = ble.ble_read_data()

        # append new data point to the x and y data
        self.x_data.append(datetime.now())
        self.y_data.append(rot_speed)    
         
        # remove oldest data point
        del self.x_data[0]
        del self.y_data[0]
        # self.x_data = self.x_data[1:]
        # self.y_data = self.y_data[1:]

        #  update plot data
        self.plot.set_xdata(self.x_data)
        self.plot.set_ydata(self.y_data)
        self.ax.set_xlim(self.x_data[0], self.x_data[-1])
        self.canvas.draw_idle()  # redraw plot
        self.after(1000, self.animate)  # repeat after 1s


root = tk.Tk()
ble = ble("COM3", "B0:91:22:0C:61:84")
graph = GraphPage(root, num_points=10)
graph.pack(fill='both', expand=True)
root.geometry('800x800')
graph.animate()  # launch the animation
root.mainloop()