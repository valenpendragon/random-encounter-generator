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


if __name__ == "__main__":
    tables = import_tables("./samples/tables.json")
    print(tables)
