# 23-24 CanSat Source Code
# Danush Singla :))
# Matthew Lee 
# Alex Segelnick
# Sarah Tran :)

import PySimpleGUI as sg
import matplotlib.pyplot as plt


""" # Not sure if this is possible. I wanted to make a class of graphs that we're using
class graphs:
    def __init__(self, graph_title: str, x_axis_title: str, y_axis_title: str):
        fig = plt.figure()
        plt.plot(x, y)
        plt.title(graph_title)
        plt.xlabel(x_axis_title)
        plt.ylabel(y_axis_title)
"""

class CanSat:
    # TODO: Initialize each variable based on the ones listed in the resources
    def __init__(self):
        self.ALTITUDE = 0
        self.TEMPERTAURE = 0
        self.PRESSURE = 0

         # Variables used for the first row of the GUI
        self.TEAM_ID = 2031 #Team ID, given by the contest
        self.MISSION_TIME = '00:00:00' # In UTC time in hh:mm:ss

        # Variables used for the second row of the GUI 
        self.PC_DEPLOY = 'N' # 'C' indicates the parachute is deployed (at 100 m), 'N' otherwise.
        self.MODE = 'S' # 'F' for flight mode and 'S' for simulation mode.
        self.GPS_TIME = '00:00:00' # Is the time from the GPS receiver. The time must be reported in UTC and have a resolution of a second.
        self.SS1 = 'U' # Software State - Tells the state of the rocket - 'LAUNCH_WAIT', 'ASCENT', 'ROCKET_SEPARATION', 'DESCENT', 'HS_RELEASE', 'LANDED', or 'U' (undetermined)

        # Variables used for the third row of the GUI 
        self.PACKET_COUNT = 0 # Number of packets
        self.HS_DEPLOY = 'N' # 'P' indicates the heat shield is deployed, 'N' otherwise.
        self.GPS_SATS = 0 # Is the number of GPS satellites being tracked by the GPS receiver. This must be an integer.
        self.CMD_ECHO = "CXON" # Is the text of the last command received and processed by the Cansat. For example, CXON or SP101325. See the command section for details of command formats. Do not include com characters.




def main():
    # List of graphs needed
    list_of_graphs = ['Altitude (m) vs. Time (s)',
                      'Temp (c) vs. Time (s)',
                      'Voltage (volt) vs Time (s)',
                      'Tilt X (deg) vs Time (s)',
                      'Tilt Y (deg) vs Time (s)',
                      'GPS Altitude (deg) vs Time (s)',
                      'GPS Latitude (deg) vs Time (s)',
                      'GPS Longitude (deg) vs Time (s)',
                      'Acceleration (m/s^2) vs Time (s)']
    
    cansat = CanSat()

    # Sets the color theme of the dashboard 
    sg.theme('DarkAmber')

    # All the stuff inside your window.
    top_banner = [sg.Text('Team ID: '+str(cansat.TEAM_ID), font='Any 26', background_color='#1B2838', border_width=(5), size=(40), key = 'TEAM_ID'),
            sg.Text(cansat.MISSION_TIME, font='Any 22', background_color='#1B2838', border_width=(8), size=(10), key = 'missionTime'),
            sg.Button('Calibrate', font='Any 16'),
            sg.Button('Connect', font='Any 16'),
            sg.Button('Close', font='Any 16')]
    
    second_row = [sg.Text('PC DEPOY: '+ cansat.PC_DEPLOY, size=(14), font='Any 16', background_color='#1B2838', key = 'PC_DEPLOY'),
            sg.Text('Mode: '+ cansat.MODE, size=(13), font='Any 16', background_color='#1B2838', key = 'MODE'),
            sg.Text('GPS Time: ' + cansat.GPS_TIME, size=(18), font='Any 16', background_color='#1B2838', key='gpsTime'),
            sg.Text('Software State : '+cansat.SS1, size=(32), font='Any 16', background_color='#1B2838', key = 'STATE')]
    
    third_row = [sg.Text('Packet Count: '+str(cansat.PACKET_COUNT), size=(17), font='Any 16', background_color='#1B2838', key = 'PC1'),
            sg.Text('HS Deploy: '+cansat.HS_DEPLOY, size=(15), font='Any 16', background_color='#1B2838', key = 'HS_DEPLOY'),
            sg.Text('GPS Sat: ' +str(cansat.GPS_SATS), size=(13), font='Any 16', background_color='#1B2838', key = 'GPS_SAT'),
            sg.Text('CMD Echo: '+cansat.CMD_ECHO, size=(25), font='Any 16', background_color='#1B2838', key = 'CMD_ECHO')]
    
    layout = [top_banner,
              second_row,
              third_row]
    
    # Create the Window
    window = sg.Window('Window Title', layout)

    # Event Loop to process "events" and get the "values" of the inputs
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
            break
        print('You entered ', values[0])

    # Closes the window 
    window.close()

if __name__=='__main__':
    main()
