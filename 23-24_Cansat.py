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
            'MISSION_TIME': '00:00:00', # UTC time in hh:mm:ss
            'PACKET_COUNT': 0, # The total count of transmitted packets since turned on reset to zero by command when the CanSat is installed in the rocket on the launch pad at the beginning of the mission and maintained through processor reset.
            'MODE': 'S', # 'F' for flight mode and 'S' for simulation mode.
            'STATE': 'U', # The operation state of the software. (LAUNCH_WAIT, ASCENT, ROCKET_SEPERATION, DESCENT, HS_RELEASE, LANDED, etc).
            'ALTITUDE': 0, # In units of meters and must be relative to ground level at the launch site. 
            'AIR_SPEED': 0, # In meters/second measured with the pitot tube during both ascent and descent.
            'HS_DEPLOYED': 'N', # 'P' indicates the heat shield is deployed, 'N' otherwise.
            'PC_DEPLOYED': 'N', # 'C' indicates he parachute is deployed (at 100m), 'N' otherwise. 
            'TEMPERATURE': 0, # In degrees Celsius
            'PRESSURE': 0, # In kPa. Air pressure of the censor used. 
            'VOLTAGE': 0, # Voltage of the Cansat power bus 
            'GPS_TIME': '00:00:00', # In UTC. Time from the GPS reciever. 
            'GPS_ALTITUDE': 0, # In meters. The altitude from the GPS reciever above mean sea level.
            'GPS_LATITUDE': 0, # In degrees North. The latitude from the GPS reciever.
            'GPS_LONGITUDE': 0, # In degrees West. The longitude from the GPS reciever.
            'GPS_SATS': 0, # In int. Number of GPS satellites being tracked by the GPS reciever. 
            'TILT_X': 0, # In angle degrees of the CanSat on the x-axis.
            'TILT_Y': 0, # In angle degrees of the CanSat on the y-axis.
            'ROT_Z': 0, # In degrees/second. The rotation rate of the CanSat.
            'CMD_ECHO': "CXON" # Text of the last command recieved and processed by the CanSat.
        }

        self.fig, self.ax = plt.subplots(figsize=(6, 3))
        self.canvas_elem = FigureCanvasTkAgg(self.fig, master=None)
        self.layout = self.create_gui_layout()
        self.csv_file_path = csv_file_path
        self.df = pd.read_csv(self.csv_file_path)

    # Creates a canvas for the graphs 
    def create_graph_canvas(self):
        return sg.Canvas(
            key='graph_canvas',
            background_color='white',
            size=(400, 200),
            pad=(10, 10)
        )

    # Creates the graph 
    def display_graph(self, x_data, y_data, x_label, y_label, title):
        self.ax.clear()
        self.ax.plot(x_data, y_data, marker='o')
        self.ax.set_xlabel(x_label)
        self.ax.set_ylabel(y_label)
        self.ax.set_title(title)
        self.canvas_elem.get_tk_widget().pack_forget()
        self.canvas_elem = FigureCanvasTkAgg(self.fig, master=self.window['graph_canvas'].TKCanvas)
        self.canvas_elem.get_tk_widget().pack(fill='both', expand=True)
        self.canvas_elem.draw()

    # Creates the 1st row of the PySimpleGUI
    def create_top_banner(self):
        return [
            sg.Text('Team ID: ' + str(self.data['TEAM_ID']), font=('Helvetica', 16), background_color='#1B2838', text_color='white', size=(20, 1), justification='left', key='TEAM_ID'),
            sg.Text(self.data['MISSION_TIME'], font=('Helvetica', 16), background_color='#1B2838', text_color='white', size=(10, 1), justification='right', key='missionTime'),
            sg.Button('Calibrate', font=('Helvetica', 12)),
            sg.Button('Connect', font=('Helvetica', 12)),
            sg.Button('Close', font=('Helvetica', 12))
        ]

    # Creates the 2nd row of the PySimpleGUI    
    def create_second_row(self):
        return [
            sg.Text('PC DEPLOY: ' + self.data['PC_DEPLOYED'], font=('Helvetica', 14), background_color='#1B2838', text_color='white', size=(12, 1), justification='left', key='PC_DEPLOY'),
            sg.Text('Mode: ' + self.data['MODE'], font=('Helvetica', 14), background_color='#1B2838', text_color='white', size=(12, 1), justification='left', key='MODE'),
            sg.Text('GPS Time: ' + self.data['GPS_TIME'], font=('Helvetica', 14), background_color='#1B2838', text_color='white', size=(16, 1), justification='left', key='gpsTime'),
            sg.Text('Software State: ' + self.data['STATE'], font=('Helvetica', 14), background_color='#1B2838', text_color='white', size=(30, 1), justification='left', key='STATE')
        ]

    # Creates the 3rd row of the PySimpleGUI
    def create_third_row(self):
        return [
            sg.Text('Packet Count: ' + str(self.data['PACKET_COUNT']), font=('Helvetica', 14), background_color='#1B2838', text_color='white', size=(15, 1), justification='left', key='PC1'),
            sg.Text('HS Deploy: ' + self.data['HS_DEPLOYED'], font=('Helvetica', 14), background_color='#1B2838', text_color='white', size=(15, 1), justification='left', key='HS_DEPLOY'),
            sg.Text('GPS Sat: ' + str(self.data['GPS_SATS']), font=('Helvetica', 14), background_color='#1B2838', text_color='white', size=(12, 1), justification='left', key='GPS_SAT'),
            sg.Text('CMD Echo: ' + self.data['CMD_ECHO'], font=('Helvetica', 14), background_color='#1B2838', text_color='white', size=(25, 1), justification='left', key='CMD_ECHO')
        ]

    # Creates the 4th row of the PySimpleGUI
    def create_fourth_row(self):
        return [
            sg.Canvas(background_color="black", size=(250, 250)), # Altitude (m) vs Time (s)
            sg.Canvas(background_color="black", size=(250, 250)), # Temperature (C) vs Time (s)
            sg.Canvas(background_color="black", size=(250, 250)), # Voltage (Volts) vs Time (s)
            sg.Canvas(background_color="black", size=(250, 250))  # Acceleration (m/s^2) vs Time (s)
        ]
    
    # Creates the 5th row of the PySimpleGUI
    def create_fifth_row(self):
        return[
            sg.Canvas(background_color="black", size=(250, 250)), # Tilt X (deg) vs Time (s)
            sg.Canvas(background_color="black", size=(250, 250)), # Tilt Y (deg) vs Time (s)
            sg.Canvas(background_color="black", size=(250, 250))  # Rotation Z (deg) vs Time (s)
        ]
    
    # Creates the 6th row of the PySimpleGUI
    def create_sixth_row(self):
        return[
            sg.Canvas(background_color="black", size=(250, 250)), # GPS Altitude (deg) vs Time (s)
            sg.Canvas(background_color="black", size=(250, 250)), # GPS Latitude (deg) vs Time (s)
            sg.Canvas(background_color="black", size=(250, 250)), # GPS Longitude (deg) vs Time (s)
            sg.Canvas(background_color="black", size=(250, 250))  # Air Speed (m/s) vs Time (s)

        ]

    # Creates the whole PySimpleGUI that will be displayed
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

            [self.create_graph_canvas()],  # Add the graph canvas to the layout.
        ]
        return layout

    # Updates all the class attributes from the csv file. 
    def set_data(self, data_dict):
        self.data.update(data_dict)

    # Returns information about the status of the CanSat
    def get_details(self):
        keys = ['MISSION_TIME', 'PACKET_COUNT', 'MODE', 'STATE', 'HS_DEPLOYED', 'PC_DEPLOYED']
        return self.get_values(keys)

    # Returns information about the location and environment of the CanSat
    def get_measurements(self):
        keys = ['ALTITUDE', 'AIR_SPEED', 'TEMPERATURE', 'PRESSURE', 'VOLTAGE']
        return self.get_values(keys)

    # Returns information about the GPS used to track the CanSat
    def get_GPS(self):
        keys = ['GPS_TIME', 'GPS_ALTITUDE', 'GPS_LATITUDE', 'GPS_LONGITUDE', 'GPS_SATS']
        return self.get_values(keys)

    # Returns the Tilt X, Tilt Y, and Rotation Z of the CanSat in angle degrees
    def get_direction(self):
        keys = ['TILT_X', 'TILT_Y', 'ROT_Z']
        return self.get_values(keys)

    # Gets the corresponding value to the key in a loop.
    def get_values(self, keys):
        return {key: self.data[key] for key in keys}

    # Displays the PySimpleGUI
    def run_gui(self):
        sg.theme('DarkBlue3')
        self.window = sg.Window('CanSat Dashboard', self.layout, finalize=True)

        while True:
            event, values = self.window.read()
            if event == sg.WIN_CLOSED or event == 'Close':
                break
                
            # Make and Update graph(s)
            if event == 'Display Altitude vs. Mission Time':
                x_data = self.df['MISSION_TIME']
                y_data = self.df['ALTITUDE']
                self.display_graph(x_data, y_data, 'Time (s)', 'Altitude (m)', 'Altitude vs. Time')

            if event == 'Display Temperature vs. Mission Time':
                x_data = self.df['MISSION_TIME']
                y_data = self.df['TEMPERATURE']
                self.display_graph(x_data, y_data, 'Time (s)', 'Temperature (C)', 'Temperature vs. Time')

            if event == 'Voltage vs. Mission Time':
                x_data = self.df['MISSION_TIME']
                y_data = self.df['VOLTAGE']
                self.display_graph(x_data, y_data, 'Time (s)', 'Voltage (V)', "Voltage vs. Time")

        self.window.close()



def main():
    csv_file_path = "Sample_Flight.csv"
    cansat = CanSat(csv_file_path)
    cansat.run_gui()



if __name__ == '__main__':
    main()