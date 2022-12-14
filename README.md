# klauro_si507FinalProject
SI 507 Final Project
DASH Diet Recipe Finder

Required Modules: requests, json, BeautifulSoup, webbrowser, Flask, render_template, request

This program provides users with DASH Diet serving size reccomendations. It then asks users to enter in a protein and another ingredient of their choice. Based on this input the program will search the mealdb api for recipes and return them to the user. The user can then type in the meal they'd like the recipe for and the full recipe will be provided and if available, will open a youtube video of the recipe instructions. The program will then search the USDA api for the nutritional facts of these meal and return them if available.

This program uses a tree to query users for their ingredient choice. It also obtains data from the Mayo Clinic, Mealdb API, and USDA API. API keys were needed and requested from both Mealdb API and USDA API.

Of note, the Mealdb has proven to be slightly challenging to use when searching more than one ingredient. (it will not find any recipes for 'pork' and 'carrots' but will find recipes for 'chicken' and 'potatoes') 

To run program:
1. Template html documents needs to be placed in a Templates directory within the same directory that holds the python code.
2. Open the 'Final Project.py' file and click run. A blank webpage will open but for now, follow the input prompts in the terminal. If successful the webpage will update to reflect the user inputs. Choose any further viewing options on the webpage and click submit.
