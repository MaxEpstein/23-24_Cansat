
# 23-24 CanSat Source Code
# Team Lead: Steele Elliott

# Members: 
# Danush Singla
# Matthew Lee 
# Alex Segelnick
# Sarah Tran 
# Dylan Manauasa
import pandas as pd
import PySimpleGUI as sg
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class CanSat:
    def __init__(self, csv_file_path):
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
            'ROT_Z': 0,
            'CMD_ECHO': "CXON"
        }
        self.csv_file_path = csv_file_path
        self.df = pd.read_csv(self.csv_file_path)
        self.layout = self.create_gui_layout()
            
    def init_graphs(self):
        self.graphs = {
            'altitude': plt.subplots(figsize=(3.5, 3.5)),
            'temperature': plt.subplots(figsize=(3.5, 3.5)),
            'voltage': plt.subplots(figsize=(3.5, 3.5)),
            'tilt_x': plt.subplots(figsize=(3.5, 3.5)),
            'tilt_y': plt.subplots(figsize=(3.5, 3.5)),
            'rot_z': plt.subplots(figsize=(3.5, 3.5)),
            'gps_altitude': plt.subplots(figsize=(3.5, 3.5)),
            'gps_latitude': plt.subplots(figsize=(3.5, 3.5)),
            'gps_longitude': plt.subplots(figsize=(3.5, 3.5))
        }
        self.graph_canvases = {}
        for i, (key, (fig, ax)) in enumerate(self.graphs.items()):
            canvas = FigureCanvasTkAgg(fig, master=self.window[f'graph_canvas_{i}'].TKCanvas)
            canvas_widget = canvas.get_tk_widget()
            canvas_widget.pack(fill='both', expand=True)
            self.graph_canvases[key] = (canvas, canvas_widget)
        
    def update_graphs(self, data):
        for key, (fig, ax) in self.graphs.items():
            ax.clear()
            ax.plot(data['time'], data[key])
            ax.set_xlabel('Time')
            ax.set_ylabel(key.capitalize())
            ax.set_title(f'{key.capitalize()} vs Time')

    def display_all_graphs(self):
        for key, (fig, ax) in self.graphs.items():
            canvas, canvas_widget = self.graph_canvases[key]
            canvas.draw()


    def create_top_banner(self):
        return [
            sg.Text('Team ID: ' + str(self.data['TEAM_ID']), font=('Helvetica', 16), background_color='#1B2838', text_color='white', size=(20, 1), justification='left', key='TEAM_ID'),
            sg.Text(self.data['MISSION_TIME'], font=('Helvetica', 16), background_color='#1B2838', text_color='white', size=(10, 1), justification='right', key='MISSION_TIME'),
            sg.Button('Calibrate', font=('Helvetica', 12)),
            sg.Button('Connect', font=('Helvetica', 12)),
            sg.Button('Close', font=('Helvetica', 12))
        ]

    def create_second_row(self):
        return [
            sg.Text('PC DEPLOY: ' + self.data['PC_DEPLOYED'], font=('Helvetica', 14), background_color='#1B2838', text_color='white', size=(12, 1), justification='left', key='PC_DEPLOY'),
            sg.Text('Mode: ' + self.data['MODE'], font=('Helvetica', 14), background_color='#1B2838', text_color='white', size=(12, 1), justification='left', key='MODE'),
            sg.Text('GPS Time: ' + self.data['GPS_TIME'], font=('Helvetica', 14), background_color='#1B2838', text_color='white', size=(16, 1), justification='left', key='GPS_TIME'),
            sg.Text('Software State: ' + self.data['STATE'], font=('Helvetica', 14), background_color='#1B2838', text_color='white', size=(30, 1), justification='left', key='STATE')
        ]

    def create_third_row(self):
        return [
            sg.Text('Packet Count: ' + str(self.data['PACKET_COUNT']), font=('Helvetica', 14), background_color='#1B2838', text_color='white', size=(15, 1), justification='left', key='PC1'),
            sg.Text('HS Deploy: ' + self.data['HS_DEPLOYED'], font=('Helvetica', 14), background_color='#1B2838', text_color='white', size=(15, 1), justification='left', key='HS_DEPLOY'),
            sg.Text('GPS Sat: ' + str(self.data['GPS_SATS']), font=('Helvetica', 14), background_color='#1B2838', text_color='white', size=(12, 1), justification='left', key='GPS_SAT'),
            sg.Text('CMD Echo: ' + self.data['CMD_ECHO'], font=('Helvetica', 14), background_color='#1B2838', text_color='white', size=(25, 1), justification='left', key='CMD_ECHO')
        ]

    def create_fourth_row(self):
        return [
            sg.Canvas(key='graph_canvas_0', background_color="black", size=(250, 250)), # Altitude (m) vs Time (s)
            sg.Canvas(key='graph_canvas_1', background_color="black", size=(250, 250)), # Temperature (C) vs Time (s)
            sg.Canvas(key='graph_canvas_2', background_color="black", size=(250, 250)), # Voltage (Volts) vs Time (s)
            sg.Canvas(key='graph_canvas_3', background_color="black", size=(250, 250))  # Acceleration (m/s^2) vs Time (s)
        ]

    def create_fifth_row(self):
        return[
            sg.Canvas(key='graph_canvas_4', background_color="black", size=(250, 250)), # Tilt X (deg) vs Time (s)
            sg.Canvas(key='graph_canvas_5', background_color="black", size=(250, 250)), # Tilt Y (deg) vs Time (s)
            sg.Canvas(key='graph_canvas_6', background_color="black", size=(250, 250))  # Tilt Z (deg) vs Time (s)
        ]

    def create_sixth_row(self):
        return[
            sg.Canvas(key='graph_canvas_7', background_color="black", size=(250, 250)), # GPS Altitude (deg) vs Time (s)
            sg.Canvas(key='graph_canvas_8', background_color="black", size=(250, 250)), # GPS Latitude (deg) vs Time (s)
            sg.Canvas(key='graph_canvas_9', background_color="black", size=(250, 250))  # GPS Longitude (deg) vs Time (s)
        ]

    def create_gui_layout(self):
        top_banner = self.create_top_banner()
        second_row = self.create_second_row()
        third_row = self.create_third_row()
        fourth_row = self.create_fourth_row()
        fifth_row = self.create_fifth_row()
        sixth_row = self.create_sixth_row()
        layout = [
            top_banner,
            second_row,
            third_row,
            fourth_row,
            fifth_row, 
            sixth_row,

        ]
        return layout

    def set_data(self, data_dict):
        self.data.update(data_dict)

    def run_gui(self):
        sg.theme('DarkBlue3')
        self.window = sg.Window('CanSat Dashboard', self.layout, finalize=True)
        self.init_graphs()
        while True:
            event, values = self.window.read(timeout=1000)
            if event == sg.WIN_CLOSED or event == 'Close':
                break

            new_data = self.read_latest_csv_data()  # Read latest data from CSV
            self.update_graphs(new_data)
            self.display_all_graphs()
            self.update_gui_elements()

        self.window.close()


    # Placeholder for data update simulation
    def read_latest_csv_data(self):
        # Re-read the CSV file to get the latest data
        self.df = pd.read_csv(self.csv_file_path)

        # Get the latest row
        latest_data = self.df.iloc[-1]

        # Update the self.data dictionary with the latest data
        self.data['MISSION_TIME'] = latest_data['MISSION_TIME']
        self.data['PACKET_COUNT'] = latest_data['PACKET_COUNT']
        self.data['MODE'] = latest_data['MODE']
        self.data['STATE'] = latest_data['STATE']
        self.data['ALTITUDE'] = latest_data['ALTITUDE']
        self.data['AIR_SPEED'] = latest_data['AIR_SPEED']
        self.data['HS_DEPLOYED'] = latest_data['HS_DEPLOYED']
        self.data['PC_DEPLOYED'] = latest_data['PC_DEPLOYED']
        self.data['TEMPERATURE'] = latest_data['TEMPERATURE']
        self.data['PRESSURE'] = latest_data['PRESSURE']
        self.data['VOLTAGE'] = latest_data['VOLTAGE']
        self.data['GPS_TIME'] = latest_data['GPS_TIME']
        self.data['GPS_ALTITUDE'] = latest_data['GPS_ALTITUDE']
        self.data['GPS_LATITUDE'] = latest_data['GPS_LATITUDE']
        self.data['GPS_LONGITUDE'] = latest_data['GPS_LONGITUDE']
        self.data['GPS_SATS'] = latest_data['GPS_SATS']
        self.data['TILT_X'] = latest_data['TILT_X']
        self.data['TILT_Y'] = latest_data['TILT_Y']
        self.data['ROT_Z'] = latest_data['ROT_Z']
        self.data['CMD_ECHO'] = latest_data['CMD_ECHO']

        # Create a dictionary to hold the data for the graphs
        graph_data = {
            'time': [latest_data['MISSION_TIME']],
            'altitude': [latest_data['ALTITUDE']],
            'temperature': [latest_data['TEMPERATURE']],
            'voltage': [latest_data['VOLTAGE']],
            'tilt_x': [latest_data['TILT_X']],
            'tilt_y': [latest_data['TILT_Y']],
            'rot_z': [latest_data['ROT_Z']],
            'gps_altitude': [latest_data['GPS_ALTITUDE']],
            'gps_latitude': [latest_data['GPS_LATITUDE']],
            'gps_longitude': [latest_data['GPS_LONGITUDE']]
            # Add other fields if needed
        }

        return graph_data



    def update_gui_elements(self):
        # Update GUI elements with the latest data
        self.window['TEAM_ID'].update('Team ID: ' + str(self.data['TEAM_ID']))
        self.window['MISSION_TIME'].update('Mission Time: ' + self.data['MISSION_TIME'])
        self.window['PC1'].update('Packet Count: ' + str(self.data['PACKET_COUNT']))
        self.window['MODE'].update('Mode: ' + self.data['MODE'])
        self.window['STATE'].update('Software State: ' + self.data['STATE'])
        self.window['PC_DEPLOY'].update('PC Deploy: ' + self.data['PC_DEPLOYED'])
        self.window['HS_DEPLOY'].update('HS Deploy: ' + self.data['HS_DEPLOYED'])
        self.window['GPS_SAT'].update('GPS Sat: ' + str(self.data['GPS_SATS']))
        self.window['CMD_ECHO'].update('CMD Echo: ' + self.data['CMD_ECHO'])
        self.window['GPS_TIME'].update('GPS Time: ' + self.data['GPS_TIME'])
        # Add additional updates for other parameters
        '''
        self.window['ALTITUDE'].update('Altitude: ' + str(self.data['ALTITUDE']))
        self.window['AIR_SPEED'].update('Air Speed: ' + str(self.data['AIR_SPEED']))
        self.window['TEMPERATURE'].update('Temperature: ' + str(self.data['TEMPERATURE']))
        self.window['PRESSURE'].update('Pressure: ' + str(self.data['PRESSURE']))
        self.window['VOLTAGE'].update('Voltage: ' + str(self.data['VOLTAGE']))
        self.window['GPS_ALTITUDE'].update('GPS Altitude: ' + str(self.data['GPS_ALTITUDE']))
        self.window['GPS_LATITUDE'].update('GPS Latitude: ' + str(self.data['GPS_LATITUDE']))
        self.window['GPS_LONGITUDE'].update('GPS Longitude: ' + str(self.data['GPS_LONGITUDE']))
        self.window['TILT_X'].update('Tilt X: ' + str(self.data['TILT_X']))
        self.window['TILT_Y'].update('Tilt Y: ' + str(self.data['TILT_Y']))
        self.window['TILT_Z'].update('Tilt Z: ' + str(self.data['TILT_Z']))
        self.window['ROT_Z'].update('Rot Z: ' + str(self.data['ROT_Z']))
'''


def main():
    csv_file_path = "Sample_Flight.csv"
    cansat = CanSat(csv_file_path)
    cansat.run_gui()

if __name__ == '__main__':
    main()
