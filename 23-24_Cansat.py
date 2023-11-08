# 23-24 CanSat Source Code
# Team Lead: Steele Elliott

# Members: 
# Danush Singla :))
# Matthew Lee 
# Alex Segelnick
# Sarah Tran :)
# Dylan Manauasa

import PySimpleGUI as sg
import matplotlib.pyplot as plt
import csv


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
    #TODO: declare and define getter and setter functions within the class. The get function will retrieve/return the values, and the setter will update

    def setData(self):
        # Open file  
        with open(r"samplecsv.csv") as file:     # changed 'samplecsv.csv' to correct csv filename
      
            # creates reader that reads the file
            reader = csv.reader(file)

            i = 0
            for row in reader:          # iterates through row because the type of reader is csv_reader which does not allow access to specific indices
                if i == 0:
                    titles = row        # this reads the first row of the file, which are the names of each category
                if i == 1:
                    values = row        # this reads the second row of the file, which are the latest values of each category
                    break               # we only need the first two rows so break out
                i += 1
        
        for i in range(len(titles)):        # goes through both lists
            if titles[i] == 'MISSION_TIME':
                self.MISSION_TIME = values[i]
            if titles[i] == 'PACKET_COUNT':
                self.PACKET_COUNT = values[i]       # does this because each index corresponds to the title and its respective value
            if titles[i] == 'MODE':
                self.MODE = values[i]
            if titles[i] == 'STATE':
                self.STATE = values[i]
            if titles[i] == 'ALTITUDE':
                self.ALTITUDE = values[i]
            if titles[i] == 'AIR_SPEED':
                self.AIR_SPEED = values[i]
            if titles[i] == 'HS_DEPLOYED':
                self.HS_DEPLOYED = values[i]
            if titles[i] == 'PC_DEPLOYED':
                self.PC_DEPLOYED = values[i]
            if titles[i] == 'TEMPERATURE':
                self.TEMPERATURE = values[i]
            if titles[i] == 'PRESSURE':
                self.PRESSURE = values[i]
            if titles[i] == 'VOLTAGE':
                self.VOLTAGE = values[i]
            if titles[i] == 'GPS_TIME':
                self.GPS_TIME = values[i]
            if titles[i] == 'GPS_ALTITUDE':
                self.GPS_ALTITUDE = values[i]
            if titles[i] == 'GPS_LATITUDE':
                self.GPS_LATITUDE = values[i]
            if titles[i] == 'GPS_LONGITUDE':
                self.GPS_LONGITUDE = values[i]
            if titles[i] == 'GPS_SATS':
                self.GPS_SATS = values[i]
            if titles[i] == 'TILT_X':
                self.TILT_X = values[i]
            if titles[i] == 'TILT_Y':
                self.TILT_Y = values[i]
            if titles[i] == 'TILT_Z':
                self.TILT_Z = values[i]
            if titles[i] == 'ROT_Z':
                self.ROT_Z = values[i]
    
    def get_details(self):
        return self.MISSION_TIME, self.PACKET_COUNT, self.MODE, self.STATE, self.HS_DEPLOYED, self.PC_DEPLOYED
    
    def get_measurements(self):
        return self.ALTITUDE, self.AIR_SPEED, self.TEMPERATURE, self.PRESSURE, self.VOLTAGE
    
    def get_GPS(self):
        return self.GPS_TIME, self.GPS_ALTITUDE, self.GPS_LATITUDE, self.GPS_LONGITUDE, self.GPS_SATS
    
    def get_direction(self):
        return self.TILT_X, self.TILT_Y, self.TILT_Z, self.ROT_Z





def main():
    cansat = CanSat()
    cansat.run_gui()
    
if __name__=='__main__':
    # main()
    cansat = CanSat()
    cansat.setData()
