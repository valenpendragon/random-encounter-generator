import pandas as pd
import openpyxl
import json


def import_tables(filepath):
    """
    This function takes a json listing the desired encounter tables to use from
    an excel workbook and returns the list.
    :param filepath: filepath
    :return: list of str
    """
    try:
        with open(filepath, "r") as fp:
            content = fp.read()
    except IOError:
        print(f"{filepath} not found or is not readable.")
        raise Exception(f"Configuration Problem: {filepath} was not readable.")

    raw_data = json.loads(content)
    return raw_data["table list"]


def import_workbook(tabs: list, filepath):
    """
    This function takes a list of tab names and a filepath to an excel workbook
    and returns a dictionary of pandas dataframes, using the tab names as keys.
    The first two columns are created by transforming the D100 string columns into
    separate columns of integers labeled Roll and Max.
    :param tabs: list of str
    :param filepath: filepath
    :return: dict of pd.DataFrame
    """
    wb = pd.read_excel(filepath, sheet_name=tabs, index_col=None, na_values=False)
    for tab in tabs:
        print(f"tab: {tab}")
        rolls = []
        maxes = []
        for i in range(len(wb[tab])):
            item = wb[tab]["D100"][i].split("–")
            print(f"item: {item}")
            if len(item) > 1:
                rolls.append(int(item[0]))
                maxes.append(int(item[1]))
            else:
                try:
                    temp = int(item[0])
                except ValueError:
                    item = wb[tab]["D100"][i].split("-")
                rolls.append(int(item[0]))
                maxes.append(int(item[0]))
        roll_s = pd.Series(rolls, index=None)
        max_s = pd.Series(maxes, index=None)
        wb[tab]["Roll"] = roll_s
        wb[tab]["Max"] = max_s
    return wb


if __name__ == "__main__":
    tables = import_tables("./samples/tables.json")
    print(tables)
    workbook = import_workbook(tables, "./samples/encounters.xlsx")
    print(workbook)
