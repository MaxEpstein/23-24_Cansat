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
        # Variables used for the first row of the GUI
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
        self.GPS_LATITUDE = 0
        self.GPS_LONGITUDE = 0
        self.GPS_SATS = 0 # Is the number of GPS satellites being tracked by the GPS receiver. This must be an integer.
        self.TILT_X = 0 # Is the tilt angle of the CanSat along the X axis. The tilt angle must be in degrees and have a resolution of a degree.
        self.TILT_Y = 0 # Is the tilt angle of the CanSat along the Y axis. The tilt angle must be in degrees and have a resolution of a degree.
        self.TILT_Z = 0 # Is the tilt angle of the CanSat along the Z axis. The tilt angle must be in degrees and have a resolution of a degree.
        self.ROT_Z = 0 # Is the rotation angle of the CanSat along the Z axis. The rotation angle must be in degrees and have a resolution of a degree.
        
        self.CMD_ECHO = "CXON" # Is the text of the last command received and processed by the Cansat. For example, CXON or SP101325. See the command section for details of command formats. Do not include com characters.


    def create_top_banner(self):
        return [
            sg.Text('Team ID: ' + str(self.TEAM_ID), font=('Helvetica', 18), background_color='#1B2838', text_color='white', size=(25, 1), justification='left', key='TEAM_ID'),
            sg.Text(self.MISSION_TIME, font=('Helvetica', 18), background_color='#1B2838', text_color='white', size=(10, 1), justification='right', key='missionTime'),
            sg.Button('Calibrate', font=('Helvetica', 14)),
            sg.Button('Connect', font=('Helvetica', 14)),
            sg.Button('Close', font=('Helvetica', 14))
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
    cansat.run_gui()

if __name__=='__main__':
    main()
