# 23-24 CanSat Source Code
import PySimpleGUI as sg

def main():
    #Variables for first row 
    TEAM_ID = 1032 #CHANGE THIS. OLD TEAM ID NUM
    MISSION_TIME = '00:00:00' # In UTC time in hh:mm:ss

    #Variables for second row
    PC_DEPLOY = 'N' # 'C' indicates the parachute is deployed (at 100 m), 'N' otherwise.
    MODE = 'S' # 'F' for flight mode and 'S' for simulation mode.
    GPS_TIME = '00:00:00' # Is the time from the GPS receiver. The time must be reported in UTC and have a resolution of a second.
    SS1 = 'U' # Software State - Tells the state of the rocket - 'LAUNCH_WAIT', 'ASCENT', 'ROCKET_SEPARATION', 'DESCENT', 'HS_RELEASE', 'LANDED', or 'U' (undetermined)


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
    
    layout = [top_banner,
              second_row]
    
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
