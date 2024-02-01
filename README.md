# RecipePlanner
An application for creating files that contain recipe information for building large machines in GregTech and other similar scenarios. Its purpose is to us that information to count how much of each raw material is needed to complete a project.

Usage commands:

exit: saves and closes the app

open <project_name>: saves and opens an existing project

newfile <project_name>: saves and creates a new project and file

save: saves the current project

add <makes> <ingredient> <count=1.0> |
<makes> add <ingredient> <count=1.0>:
sets a given item (makes) to require count of a specified ingredient

list: lists all raw ingredients with required amounts for a whole project

list <item>: lists all raw ingredients with required amounts for a specific item

count: lists all items and with total required amounts

count <item>: dispays how much of a specific item is needed total

tree: displays an every item with its ingredients and counts underneath

tree <item>: displays an item with each ingredients underneath

print: displays a json sturcture of every item with its ingredients
