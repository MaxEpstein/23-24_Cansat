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

class CanSat:
    def __init__(self):
        self.data = {
            'TEAM_ID': 2031,
            'MISSION_TIME': '00:00:00',
            'PACKET_COUNT': 0,
            'MODE': 'S',
            'STATE': 'U',
            'ALTITUDE': 0,
            'AIR_SPEED': 0,
            'HS_DEPLOYED': 'N',
            'PC_DEPLOYED': 'N',
            'TEMPERATURE': 0,
            'PRESSURE': 0,
            'VOLTAGE': 0,
            'GPS_TIME': '00:00:00',
            'GPS_ALTITUDE': 0,
            'GPS_LATITUDE': 0,
            'GPS_LONGITUDE': 0,
            'GPS_SATS': 0,
            'TILT_X': 0,
            'TILT_Y': 0,
            'TILT_Z': 0,
            'ROT_Z': 0,
            'CMD_ECHO': "CXON"
        }

    # Set values for multiple variables using a dictionary
    def set_values(self, data_dict):
        for key, value in data_dict.items():
            if key in self.data:
                self.data[key] = value

    # Get values for multiple variables using a list of keys
    def get_values(self, keys):
        return {key: self.data[key] for key in keys}

    def create_top_banner(self):
        return [
            sg.Text('Team ID: ' + str(self.data['TEAM_ID']), font=('Helvetica', 16), background_color='#1B2838', text_color='white', size=(20, 1), justification='left', key='TEAM_ID'),
            sg.Text(self.data['MISSION_TIME'], font=('Helvetica', 16), background_color='#1B2838', text_color='white', size=(10, 1), justification='right', key='missionTime'),
            sg.Button('Calibrate', font=('Helvetica', 12)),
            sg.Button('Connect', font=('Helvetica', 12)),
            sg.Button('Close', font=('Helvetica', 12))
        ]

    def create_second_row(self):
        return [
            sg.Text('PC DEPLOY: ' + self.data['PC_DEPLOYED'], font=('Helvetica', 14), background_color='#1B2838', text_color='white', size=(12, 1), justification='left', key='PC_DEPLOY'),
            sg.Text('Mode: ' + self.data['MODE'], font=('Helvetica', 14), background_color='#1B2838', text_color='white', size=(12, 1), justification='left', key='MODE'),
            sg.Text('GPS Time: ' + self.data['GPS_TIME'], font=('Helvetica', 14), background_color='#1B2838', text_color='white', size=(16, 1), justification='left', key='gpsTime'),
            sg.Text('Software State: ' + self.data['STATE'], font=('Helvetica', 14), background_color='#1B2838', text_color='white', size=(30, 1), justification='left', key='STATE')
        ]

    def create_third_row(self):
        return [
            sg.Text('Packet Count: ' + str(self.data['PACKET_COUNT']), font=('Helvetica', 14), background_color='#1B2838', text_color='white', size=(15, 1), justification='left', key='PC1'),
            sg.Text('HS Deploy: ' + self.data['HS_DEPLOYED'], font=('Helvetica', 14), background_color='#1B2838', text_color='white', size=(15, 1), justification='left', key='HS_DEPLOY'),
            sg.Text('GPS Sat: ' + str(self.data['GPS_SATS']), font=('Helvetica', 14), background_color='#1B2838', text_color='white', size=(12, 1), justification='left', key='GPS_SAT'),
            sg.Text('CMD Echo: ' + self.data['CMD_ECHO'], font=('Helvetica', 14), background_color='#1B2838', text_color='white', size=(25, 1), justification='left', key='CMD_ECHO')
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

    def setData(self):
        # Open file
        with open("Sample_Flight.csv") as file:  # Replace with your CSV file path
            reader = csv.reader(file)
            i = 0
            for row in reader:
                if i == 0:
                    titles = row
                if i == 1:
                    values = row
                    break
                i += 1

        data_dict = {titles[i]: values[i] for i in range(len(titles))}
        self.set_values(data_dict)

    def get_details(self):
        keys = ['MISSION_TIME', 'PACKET_COUNT', 'MODE', 'STATE', 'HS_DEPLOYED', 'PC_DEPLOYED']
        return self.get_values(keys)

    def get_measurements(self):
        keys = ['ALTITUDE', 'AIR_SPEED', 'TEMPERATURE', 'PRESSURE', 'VOLTAGE']
        return self.get_values(keys)

    def get_GPS(self):
        keys = ['GPS_TIME', 'GPS_ALTITUDE', 'GPS_LATITUDE', 'GPS_LONGITUDE', 'GPS_SATS']
        return self.get_values(keys)

    def get_direction(self):
        keys = ['TILT_X', 'TILT_Y', 'TILT_Z', 'ROT_Z']
        return self.get_values(keys)


def main():
    cansat = CanSat()
    cansat.setData()
    cansat.run_gui()

if __name__ == '__main__':
    main()
