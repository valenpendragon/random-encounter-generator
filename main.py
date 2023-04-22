import PySimpleGUI as sg
import pandas as pd
import backend

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
                                 size=2,
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


def make_journey_window(days: int, tables: list) -> sg.Window:
    """
    This function creates a window that allows the user to pick the types of terrain
    that the party will pass through on their journey, using the number of days to
    create frames for each section. Each section also allows the GM to choose the
    percentage chance of an encounter. The types of encounters will be found in the
    encounter workbook, the tables in tables.json.
    It is best to keep the number to 7 days at a time to keep the window size from
    growing too large.
    :param days:
    :param tables: list of str
    :return:
    """
    layout = []
    for day in range(days):
        # Day 0 is an encounter near the starting point, like in a city or town on
        # the way out of town.
        frame = make_journey_row(day, tables)
        layout.append([frame])

    close_button = sg.Button("Close",
                             tooltip="Closes this window. Not recommended while working.",
                             key="close journey")
    create_button = sg.Button("Create Encounters",
                              tooltip="Generate a list of encounters",
                              key="create encounters")
    bottom_row_layout = [close_button, create_button]
    layout.append(bottom_row_layout)
    return sg.Window("Journey Window", layout=layout, finalize=True)


def make_journey_row(day: int, tables) -> sg.Frame:
    """
    This function creates a Frame for each segment of the journey, allowing the user
    to enter a percentage chance of an encounter for each segment, to choose a
    table to use for that segment, and the number of times per day to check.
    :param day:
    :return:
    """
    frame_label = f"Day {day} of Journey"
    terrain_label = sg.Text("Choose Terrain and Tier Level")
    terrain_listbox = sg.Combo(tables, enable_events=True, default_value="Country Shire Tier0",
                               visible=True, key=f"terrain choice{day}")
    chance_label = sg.Text("Encounter Chance (%):")
    chance_input = sg.Input(default_text="10", enable_events=True, size=2,
                            tooltip="Indicate a percentage change of encounter",
                            key=f"chance{day}")
    frequency_label = sg.Text("Frequency Each Day: ")
    daytime_checkbox = sg.Checkbox("Daytime", default=True, tooltip="Every Morning?",
                                   enable_events=True, key=f"daytime{day}")
    evening_checkbox = sg.Checkbox("Evening", default=True, tooltip="Every Evening?",
                                   enable_events=True, key=f"evening{day}")
    night_checkbox = sg.Checkbox("Night", default=False, tooltip="Every Night During Sleep?",
                                 enable_events=True, key=f"night{day}")
    frame_layout = [[terrain_label, terrain_listbox, chance_label, chance_input],
                    [frequency_label, daytime_checkbox, evening_checkbox,night_checkbox]]
    return sg.Frame(frame_label, layout=frame_layout)


def main():
    main_window, journey_window = make_main_window(), None
    print(main_window)

    while True:
        window, event, values = sg.read_all_windows()
        print(window, event, values)
        if event == sg.WIN_CLOSED and window == main_window:
            break
        elif event == sg.WIN_CLOSED and window == journey_window:
            journey_window.close()
        # Closing next window goes here. There are three windows total.
        # Closing encounter window goes after this one.

        match event:
            case "next":
                if journey_window != sg.WIN_CLOSED:
                    journey_window.close()
                tables = backend.import_tables(values["json filepath"])
                tables.sort()
                workbook = backend.import_workbook(tables, values["workbook filepath"])
                days = int(values["days choice"])
                journey_window = make_journey_window(days, tables)

            case "close journey":
                journey_window.close()
            case "exit":
                break

    main_window.close()


if __name__ == "__main__":
    main()
else:
    pass