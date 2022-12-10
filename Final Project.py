### Final Project ###
## Kari Lauro ##

import requests as req
import json
from bs4 import BeautifulSoup
import webbrowser

tree = ("What is your main protein? Choices: chicken, pork, fish: ", ("Is there an additional ingredient you'd like to search for? (starch, vegetable, spice) Enter here: ", None, None), None)

def selectIngredient(tree):
    '''Takes in a tree,
    runs through the tree to determine user ingredients,
    returns json file containing recipes based on ingredients selected '''

    protein = input(tree[0])
    if protein.lower() == 'chicken':
        ingredient = input(tree[1][0])
        url = f"http://www.themealdb.com/api/json/v2/9973533/filter.php?i={protein.lower()},{ingredient.lower()}"
        resp = req.get(url)
        options = resp.json()
        if options['meals'] == None:
            print('Sorry no recipes found')
        else:
            print(f'Recipe options')
            count = 1
            for recipe in options['meals']:
                print (recipe['strMeal'])
                count +=1
            choice = input(f"Which of these recipes would you like to choose? Please type full recipe name \n")
            full_recipe = req.get(f'http://www.themealdb.com/api/json/v1/1/search.php?s={choice.lower()}')
            full_recipe = full_recipe.json()
            webbrowser.open(full_recipe['meals'][0]['strYoutube'])
            return (choice, full_recipe)
    elif protein.lower() == 'pork':
        ingredient = input(tree[1][0])
        url = f"http://www.themealdb.com/api/json/v2/9973533/filter.php?i={protein.lower()},{ingredient.lower()}"
        resp = req.get(url)
        options = resp.json()
        if options['meals'] == None:
            print('Sorry no recipes found')
        else:
            print(f'Recipe options')
            count = 1
            for recipe in options['meals']:
                print (recipe['strMeal'])
                count +=1
            choice = input(f"Which of these recipes would you like to choose? Please type full recipe name\n")
            full_recipe = req.get(f'http://www.themealdb.com/api/json/v1/1/search.php?s={choice.lower()}')
            full_recipe = full_recipe.json()
            webbrowser.open(full_recipe['meals'][0]['strYoutube'])
            return (choice, full_recipe)
    elif protein.lower() == 'fish':
        ingredient = input(tree[1][0])
        url = f"http://www.themealdb.com/api/json/v2/9973533/filter.php?i={protein.lower()},{ingredient.lower()}"
        resp = req.get(url)
        options = resp.json()
        if options['meals'] == None:
            print('Sorry no recipes found')
        else:
            print(f'Recipe options')
            count = 1
            for recipe in options['meals']:
                print (recipe['strMeal'])
                count +=1
            choice = input(f"Which of these recipes would you like to choose? Please type full recipe name\n")
            full_recipe = req.get(f'http://www.themealdb.com/api/json/v1/1/search.php?s={choice.lower()}')
            full_recipe = full_recipe.json()
            webbrowser.open(full_recipe['meals'][0]['strYoutube'])
            return (choice, full_recipe)

def nutritionalValue(recipe):
    '''Takes in a recipe,
    searches the USDA api for nutritional facts for the recipe
    and returns them to the user'''

    nutrition = req.get(f"https://api.nal.usda.gov/fdc/v1/foods/search?query={recipe}&pageSize=2&limit=1&requireAllWords=True&api_key=chhSwOkwOH5bbrKdoAh0CKq8ldeVnPbPMBZ60bPv")
    r = nutrition.json()
    if r['foods'] == []:
        return "Sorry no nutritional data for this recipe"
    else:
        return r['foods'][0]['foodNutrients']

def DASHcompliant():
    '''Loads DASH diet reccomended servings into a dictionary
    return dictionary to user'''

    import re
    keys = []
    values = []
    res = req.get("https://www.mayoclinic.org/healthy-lifestyle/nutrition-and-healthy-eating/in-depth/dash-diet/art-20050989")
    soup = BeautifulSoup(res.text,'html.parser')
    tables = soup.find('table')
    for row in tables.tbody.find_all('tr'):
        columns = row.find_all('td')
        if(columns != []):
            keys.append(columns[0].text.strip())
            values.append(columns[1].text.strip())
    d = zip(keys,values)
    dash_diet = dict(d)
    return dash_diet


def main():

    print('DASH diet reccomended servings:')
    print(DASHcompliant())
    print("Let's get a meal recipe!")
    recipeOptions = selectIngredient(tree)
    print(recipeOptions)
    if recipeOptions == None:
        searchAgain = input('Sorry, no recipes found. Would you like to try to search again? \n')
        if searchAgain.lower() == 'yes' or 'y':
            recipeOptions = selectIngredient(tree)
            print(recipeOptions)
            if recipeOptions == None:
                ("Sorry no nutritional data for this recipe")
            else:
                print(nutritionalValue(recipeOptions[0]))
        else:
            print("Ok! Search again whenever you're ready")
    else:
        print(nutritionalValue(recipeOptions[0]))




if __name__ == '__main__':
    main()
