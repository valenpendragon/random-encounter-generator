import PySimpleGUI as sg

sg.theme("Black")


def make_main_window():
    # Build the Frame for picking the desired workbook.
    wb_choice_label = sg.Text("Select Workbook Containing Encounter Tables:")
    wb_choice_input = sg.Input(key="workbook filepath",
                               enable_events=True,
                               visible=True,
                               default_text="./samples/encounters.xlsx")
    wb_choice_button = sg.FileBrowse("Workbook", key="workbook",
                                     target="workbook filepath")
    wb_layout = [[wb_choice_label], [wb_choice_input], [wb_choice_button]]
    wb_frame = sg.Frame("Workbook", layout=wb_layout)

    # Build the Frame for picking the json file with the title list.
    json_choice_label = sg.Text("Select the JSON Containing the Table List:")
    json_choice_input = sg.Input(key="json filepath",
                                 enable_events=True,
                                 visible=True,
                                 default_text="./samples/tables.json")
    json_choice_button = sg.FileBrowse("JSON File", key="json",
                                       target="json filepath")
    json_layout = [[json_choice_label], [json_choice_input], [json_choice_button]]
    json_frame = sg.Frame("Table List", layout=json_layout)

    # Now, we need to build the Frame that allows the user to input the number
    # of days of the total trip, including any days spent in cities, towns, etc.
    # along the way.
    days_choice_label = sg.Text("How many days will this trip take?:")
    days_choice_input = sg.Input(key="days choice",
                                 enable_events=True,
                                 visible=True,
                                 default_text="7",
                                 tooltip="Use blocks of 7 days for very long trips.")
    days_layout = [[days_choice_label, days_choice_input]]
    days_frame = sg.Frame("Travel Days", layout=days_layout)

    # This is the bottom row of command buttons.
    exit_button = sg.Button("Exit", key="exit")
    next_button = sg.Button("Next Step", key="next")
    bottom_row_layout = [[exit_button, next_button]]

    main_layout = [[wb_frame], [json_frame], [days_frame], [bottom_row_layout]]
    return sg.Window("Random Encounter Generator", layout=main_layout,
                     finalize=True)


def main():
    main_window = make_main_window()
    print(main_window)

    while True:
        window, event, values = sg.read_all_windows()
        print(window, event, values)
        if event == sg.WIN_CLOSED and window == main_window:
            break
        # Closing next window goes here. There are three windows total.
        # Closing encounter window goes after this one.

        match event:
            case "exit":
                break

    main_window.close()


if __name__ == "__main__":
    main()
else:
    pass