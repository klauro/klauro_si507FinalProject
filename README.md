# klauro_si507FinalProject
SI 507 Final Project
DASH Diet Recipe Finder

This program provides users with DASH Diet serving size reccomendations. It then asks users to enter in a protein and another ingredient of their choice. Based on this input the program will search the mealdb api for recipes and return them to the user. The user can then type in the meal they'd like the recipe for and the full recipe will be provided and if available, will open a youtube video of the recipe instructions. The program will then search the USDA api for the nutritional facts of these meal and return them if available.

This program uses a tree to query users for their ingredient choice. It also obtains data from the Mayo Clinic, Mealdb Api, and USDA api.

Of note, the Mealdb has proven to be slightly challenging to use when searching more than one ingredient. (it will not find any recipes for 'pork' and 'carrots' but will find recipes for 'chicken' and 'potatoes') 

To run program:
  Simply open the 'Final Project.py' file and click run. 
