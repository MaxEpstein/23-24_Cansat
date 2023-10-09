# 23-24 CanSat Source Code
import PySimpleGUI as sg

def main():
    TEAM_ID = 1032 #CHANGE THIS. OLD TEAM ID NUM
    MISSION_TIME = '1 second'

    # Sets the color theme of the dashboard 
    sg.theme('DarkAmber')   # Add a touch of color

    # All the stuff inside your window.
    top_banner = [[sg.Text('Team ID: '+str(TEAM_ID), font='Any 26', background_color='#1B2838', border_width=(5), size=(40), key = 'TEAM_ID'),
            sg.Text(MISSION_TIME, font='Any 22', background_color='#1B2838', border_width=(8), size=(10), key = 'missionTime'),
            sg.Button('Calibrate', font='Any 16'),
            sg.Button('Connect', font='Any 16'),
            sg.Button('Close', font='Any 16')]]
    
    layout = [[top_banner]]
    
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
