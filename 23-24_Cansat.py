
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
            'TILT_Z': 0,
            'ROT_Z': 0,
            'CMD_ECHO': "CXON"
        }

        self.fig, self.ax = plt.subplots(figsize=(6, 3))
        self.canvas_elem = FigureCanvasTkAgg(self.fig, master=None)
        self.layout = self.create_gui_layout()
        self.csv_file_path = csv_file_path
        self.df = pd.read_csv(self.csv_file_path)
        
    def init_graphs(self):
        self.graphs = {
            'altitude': plt.subplots(figsize=(3.5, 3.5)),
            'temperature': plt.subplots(figsize=(3.5, 3.5)),
            'voltage': plt.subplots(figsize=(3.5, 3.5)),
            'tilt_x': plt.subplots(figsize=(3.5, 3.5)),
            'tilt_y': plt.subplots(figsize=(3.5, 3.5)),
            'tilt_z': plt.subplots(figsize=(3.5, 3.5)),
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
               
    def create_graph_canvas(self):
        return sg.Canvas(
            key='graph_canvas',
            background_color='white',
            size=(400, 200),
            pad=(10, 10)
        )

    def display_all_graphs(self):
        for key, (fig, ax) in self.graphs.items():
            canvas, canvas_widget = self.graph_canvases[key]
            canvas.draw()


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

            [self.create_graph_canvas()],  # Add the graph canvas to the layout
        ]
        return layout

    def set_data(self, data_dict):
        self.data.update(data_dict)

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

    def get_values(self, keys):
        return {key: self.data[key] for key in keys}

    def run_gui(self):
        sg.theme('DarkBlue3')
        self.window = sg.Window('CanSat Dashboard', self.layout, finalize=True)
        self.init_graphs()

        while True:
            event, values = self.window.read(timeout=1000)  # Example: Update every second
            if event == sg.WIN_CLOSED or event == 'Close':
                break

            # Simulate data update; replace this with actual data reading logic
            new_data = self.simulate_data_update()
            self.update_graphs(new_data)
            self.display_all_graphs()

        self.window.close()

    # Placeholder for data update simulation
    def simulate_data_update(self):
        # Read the CSV file
        df = pd.read_csv(self.csv_file_path)

        # You can use the tail method to get the most recent data, for simulation purposes
        latest_data = df.tail(1)

        # Extract the necessary columns and convert them to the appropriate format
        # Adjust the keys according to your graph labels
        simulation_data = {
            'time': [latest_data['MISSION_TIME'].iloc[0]],
            'altitude': [latest_data['ALTITUDE'].iloc[0]],
            'temperature': [latest_data['TEMPERATURE'].iloc[0]],
            'voltage': [latest_data['VOLTAGE'].iloc[0]],
            'tilt_x': [latest_data['TILT_X'].iloc[0]],
            'tilt_y': [latest_data['TILT_Y'].iloc[0]],
            'tilt_z': [latest_data['TILT_Z'].iloc[0]],
            'gps_altitude': [latest_data['GPS_ALTITUDE'].iloc[0]],
            'gps_latitude': [latest_data['GPS_LATITUDE'].iloc[0]],
            'gps_longitude': [latest_data['GPS_LONGITUDE'].iloc[0]],
            # Add other necessary fields here
        }

        return simulation_data


def main():
    csv_file_path = "Sample_Flight.csv"
    cansat = CanSat(csv_file_path)
    cansat.run_gui()

if __name__ == '__main__':
    main()
