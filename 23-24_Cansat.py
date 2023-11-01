# 23-24 CanSat Source Code
import PySimpleGUI as sg
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd


class CanSat:
    # TODO: Initialize each variable based on the ones listed in the resources
    def __init__(self):
        self.TEAM_ID = 2031 #Team ID, given by the contest
        self.MISSION_TIME = '00:00:00' # In UTC time in hh:mm:ss
        self.PACKET_COUNT = 0 # Number of packets
        self.MODE = 'S' # 'F' for flight mode and 'S' for simulation mode.
        self.STATE = 'U' # 'L' for launchpad, 'A' for ascent, 'D' for descent, 'G' for gliding, 'P' for parachute, 'L' for landed, 'U' for unknown
        self.ALTITUDE = 0 # Altitude in meters
        self.AIR_SPEED = 0 # Air speed in meters per second
        self.HS_DEPLOYED = 'N' # 'P' if the heat shield is deployed, 'N' otherwise
        self.PC_DEPLOYED = 'N' # 'C' indicates the parachute is deployed (at 100 m), 'N' otherwise.
        self.TEMPERATURE = 0 # Temperature in degrees Celsius
        self.PRESSURE = 0 # Pressure in kilopascals
        self.VOLTAGE = 0 # Voltage in volts
        self.GPS_TIME = '00:00:00' # Is the time from the GPS receiver. The time must be reported in UTC and have a resolution of a second.
        self.GPS_ALTITUDE = 0 # Is the altitude from the GPS receiver. The altitude must be in meters and have a resolution of a meter.
        self.GPS_LATITUDE = 0 # Latitude from the GPS reciever. In meters.
        self.GPS_LONGITUDE = 0 # Longitude from GPS reciever. In meters. 
        self.GPS_SATS = 0 # Is the number of GPS satellites being tracked by the GPS receiver. This must be an integer.
        self.TILT_X = 0 # Is the tilt angle of the CanSat along the X axis. The tilt angle must be in degrees and have a resolution of a degree.
        self.TILT_Y = 0 # Is the tilt angle of the CanSat along the Y axis. The tilt angle must be in degrees and have a resolution of a degree.
        self.TILT_Z = 0 # Is the tilt angle of the CanSat along the Z axis. The tilt angle must be in degrees and have a resolution of a degree.
        self.ROT_Z = 0 # Is the rotation angle of the CanSat along the Z axis. The rotation angle must be in degrees and have a resolution of a degree.
        self.CMD_ECHO = "CXON" # Is the text of the last command received and processed by the Cansat. For example, CXON or SP101325. See the command section for details of command formats. Do not include com characters.

    # Get's the current time. Not sure if it should be here or in another function.
    def clock():
        return (time.strftime("%H:%M:%S", time.gmtime()))

    def create_top_banner(self):
        return [
            sg.Text('Team ID: ' + str(self.TEAM_ID), font=('Helvetica', 16), background_color='#1B2838', text_color='white', size=(20, 1), justification='left', key='TEAM_ID'),
            sg.Text(self.MISSION_TIME, font=('Helvetica', 16), background_color='#1B2838', text_color='white', size=(10, 1), justification='right', key='missionTime'),
            sg.Button('Calibrate', font=('Helvetica', 12)),
            sg.Button('Connect', font=('Helvetica', 12)),
            sg.Button('Close', font=('Helvetica', 12))
        ]

    def create_second_row(self):
        return [
            sg.Text('PC DEPLOY: ' + self.PC_DEPLOYED, font=('Helvetica', 14), background_color='#1B2838', text_color='white', size=(12, 1), justification='left', key='PC_DEPLOY'),
            sg.Text('Mode: ' + self.MODE, font=('Helvetica', 14), background_color='#1B2838', text_color='white', size=(12, 1), justification='left', key='MODE'),
            sg.Text('GPS Time: ' + self.GPS_TIME, font=('Helvetica', 14), background_color='#1B2838', text_color='white', size=(16, 1), justification='left', key='gpsTime'),
            sg.Text('Software State: ' + self.STATE, font=('Helvetica', 14), background_color='#1B2838', text_color='white', size=(30, 1), justification='left', key='STATE')
        ]

    def create_third_row(self):
        return [
            sg.Text('Packet Count: ' + str(self.PACKET_COUNT), font=('Helvetica', 14), background_color='#1B2838', text_color='white', size=(15, 1), justification='left', key='PC1'),
            sg.Text('HS Deploy: ' + self.HS_DEPLOYED, font=('Helvetica', 14), background_color='#1B2838', text_color='white', size=(15, 1), justification='left', key='HS_DEPLOY'),
            sg.Text('GPS Sat: ' + str(self.GPS_SATS), font=('Helvetica', 14), background_color='#1B2838', text_color='white', size=(12, 1), justification='left', key='GPS_SAT'),
            sg.Text('CMD Echo: ' + self.CMD_ECHO, font=('Helvetica', 14), background_color='#1B2838', text_color='white', size=(25, 1), justification='left', key='CMD_ECHO'),
        ]
    
    def create_fourth_row(self):
        return [
            sg.Canvas(background_color= "black", size = (200, 200), key = 'Altitude (m) vs Time (s)'),
            sg.Canvas(background_color= "black", size = (200, 200), key = 'Temp (c) vs Time (s)'),
            sg.Canvas(background_color= "black", size = (200, 200), key = 'Voltage (volts) vs Time (s)'),
            sg.Canvas(background_color= "black", size = (200, 200), key = 'Acceleration (m/s^2) vs Time (s)')
        ]
    
    def create_fifth_row(self):
        return [
            sg.Canvas(background_color= "black", size = (200, 200), key = 'TiltX (deg) vs Time (s)'),
            sg.Canvas(background_color= "black", size = (200, 200), key = 'TiltY (deg) vs Time (s)'),
            sg.Canvas(background_color= "black", size = (200, 200), key = 'TiltZ (deg) vs Time (s)')
        ]
    
    def create_sixth_row(self):
        return[
            sg.Canvas(background_color= "black", size = (200, 200), key = 'GPS ALT (deg) vs Time (s)'),
            sg.Canvas(background_color= "black", size = (200, 200), key = 'GPS LAT (deg) vs Time (s)'),
            sg.Canvas(background_color= "black", size = (200, 200), key = 'GPS LONG (deg) vs Time (s)')
        ]
    
    def create_seventh_row(self):
        return[
            sg.Text('CMD', size=(8), font = 'Any 26', background_color='#1B2838'),
            sg.Input(size=(30)),
            sg.Button('Send',size=(18), font='Any 16'),
            sg.Text(' '*100)
        ]

    # This was in Max's code and I've been seeing it when I look it up. Idk what this does. - Sarah
    def draw_figure(canvas, figure):
        figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
        figure_canvas_agg.draw()
        figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
        return figure_canvas_agg


    # Creates the main GUI to display 
    def create_gui_layout(self):
        top_banner = self.create_top_banner()
        second_row = self.create_second_row()
        third_row = self.create_third_row()
        fourth_row = self.create_fourth_row()
        fifth_row = self.create_fifth_row()
        sixth_row = self.create_sixth_row()
        seventh_row = self.create_seventh_row()

        layout = [
            top_banner,
            second_row,
            third_row,
            fourth_row,
            fifth_row,
            sixth_row,
            seventh_row
        ]
        return layout

    def run_gui(self):
        sg.theme('DarkBlue3')
        layout = self.create_gui_layout()
        window = sg.Window('CanSat Dashboard', layout, finalize=True)

        while True:
            event, values = window.read()
            if event == sg.WIN_CLOSED or event == 'Close':
                break

        window.close()


class Graph(CanSat):
    def __init__(self, graph_title: str, x_axis_title: str, y_axis_title: str): 
        self.graph = {} # Using a dictionary to store vertices and their connections
        plt.title(graph_title)
        plt.xlabel(x_axis_title)
        plt.ylabel(y_axis_title)

    # Put in a new data point 
    def add_point(self, point):
        if point not in self.graph:
            self.graph[point] = []

    # Add a line between two points
    def add_edge(self, start_point, end_point):
        if start_point in self.graph and end_point in self.graph:
            self.graph[start_point].append(end_point)
            self.graph[end_point].append(start_point)  # For an undirected graph

    # Draws the graph
    def draw_graph(self):
        for vertex in self.graph:
            for edge in self.graph[vertex]:
                plt.plot([vertex[0], edge[0]], [vertex[1], edge[1]], 'bo-')  # 'bo-' specifies blue color, circle marker, and line style

        for vertex in self.graph:
            plt.plot(vertex[0], vertex[1], 'ro')  # 'ro' specifies red color and circle marker for vertices
            plt.text(vertex[0], vertex[1], str(vertex))  # Adding labels to vertices

        plt.grid(False)
        plt.show()


def main():
    cansat = CanSat()
    cansat.run_gui()
    
if __name__=='__main__':
    main()
