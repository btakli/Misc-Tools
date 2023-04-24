import PySimpleGUI as sg

from tools import functions


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
        event, values = window.read()
        # End program if user closes window or
        # presses the OK button
        if event == sg.WIN_CLOSED:
            break
        elif event == '-FOLDER-':
            folder = values["-FOLDER-"]
        elif event in functions.FUNCTION_MAP:
            toolCalled = functions.FUNCTION_MAP[event]
            toolCalled(folder, True)

    window.close()


if __name__ == "__main__":
    main()
