# 23-24 CanSat Source Code
import PySimpleGUI as sg

def main():
    # Variables used for the first row of the GUI
    TEAM_ID = 1032 #CHANGE THIS. OLD TEAM ID NUM
    MISSION_TIME = '00:00:00' # In UTC time in hh:mm:ss

    # Variables used for the second row of the GUI 
    PC_DEPLOY = 'N' # 'C' indicates the parachute is deployed (at 100 m), 'N' otherwise.
    MODE = 'S' # 'F' for flight mode and 'S' for simulation mode.
    GPS_TIME = '00:00:00' # Is the time from the GPS receiver. The time must be reported in UTC and have a resolution of a second.
    SS1 = 'U' # Software State - Tells the state of the rocket - 'LAUNCH_WAIT', 'ASCENT', 'ROCKET_SEPARATION', 'DESCENT', 'HS_RELEASE', 'LANDED', or 'U' (undetermined)

    # Variables used for the third row of the GUI 
    PC1 = 0 # Number of packets of PC has?
    HS_DEPLOY = 'N' # 'P' indicates the heat shield is deployed, 'N' otherwise.
    MAST_RAISE  = '??' # Not sure what this means
    GPS_SAT = 0 # Is the number of GPS satellites being tracked by the GPS receiver. This must be an integer.
    CMD_ECHO = "CXON" # Is the text of the last command received and processed by the Cansat. For example, CXON or SP101325. See the command section for details of command formats. Do not include com characters.


    # Sets the color theme of the dashboard 
    sg.theme('DarkAmber')

    # All the stuff inside your window.
    top_banner = [sg.Text('Team ID: '+str(TEAM_ID), font='Any 26', background_color='#1B2838', border_width=(5), size=(40), key = 'TEAM_ID'),
            sg.Text(MISSION_TIME, font='Any 22', background_color='#1B2838', border_width=(8), size=(10), key = 'missionTime'),
            sg.Button('Calibrate', font='Any 16'),
            sg.Button('Connect', font='Any 16'),
            sg.Button('Close', font='Any 16')]
    
    second_row = [sg.Text('PC DEPOY: '+ PC_DEPLOY, size=(14), font='Any 16', background_color='#1B2838', key = 'PC_DEPLOY'),
            sg.Text('Mode: '+ MODE, size=(13), font='Any 16', background_color='#1B2838', key = 'MODE'),
            sg.Text('GPS Time: ' + GPS_TIME, size=(18), font='Any 16', background_color='#1B2838', key='gpsTime'),
            sg.Text('Software State : '+SS1, size=(32), font='Any 16', background_color='#1B2838', key = 'STATE')]
    
    third_row = [sg.Text('Packet Count: '+str(PC1), size=(17), font='Any 16', background_color='#1B2838', key = 'PC1'),
            sg.Text('HS Deploy: '+HS_DEPLOY, size=(15), font='Any 16', background_color='#1B2838', key = 'HS_DEPLOY'),
            sg.Text('Mast Raised: '+MAST_RAISE, size=(15), font='Any 16', background_color='#1B2838', key = 'MAST_RAISED'),
            sg.Text('GPS Sat: ' +str(GPS_SAT), size=(13), font='Any 16', background_color='#1B2838', key = 'GPS_SAT'),
            sg.Text('CMD Echo: '+CMD_ECHO, size=(25), font='Any 16', background_color='#1B2838', key = 'CMD_ECHO')]
    
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
