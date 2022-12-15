### Final Project ###
## Kari Lauro ##

import requests as req
import json
from bs4 import BeautifulSoup
import webbrowser
from flask import Flask, render_template, request
app = Flask(__name__)

tree = ("What is your main protein? Choices: chicken, pork, fish: ", ("Is there an additional ingredient you'd like to search for? (starch, vegetable, spice) Enter here: ", None, None), None)

CACHE_FILENAME = 'finalProjectCache.json'
def save_cache(cache_dict):
    ''' saves the current state of the cache to disk
    Parameters
    ----------
    cache_dict: dict
        The dictionary to save
    Returns
    -------
    None
    '''
    dumped_json_cache = json.dumps(cache_dict)
    fw = open(CACHE_FILENAME,"w")
    fw.write(dumped_json_cache)
    fw.close()


@app.route('/')
def index():
    '''Fills initial Flask application with data provided using other functions'''
    dash_diet = open('finalProjectCache.json')
    dashData = json.load(dash_diet)
    recipeOptions = selectIngredient(tree)
    if recipeOptions == None:
        searchAgain = input('Sorry, no recipes found. Would you like to try to search again? \n')
        if searchAgain.lower() == 'yes':
            recipeOptions = selectIngredient(tree)
            print(recipeOptions)
            choice = input(f"Which of these recipes would you like to choose? Please type full recipe name \n")
            fRecipe = getFullRecipe(choice)
            return render_template('finalProjectTemplate.html',
                result=dashData, recipeList=recipeOptions, fullRecipe=fRecipe)
    else:
        print(recipeOptions)
        choice = input(f"Which of these recipes would you like to choose? Please type full recipe name \n")
        fRecipe = getFullRecipe(choice)
        return render_template('finalProjectTemplate.html',
            result=dashData, recipeList=recipeOptions, fullRecipe=fRecipe)

@app.route('/nutritionalInfo', methods=['POST', 'GET'])
def handle_the_form():
    '''Pulls in form responses and uses them to provide additional information to the user'''
    if request.method =='POST':
        r = request.form.get('meal')
        v = request.form.get('Option')
        if v == 'Yes':
            full_recipe = req.get(f'http://www.themealdb.com/api/json/v1/1/search.php?s={r.lower()}')
            frecipe = full_recipe.json()
            openvideo(frecipe)
        n = request.form.get('options')
        if n =='Yes':
            nutr = nutritionalValue(r)
            return render_template('Response.html', nutrients=nutr)
    else:
        return 'Thanks for your search!'

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
            return 'Sorry no recipes found'
        else:
            print(f'Recipe options')
            recipe_names = []
            for recipe in options['meals']:
                recipe_names.append(recipe['strMeal'])
            return recipe_names
    elif protein.lower() == 'pork':
        ingredient = input(tree[1][0])
        url = f"http://www.themealdb.com/api/json/v2/9973533/filter.php?i={protein.lower()},{ingredient.lower()}"
        resp = req.get(url)
        options = resp.json()
        if options['meals'] == None:
            print('Sorry no recipes found')
        else:
            print(f'Recipe options')
            recipe_names = []
            for recipe in options['meals']:
                recipe_names.append(recipe['strMeal'])
            return recipe_names
    elif protein.lower() == 'fish':
        ingredient = input(tree[1][0])
        url = f"http://www.themealdb.com/api/json/v2/9973533/filter.php?i={protein.lower()},{ingredient.lower()}"
        resp = req.get(url)
        options = resp.json()
        if options['meals'] == None:
            print('Sorry no recipes found')
        else:
            print(f'Recipe options')
            recipe_names = []
            for recipe in options['meals']:
                recipe_names.append(recipe['strMeal'])
            return recipe_names


def getFullRecipe(choice):
    '''takes in recipe name,
    searches the mealdb API and returns the full recipe,
    converted to a human readable format'''
    recipe_instructions = {}
    full_recipe = req.get(f'http://www.themealdb.com/api/json/v1/1/search.php?s={choice.lower()}')
    full_recipe = full_recipe.json()
    #print(full_recipe)
    for item in full_recipe['meals']:
        val = list(item.values())
        ing = val[9:29]
        amt = val[29:]
        recipe_instructions['Name']=item['strMeal']
        recipe_instructions['Instructions'] = item['strInstructions']
    dic = zip(ing,amt)
    ingred = dict(dic)
    recipe_instructions['Ingredients']=ingred

    return recipe_instructions

def openvideo(full_recipe):
    '''Using the full recipe, accesses the Youtube link if one is available and opens it'''
    webbrowser.open(full_recipe['meals'][0]['strYoutube'])

def nutritionalValue(recipe):
    '''Takes in a recipe,
    searches the USDA api for nutritional facts for the recipe
    and returns them to the user'''

    nutrition = req.get(f"https://api.nal.usda.gov/fdc/v1/foods/search?query={recipe}&pageSize=2&limit=1&requireAllWords=True&api_key=chhSwOkwOH5bbrKdoAh0CKq8ldeVnPbPMBZ60bPv")
    r = nutrition.json()
    print(r)
    if r['foods'] == []:
        return "Sorry no nutritional data for this recipe"
    else:
        keys = []
        vals = []
        for i in r['foods'][0]['foodNutrients']:
                if 'nutrientName' in i.keys():
                   keys.append(i['nutrientName'])
                if 'percentDailyValue' in i.keys():
                    vals.append(i['percentDailyValue'])
        d = zip(keys,vals)
        nut = dict(d)
        print(nut)
        return nut

def DASHcompliant():
    '''Loads DASH diet reccomended servings into a dictionary
    return dictionary to user'''

    keys = []
    values = []
    res = req.get("https://www.mayoclinic.org/healthy-lifestyle/nutrition-and-healthy-eating/in-depth/dash-diet/art-20050989")
    soup = BeautifulSoup(res.text,'html.parser')
    tables = soup.find('table')
    for row in tables.tbody.find_all('tr'):
        columns = row.find_all('td')
        if(columns != []):
            keys.append(columns[0].text.strip())
            values.append(columns[2].text.strip())
    d = zip(keys,values)
    dash_diet = dict(d)
    return dash_diet

if __name__ == '__main__':
    app.run(debug=True)
