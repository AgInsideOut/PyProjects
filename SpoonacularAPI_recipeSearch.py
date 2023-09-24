import requests
import json
import inflect
import pprint
import csv
import AppConfig

headers = {
	"X-RapidAPI-Key": AppConfig.spoonacular_app_key,
	"X-RapidAPI-Host": "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com"
	}

def ingredient_search(querystring_0):
    url = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/food/ingredients/search"
    response = requests.request("GET", url, headers=headers, params=querystring_0)
    results = json.loads(response.text)
    return results

def ingredient_data(chosen_id):
    url_0 = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/food/ingredients/{}/information".format(chosen_id)
    querystring = {"amount":"100","unit":"grams"}
    response_0 = requests.request("GET", url_0, headers=headers, params=querystring)
    results_0 = json.loads(response_0.text)
    return results_0

def recipe_search(querystring):
    url_1 = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/complexSearch"
    response_1 = requests.request("GET", url_1, headers=headers, params=querystring)
    results_1 = json.loads(response_1.text)
    return results_1
    
def recipe_instruction(item):
    url_2 = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/{}/analyzedInstructions".format(item)
    str_item = str(item)
    response_2 = requests.request("GET", url_2, headers=headers, params=str_item)
    results_2 = json.loads(response_2.text)
    return results_2
    
def nutrition_data(item):
    url_3 = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/{}/information".format(item)
    str_item = str(item)
    response_3 = requests.request("GET", url_3, headers=headers, params=str_item)
    results_3 = json.loads(response_3.text)
    return results_3
    
def choose_recipe():
    print('Enter an ingredient: ')
    ingredient = input()
    p = inflect.engine()
    ingredient_plural = ([p.plural(ingredient) for ingredient in ingredient.split(' ')])
    querystring_0 = {"query":"lemons"}
    querystring_0.update(query = ingredient_plural)
    ingrData = ingredient_search(querystring_0)
    ingrID = ingrData['results']
    ingredientIDs = []
    for i in ingrID:
        iID = i['id']
        ingredientIDs.append(iID)
    chosen_id = ingredientIDs[0]
    print(f'100 g of {ingredient_plural} contain:')
    n_results = ingredient_data(chosen_id)
    n_keys = n_results['nutrition']['caloricBreakdown']
    pprint.pprint(n_keys)
    print()
    healthLabel = input('Choose your health restrictions/requirements: \n (pescetarian/ lacto vegetarian/ ovo vegetarian/ vegan/ paleo/ primal/ vegetarian):')
    print()
    querystring = {"query":"pasta","diet":"vegan"}
    querystring.update(query = ingredient,diet = healthLabel)
    idSearch = recipe_search(querystring)
    ids = idSearch['results']
    recipeName = []
    recipeIDs = []
    print(f'Your preferences match:')
    for id in ids:
        recipe_name = id['title']
        recipeName.append(recipe_name)
        print(recipe_name)
    print()
    print('Which meal would you like to make?')
    chosen_meal = input()
    for id in ids:
        recipeID = id['id']
        recipeIDs.append(recipeID)
    recipeData = dict(zip(recipeName, recipeIDs))
    res = None
    if chosen_meal in set(recipeName).intersection(recipeData):
        res = recipeData[chosen_meal]
        item = str(res)
        print(f'\nMeal ID: {item}')
        nutrients = nutrition_data(item)
        link = nutrients['sourceUrl']
        print(link)
        preparationMinutes = nutrients['preparationMinutes']
        print(f'Preparation minutes: {preparationMinutes}')
        cookingMinutes = nutrients['cookingMinutes']
        print(f'Cooking minutes: {cookingMinutes}')
        diets = nutrients['diets']
        print(f'Diets: {diets}')
        print()
        print('Ingredients:')
        quantity = []
        measure = []
        food = []
        cookingIngredients = nutrients['extendedIngredients']
        for ingr in cookingIngredients:
            foo = ingr['originalName']
            food.append(foo)
            quant = ingr['amount']
            quantity.append(quant)
            meas = ingr['unit']
            measure.append(meas)
            print(ingr['original'])
        results = recipe_instruction(item)
        print()
        print('Preparation:')
        for res in results:
            steps = res['steps']
            for step in steps:
                print(step['step'])
            with open(f'{chosen_meal}.txt', 'w') as file_name:
                pprint.pprint(results, file_name)
        print()
        print("Bon appetit!")
        print()
        print(f'The recipe you selected has been exported to a file, named: {chosen_meal}.txt')
        with open(f'{chosen_meal}_groceries.csv', 'w') as csv_file_name:
            spreadsheet = csv.writer(csv_file_name)
            for value in range(len(food)):
                spreadsheet.writerow([food[value], str(quantity[value]), measure[value]])
        print(f'Your grocery list has been exported to a file, named: {chosen_meal}_groceries.csv')
    else:
        print('Wrong name. Try again.')
        return

choose_recipe()