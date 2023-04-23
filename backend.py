import pandas as pd
import openpyxl
import json
import random


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


def roll_result(table: pd.DataFrame) -> str:
    """
    This function accepts a random encounter table, determines the range for the
    random roll, and returns the string result corresponding to the roll. This table
    must have the following columns: Roll (int), Max (int), TYPE (str), and
    ENCOUNTER (str). There can be no overlap between the ranges specified by Roll
    and Max in each row and Roll <= Max. There can be no blank spaces in these columns.
    :param table: pd.DataFrame
    :return: str: result
    """
    # Find the min and max for the roll range. These encounter tables can have
    # numbers far above 100.
    roll_series = table["Roll"]
    max_series = table["Max"]
    min_roll = roll_series.min()
    max_roll = max_series.max()

    roll = random.randint(min_roll, max_roll)
    print(f"roll: {roll}")
    # Filter for smaller than or equal to roll in table.Roll.
    filtered = table.loc[table.Roll <= roll]
    print(f"1st filter: {filtered}")
    # Now, filter again for larger than or equal to roll in table.Max.
    # This should reduce it to a single row if there are no overlaps.
    filtered = filtered.loc[filtered.Max >= roll]
    print(f"2nd filter: {filtered}")
    result = filtered["ENCOUNTER"].squeeze()
    type_result = filtered["TYPE"].squeeze()
    return f"{result} ({type_result})"


if __name__ == "__main__":
    tables = import_tables("./samples/tables.json")
    print(tables)
    workbook = import_workbook(tables, "./samples/encounters.xlsx")
    print(workbook)
    idx = random.randint(0, len(tables) - 1)
    print(f"idx: {idx}")
    table = workbook[tables[idx]]
    print(table)
    result = roll_result(table)
    print(f"result: {result}")
