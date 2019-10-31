import PySimpleGUI as sg
time=sg.time


def Splash(image_source, **kwargs):
    valid_args = dict(wait=1, start_mode='fast',
                      time_between_frames=30, hide_cmd='',
                      transparency=0)
    for key, value in valid_args.items():
        if key in kwargs:
            valid_args[key] = kwargs[key]
    wait = valid_args['wait']
    start_mode = valid_args['start_mode']
    time_between_frames = valid_args['time_between_frames']
    hide_cmd = valid_args['hide_cmd']

    transparency = valid_args['transparency']

    layout = [[sg.Image(image_source, key='_IMAGE_', background_color='#1D1F1C'),
               sg.T('Cancel (X)',
                    tooltip='Cancel', size=(10, 12),
                    font=('Forque', 11),
                    justification='center',
                    click_submits=True,
                    text_color='White',
                    background_color='#1D1F1C'),
               ]]

    window = sg.Window('SPLASH SCREEN',
                       no_titlebar=True,
                       grab_anywhere=False,
                       keep_on_top=True,
                       location=(None, None),
                       alpha_channel=1 - transparency,
                       element_padding=(0, 0),
                       return_keyboard_events=True,
                       background_color='#1D1F1C',
                       margins=(0, 0)).Layout(layout)

    animation_started = False
    '#############################'
    if hide_cmd:
        import win32gui
        import win32con
        The_program_to_hide = win32gui.FindWindowEx(None, None, None, hide_cmd)
        name_program_to_hide = win32gui.GetWindowText(The_program_to_hide)
        print(hide_cmd)
        print(name_program_to_hide, ', found_cmd:', bool(The_program_to_hide))
        if The_program_to_hide and hide_cmd:
            win32gui.ShowWindow(The_program_to_hide, win32con.SW_HIDE)
    '#############################'

    if start_mode in'quick_start,animate_after,fast':
        window.Finalize()
        window.Refresh()
        window.TKroot.attributes('-topmost', True)
        window.TKroot.attributes('-topmost', False)

        while True:
            window.Element('_IMAGE_').UpdateAnimation(
                image_source, time_between_frames=time_between_frames)
            window.Refresh()
            now = time.clock()

            event, values = window.Read(timeout=10)

            if not animation_started:
                animation_started = True
                wait += time.clock()
            elif now > wait:
                break
            elif event in ['x', 'X', 'Cancel (X)']:
                import sys
                sys.exit()
                break

    else:
        while True:
            window.Element('_IMAGE_').UpdateAnimation(
                image_source, time_between_frames=30)
            window.Refresh()
            now = time.clock()
            event, values = window.Read(timeout=20)
            if not animation_started:
                animation_started = True
                window.Finalize()
                window.TKroot.attributes('-topmost', True)
                window.TKroot.attributes('-topmost', False)
                wait += time.clock()
            elif now > wait:
                break
            elif event in ['x', 'X', 'Cancel (X)']:
                import sys
                sys.exit()
                break

    window.Close()

Splash(image_source='splash.gif', wait=4, transparency=0.25,
       start_mode='fast', time_between_frames=30)
