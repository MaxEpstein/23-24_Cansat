
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
import time

# Define a consistent color scheme and fonts
# Updated color constants
PRIMARY_COLOR = '#1B2838'  # Dark background color for the GUI
TEXT_COLOR = 'white'  # Text color for GUI elements on the primary background
GRAPH_BACKGROUND_COLOR = 'white'  # White background color for graphs
GRAPH_TEXT_COLOR = 'white'  # Text color for graph labels, titles, and axes

# Font definitions
FONT_TITLE = ('Helvetica', 16)
FONT_MAIN = ('Helvetica', 14)
FONT_BUTTON = ('Helvetica', 12)
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
        self.csv_file_path = csv_file_path
        self.df = pd.read_csv(self.csv_file_path)
        self.graph_canvases = {}
        self.layout = self.create_gui_layout()
        self.window = sg.Window('CanSat Dashboard', self.layout, finalize=True)
        self.window.move(0, 0)

        self.simulation_mode = False  # Simulation mode flag
        self.init_graphs()
            
    def init_graphs(self):
        fig_size = (3.8, 3.5)
        self.graphs = {
            'altitude': plt.subplots(figsize=(fig_size)),
            'air_speed': plt.subplots(figsize=(fig_size)),
            'temperature': plt.subplots(figsize=(fig_size)),
            'pressure': plt.subplots(figsize=(fig_size)),
            'voltage': plt.subplots(figsize=(fig_size)),
            'gps_altitude': plt.subplots(figsize=(fig_size)),
            'gps_latitude': plt.subplots(figsize=(fig_size)),
            'gps_longitude': plt.subplots(figsize=(fig_size)),
            'tilt_x': plt.subplots(figsize=(fig_size)),
            'tilt_y': plt.subplots(figsize=(fig_size)),
            'rot_z': plt.subplots(figsize=(fig_size))
        }
        for key, (fig, ax) in self.graphs.items():
            ax.set_facecolor(GRAPH_BACKGROUND_COLOR)
            ax.tick_params(colors=GRAPH_TEXT_COLOR)
            ax.xaxis.label.set_color(GRAPH_TEXT_COLOR)
            ax.yaxis.label.set_color(GRAPH_TEXT_COLOR)
            ax.title.set_color(GRAPH_TEXT_COLOR)
            fig.patch.set_facecolor(PRIMARY_COLOR)
            fig.subplots_adjust(left=0.15, bottom=0.25, right=0.85, top=0.90)

            # Create canvas as before
            canvas = FigureCanvasTkAgg(fig, master=self.window[f'graph_canvas_{key}'].TKCanvas)
            canvas_widget = canvas.get_tk_widget()
            canvas_widget.pack(fill='both', expand=True)
            self.graph_canvases[key] = (canvas, canvas_widget)
    
    def format_key(self, key):
        """Format the key by replacing underscores with spaces and capitalizing each word."""
        return key.replace('_', ' ').upper()
    
     
    def update_graphs(self, data):
        for key, (fig, ax) in self.graphs.items():
            ax.clear()
            if key in data and 'time' in data and len(data[key]) == len(data['time']):
                formatted_key = self.format_key(key)  # Format the key for display
                ax.plot(data['time'], data[key], color='black')
                ax.set_xlabel('TIME', color=GRAPH_TEXT_COLOR)
                ax.set_ylabel(formatted_key, color=GRAPH_TEXT_COLOR)  # Use formatted key here
                
                # Set the title with bold font
                ax.set_title(f'{formatted_key} VS TIME', color=GRAPH_TEXT_COLOR, fontweight='bold')
                
                plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")
            self.graph_canvases[key][0].draw()

    def display_all_graphs(self):
        for key, (fig, ax) in self.graphs.items():
            canvas, canvas_widget = self.graph_canvases[key]
            canvas.draw()


    def create_top_banner(self):
        return [
            sg.Text('Team ID: ' + str(self.data['TEAM_ID']), font=FONT_TITLE, background_color=PRIMARY_COLOR, text_color=TEXT_COLOR, size=(15, 1), justification='centere', key='TEAM_ID'),
            sg.Text(self.data['MISSION_TIME'], font=FONT_TITLE, background_color=PRIMARY_COLOR, text_color=TEXT_COLOR, size=(20, 1), justification='centere', key='MISSION_TIME'),
            sg.Button('Calibrate', font=FONT_BUTTON),
            sg.Button('Connect', font=FONT_BUTTON),
            sg.Button('Simulation Mode', font=FONT_BUTTON, key='Sim_Mode'),
            sg.Push(), sg.Button(font=FONT_BUTTON, button_color="#68748c", border_width=0, image_filename="close_button_edited.png"), sg.Push()   # Simulation mode button
        ]
    def create_second_row(self):
        return [
            sg.Text('PC DEPLOY: ' + self.data['PC_DEPLOYED'], font=FONT_MAIN, background_color=PRIMARY_COLOR, text_color=TEXT_COLOR, size=(14, 1), justification='center', key='PC_DEPLOYED'),
            sg.Text('Mode: ' + self.data['MODE'], font=FONT_MAIN, background_color=PRIMARY_COLOR, text_color=TEXT_COLOR, size=(14, 1), justification='center', key='MODE'),
            sg.Text('GPS Time: ' + self.data['GPS_TIME'], font=FONT_MAIN, background_color=PRIMARY_COLOR, text_color=TEXT_COLOR, size=(20, 1), justification='center', key='GPS_TIME'),
            sg.Text('Software State: ' + self.data['STATE'], font=FONT_MAIN, background_color=PRIMARY_COLOR, text_color=TEXT_COLOR, size=(20, 1), justification='center', key='STATE')
        ]

    def create_third_row(self):
        return [
            sg.Text('Packet Count: ' + str(self.data['PACKET_COUNT']), font=FONT_MAIN, background_color=PRIMARY_COLOR, text_color=TEXT_COLOR, size=(17, 1), justification='centere', key='PC1'),
            sg.Text('HS Deploy: ' + self.data['HS_DEPLOYED'], font=FONT_MAIN, background_color=PRIMARY_COLOR, text_color=TEXT_COLOR, size=(17, 1), justification='center', key='HS_DEPLOYED'),
            sg.Text('GPS Sat: ' + str(self.data['GPS_SATS']), font=FONT_MAIN, background_color=PRIMARY_COLOR, text_color=TEXT_COLOR, size=(14, 1), justification='center', key='GPS_SATS'),
            sg.Text('CMD Echo: ' + self.data['CMD_ECHO'], font=FONT_MAIN, background_color=PRIMARY_COLOR, text_color=TEXT_COLOR, size=(20, 1), justification='center', key='CMD_ECHO')
        ]

    def create_fourth_row(self):
        graph_size = (250, 250)  # Adjust size as needed
        return [
            sg.Canvas(key='graph_canvas_altitude', background_color=GRAPH_BACKGROUND_COLOR, size=graph_size, pad=(4,4)),
            sg.Canvas(key='graph_canvas_air_speed', background_color=GRAPH_BACKGROUND_COLOR, size=graph_size, pad=(4,4)),
            sg.Canvas(key='graph_canvas_temperature', background_color=GRAPH_BACKGROUND_COLOR, size=graph_size, pad=(4,4)),
            sg.Canvas(key='graph_canvas_pressure', background_color=GRAPH_BACKGROUND_COLOR, size=graph_size, pad=(4,4))
        ]

    def create_fifth_row(self):
        graph_size = (250, 250)  # Adjust size as needed
        return[
            sg.Canvas(key='graph_canvas_voltage', background_color=GRAPH_BACKGROUND_COLOR, size=graph_size, pad=(4,4)),
            sg.Canvas(key='graph_canvas_gps_altitude', background_color=GRAPH_BACKGROUND_COLOR, size=graph_size, pad=(4,4)),
            sg.Canvas(key='graph_canvas_gps_latitude', background_color=GRAPH_BACKGROUND_COLOR, size=graph_size, pad=(4,4)),
            sg.Canvas(key='graph_canvas_gps_longitude', background_color=GRAPH_BACKGROUND_COLOR, size=graph_size, pad=(4,4))
        ]

    def create_sixth_row(self):
        graph_size = (250, 250)  # Adjust size as needed
        return[
            sg.Canvas(key='graph_canvas_tilt_x', background_color=GRAPH_BACKGROUND_COLOR, size=graph_size, pad=(4,4)),
            sg.Canvas(key='graph_canvas_tilt_y', background_color=GRAPH_BACKGROUND_COLOR, size=graph_size, pad=(4,4)),
            sg.Canvas(key='graph_canvas_rot_z', background_color=GRAPH_BACKGROUND_COLOR, size=graph_size, pad=(4,4))
        ]

    def create_seventh_row(self):
        dropdown_options = ["bleh", "blah", "bloh"]
        return[
            sg.Text('CMD', font=(FONT_MAIN, 20), background_color=PRIMARY_COLOR, size=(5, 1), text_color=TEXT_COLOR, justification='centere'),
            sg.DD(dropdown_options, font=(FONT_MAIN, 20), size=(20, 15)),
            sg.Button('Send', font=FONT_BUTTON, size=(5, 1)),
        ]

    def create_gui_layout(self):
        layout = [
            [sg.Column([self.create_top_banner()], pad=(4,4))],
            [sg.Column([self.create_second_row()], pad=(4,4))],
            [sg.Column([self.create_third_row()], pad=(4,4))],
            [sg.Column([self.create_fourth_row()], pad=(4,4))],
            [sg.Column([self.create_fifth_row()], pad=(4,4))],
            [sg.Column([self.create_sixth_row()], pad=(4,4))],
            [sg.Column([self.create_seventh_row()], pad=(4,4))],

        ]
        return layout

    def set_data(self, data_dict):
        self.data.update(data_dict)

    def run_gui(self):
        while True:
            event, values = self.window.read(timeout=1500)
            if event == sg.WIN_CLOSED or event == '':
                break

            if event == 'Simulation_Mode': # Change this to Sim_Mode to get this branch to work
                self.simulation_mode = not self.simulation_mode
                print(f"Simulation Mode {'Enabled' if self.simulation_mode else 'Disabled'}")
                
            # Read and update graphs with new data
            start_time = time.perf_counter()
            new_data = self.read_latest_csv_data()
            self.update_graphs(new_data)
            self.display_all_graphs()
            
            # Update GUI elements
            self.update_gui_elements()
            end_time = time.perf_counter()
            duration = round(end_time-start_time, 5)
            print(f'Refresh rate: {duration} seconds')


        self.window.close()




    # Placeholder for data update simulation
    def read_latest_csv_data(self):
        if self.simulation_mode:
            pass
        else:
            self.df = pd.read_csv(self.csv_file_path)

            # Read the last 10 rows
            last_rows = self.df.tail(10)

            graph_data = {
                'time': last_rows['MISSION_TIME'].tolist(),
                'altitude': last_rows['ALTITUDE'].tolist(),
                'air_speed': last_rows['AIR_SPEED'].tolist(),       # does not exist in Flight_1032.csv hence the error
                'temperature': last_rows['TEMPERATURE'].tolist(),
                'pressure': last_rows['PRESSURE'].tolist(),
                'voltage': last_rows['VOLTAGE'].tolist(),
                'gps_altitude': last_rows['GPS_ALTITUDE'].tolist(),
                'gps_latitude': last_rows['GPS_LATITUDE'].tolist(),
                'gps_longitude': last_rows['GPS_LONGITUDE'].tolist(),
                'tilt_x': last_rows['TILT_X'].tolist(),
                'tilt_y': last_rows['TILT_Y'].tolist(),
                'rot_z': last_rows['ROT_Z'].tolist()
                # Add any additional fields you need
            }
            return graph_data


        '''
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
        self.data['ROT_Z'] = latest_data['ROT_Z']
        self.data['CMD_ECHO'] = latest_data['CMD_ECHO']

        # Create a dictionary to hold the data for the graphs
        graph_data = {
            'time': [latest_data['MISSION_TIME']],
            'altitude': [latest_data['ALTITUDE']],
            'air_speed': [latest_data['AIR_SPEED']],
            'temperature': [latest_data['TEMPERATURE']],
            'pressure': [latest_data['PRESSURE']],
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
'''


    def update_gui_elements(self):
        # Update GUI elements with the latest data
        self.window['TEAM_ID'].update('Team ID: ' + str(self.data['TEAM_ID']))
        self.window['MISSION_TIME'].update('Mission Time: ' + self.data['MISSION_TIME'])
        self.window['PC1'].update('Packet Count: ' + str(self.data['PACKET_COUNT']))
        self.window['MODE'].update('Mode: ' + self.data['MODE'])
        self.window['STATE'].update('Software State: ' + self.data['STATE'])
        self.window['PC_DEPLOYED'].update('PC Deploy: ' + self.data['PC_DEPLOYED'])
        self.window['HS_DEPLOYED'].update('HS Deploy: ' + self.data['HS_DEPLOYED'])
        self.window['GPS_SATS'].update('GPS Sat: ' + str(self.data['GPS_SATS']))
        self.window['CMD_ECHO'].update('CMD Echo: ' + self.data['CMD_ECHO'])
        self.window['GPS_TIME'].update('GPS Time: ' + self.data['GPS_TIME'])
        # Add additional updates for other parameters
        #DO NOT INCLUDE
        '''
        self.window['altitude'].update('Altitude: ' + str(self.data['ALTITUDE']))
        self.window['AIR_SPEED'].update('Air Speed: ' + str(self.data['AIR_SPEED']))
        self.window['TEMPERATURE'].update('Temperature: ' + str(self.data['TEMPERATURE']))
        self.window['PRESSURE'].update('Pressure: ' + str(self.data['PRESSURE']))
        self.window['VOLTAGE'].update('Voltage: ' + str(self.data['VOLTAGE']))
        self.window['GPS_ALTITUDE'].update('GPS Altitude: ' + str(self.data['GPS_ALTITUDE']))
        self.window['GPS_LATITUDE'].update('GPS Latitude: ' + str(self.data['GPS_LATITUDE']))
        self.window['GPS_LONGITUDE'].update('GPS Longitude: ' + str(self.data['GPS_LONGITUDE']))
        self.window['TILT_X'].update('Tilt X: ' + str(self.data['TILT_X']))
        self.window['TILT_Y'].update('Tilt Y: ' + str(self.data['TILT_Y']))
        self.window['ROT_Z'].update('Rot Z: ' + str(self.data['ROT_Z']))
        '''


def main():
    csv_file_path = "SimCSV.csv"
    cansat = CanSat(csv_file_path)
    cansat.run_gui()

if __name__ == '__main__':
    main()
