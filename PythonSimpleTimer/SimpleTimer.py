import PySimpleGUI as sg
import time

# ----------------  Create Form  ----------------
sg.theme('Black')
sg.set_options(element_padding=(5, 5))

def main_win():
    layout = [
        [sg.Button('Set Time', key='win_set_time')],
        [sg.Text("00:00:00",size=(12, 2), font=('Helvetica', 20), justification='center', key='timer_text')],
        [sg.Button('Start', button_color=('white', '#001480'), key='start_countdown'), sg.Button('Stop', button_color=('white', '#007339'), key='stop_countdown'), sg.Exit(button_color=('white', 'firebrick4'), key='Exit')]
    ]
    return sg.Window('Simple Timer', layout, location=(800,600), finalize=True, scaling=1.5)

def time_set_win():
    layout = [
        [sg.In(key='set_time_hours', size=10, default_text=0), 
        sg.In(key='set_time_minutes', size=10, default_text=0), 
        sg.In(key='set_time_seconds', size=10, default_text=0)],
        [sg.Button('Set time', key='timer_set_time')]
    ]
    return sg.Window('Set time', layout, finalize=True, modal=True)

window1, window2 = main_win(), None  

# Main loop
while True:             # Event Loop
    window, event, values = sg.read_all_windows()
    if event == sg.WIN_CLOSED or event == 'Exit':
        window.close()
        if window == window2:       # if closing win 2, mark as closed
            window2 = None
        elif window == window1:     # if closing win 1, exit program
            break
    elif event == 'win_set_time' and not window2:
        window2 = time_set_win()
    elif event == 'timer_set_time':
        try:
            time_hours = int(values['set_time_hours'])
            time_minutes = int(values['set_time_minutes'])
            time_seconds = int(values['set_time_seconds'])
        except:
            sg.popup("Please enter numbers only")
            continue
        
        if (time_hours < 0 or time_hours > 23 or time_minutes < 0 or time_minutes > 59 or time_seconds < 0 or time_seconds > 59):
            sg.Popup('Please enter valid numbers')
            continue

        window1['timer_text'].update('{:02d}:{:02d}:{:02d}'.format(time_hours, time_minutes, time_seconds))
        window2.close()
        window2 = None
    elif event == 'start_countdown':
        window1['timer_text'].update('{:02d}:{:02d}:{:02d}'.format(time_hours - 1, time_minutes - 1, time_seconds - 1))
    
window.close()