import PySimpleGUI as sg

from tools import functions

def operate_on_tool(toolCalled, window, folder='./'):
    """Function that calls the tool that was selected. Includes potential special logic related to needed popups so they can run in the main thread."""
    if toolCalled == functions.FUNCTION_MAP['compressmp4crf']:
        crf_message = "Please input a desired integer CRFvalue (default 28, stick from [20,30]. Lower = higher quality = bigger file). Enter nothing for default: "
        crf = sg.popup_get_text(crf_message)
        window.start_thread(lambda: toolCalled(folder, True, crf), ('-THREAD-', '-THEAD ENDED-'))
    elif toolCalled == functions.FUNCTION_MAP['youtubetomp4']:
        link = sg.popup_get_text("Please provide a YouTube link:")
        window.start_thread(lambda: toolCalled(folder, True, link), ('-THREAD-', '-THEAD ENDED-'))
    else:
        window.start_thread(lambda: toolCalled(folder, True), ('-THREAD-', '-THEAD ENDED-'))

def main():

    # Column showing files and allowing you to select a folder
    file_list_column = [
        [
            sg.Text("Choose folder to operate on"),
            sg.In(size=(25, 1), enable_events=True, key="-FOLDER-"),
            sg.FolderBrowse(initial_folder='./'),
        ],
    ]

    toolList = []
    for key in functions.FUNCTION_MAP:
        toolList.append(sg.Button(button_text=key,
                        tooltip=functions.FUNCTION_MAP[key].__doc__))

    # Column listing tools
    tools_column = [
        [sg.Text("Choose a tool to use on the selected folder")]
    ]

    # add the tools to the tools column, 5 per row
    tool_row = []
    for i in range(0, len(toolList)):
        tool_row.append(toolList[i])
        if i % 5 == 0 and i != 0:
            tools_column.append(tool_row)
            tool_row = []
    
    # add the last row of tools
    tools_column.append(tool_row)

    # ----- Full layout -----
    layout = [
        [
            sg.Column(file_list_column),
            sg.VSeperator(),
            sg.Column(tools_column),
            sg.VSeperator(),
            sg.Output(background_color='black',
                      text_color='green', size=(800, 800))
        ]
    ]

    window = sg.Window("Tool Selector", layout,
                       size=(1600, 600), resizable=True)

    folder = './'
    while True:
        event, values = window.read(timeout=100)
        # End program if user closes window or
        # presses the OK button
        if event == sg.WIN_CLOSED:
            break
        elif event == '-FOLDER-':
            folder = values["-FOLDER-"]
        elif event in functions.FUNCTION_MAP:
            toolCalled = functions.FUNCTION_MAP[event]
            operate_on_tool(toolCalled, window, folder)
        
        elif event == '-THREAD-':
            print('Thread started')
        elif event == '-THEAD ENDED-':
            print('Thread ended')

    window.close()


if __name__ == "__main__":
    main()
