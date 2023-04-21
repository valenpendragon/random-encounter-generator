# Requirements:

## Packages
This program requires Python 3.10, Pandas, Openpyxl, and PySimpleGUI.

## Excel Workbook
It also requires an Excel or other spreadsheet workbook that contains the
random encounter tables. The format of these spreadsheets is three columns
listed below with headers:

1. d100: text, either single integer or a range in the form of two integers with a dash between them.
2. ENCOUNTER: text, the actual encounter
3. TYPE: any text that helps you understand what to do with the encounter, even page references

Items in the d100 column cannot overlap or duplicate numbers. However, they
can be any integer, up to the largest unsigned integer supported. So, you
could take two actual d100 lists and combine them into a single "d200" list
and the program would use the two lists as a single list. The d100 header
is simply a leftover from the original sources used as programming data.

## JSON File

It needs a json file similar in format to the sample file I will include
in this package. This json file lists all of the spreadsheet names in the
workbook that you plan to use to create random encounters.

# The Concept

My concept is that this program will roll random encounters by region and 
tier (but it will work just fine without either). The idea is that you 
would determine the number of days spent traveling and the types of terrain
the party would pass through on their way. In the GUI, indicate how often to
roll for each day, the probability (%) of an encounter, and which table to use
on each day. The program do the rest and display the results in a view window.
The user will have the option of saving this output to disk as a text file.
