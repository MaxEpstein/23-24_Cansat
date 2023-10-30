# 23-24 CanSat Source Code
import PySimpleGUI as sg
import matplotlib.pyplot as plt
import pandas as pd


class Graph:
    def __init__(self): # graph_title: str, x_axis_title: str, y_axis_title: str
        self.graph = {} # Using a dictionary to store vertices and their connections

    def add_vertex(self, vertex):
        if vertex not in self.graph:
            self.graph[vertex] = []

    def add_edge(self, start_vertex, end_vertex):
        if start_vertex in self.graph and end_vertex in self.graph:
            self.graph[start_vertex].append(end_vertex)
            self.graph[end_vertex].append(start_vertex)  # For an undirected graph

    def draw_graph(self):
        for vertex in self.graph:
            for edge in self.graph[vertex]:
                plt.plot([vertex[0], edge[0]], [vertex[1], edge[1]], 'bo-')  # 'bo-' specifies blue color, circle marker, and line style

        for vertex in self.graph:
            plt.plot(vertex[0], vertex[1], 'ro')  # 'ro' specifies red color and circle marker for vertices
            plt.text(vertex[0], vertex[1], str(vertex))  # Adding labels to vertices

        plt.title("Graph Visualization")
        plt.xlabel("X-axis")
        plt.ylabel("Y-axis")
        plt.grid(True)
        plt.show()


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
            sg.Text('CMD Echo: ' + self.CMD_ECHO, font=('Helvetica', 14), background_color='#1B2838', text_color='white', size=(25, 1), justification='left', key='CMD_ECHO')
        ]

    # Creates the main GUI to display 
    def create_gui_layout(self):
        top_banner = self.create_top_banner()
        second_row = self.create_second_row()
        third_row = self.create_third_row()
        
        layout = [
            top_banner,
            second_row,
            third_row
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

def main():
    cansat = CanSat()
    # cansat.run_gui()

    testing = Graph()
    testing.add_vertex((0, 0))
    testing.add_vertex((1, 1))
    testing.add_vertex((2, 2))
    testing.add_vertex((3, 3))

    testing.add_edge((0, 0), (1, 1))
    testing.add_edge((1, 1), (2, 2))
    testing.add_edge((2, 2), (3, 3))
    testing.add_edge((3, 3), (0, 0))

    testing.draw_graph()
    
if __name__=='__main__':
    main()
