import csv
import requests
import pprint
import AppConfig
import json

edamam_nutr_app_id = AppConfig.edamam_nutr_app_id
edamam_nutr_app_key = AppConfig.edamam_nutr_app_key

edamam_reci_app_id = AppConfig.edamam_reci_app_id
edamam_reci_app_key = AppConfig.edamam_reci_app_key

def recipe_search(ingredient, healthLabel):
    recipe = requests.get('https://api.edamam.com/api/recipes/v2?type=public&q={}%20{}%20free&app_id={}&app_key={}'.format(ingredient, healthLabel, edamam_reci_app_id, edamam_reci_app_key))
    data_r = recipe.json()
    
    return data_r.get('hits', [])  # Return the 'hits' data or an empty list if not found

def nutrition_data(ingredient):
    quantity = '100 g ' + str(ingredient)
    nutritions = requests.get('https://api.edamam.com/api/nutrition-data?app_id={}&app_key={}&nutrition-type=cooking&ingr={}'.format(edamam_nutr_app_id, edamam_nutr_app_key, quantity))
    data_n = nutritions.json()

    return data_n

def choose_ingredient():
    
    ingredient = input(f'Enter an Ingredient:\t')
    n_results = nutrition_data(ingredient)
    n_values = n_results.get('totalNutrients', {})
    
    # Get "Energy" data
    energy_label = n_values.get('ENERC_KCAL', {}).get('label')
    energy_quantity = n_values.get('ENERC_KCAL', {}).get('quantity')
    energy_unit = n_values.get('ENERC_KCAL', {}).get('unit')
    
    # Get "Proteins" data
    proteins_label = n_values.get('PROCNT', {}).get('label')
    proteins_quantity = n_values.get('PROCNT', {}).get('quantity')
    proteins_unit = n_values.get('PROCNT', {}).get('unit')
    
    # Get "Sugar" data
    sugar_label = n_values.get('SUGAR', {}).get('label')
    sugar_quantity = n_values.get('SUGAR', {}).get('quantity')
    sugar_unit = n_values.get('SUGAR', {}).get('unit')
    
    # Get "Fat" data
    fat_label = n_values.get('FAT', {}).get('label')
    fat_quantity = n_values.get('FAT', {}).get('quantity')
    fat_unit = n_values.get('FAT', {}).get('unit')
    
    # Display nutritional information
    print(f'100 g of {ingredient} contains:\n'
        f'{energy_label} {energy_quantity} {energy_unit}\n'
        f'{sugar_label} {sugar_quantity} {sugar_unit}\n'
        f'{fat_label} {fat_quantity} {fat_unit}\n'
        f'{proteins_label} {proteins_quantity} {proteins_unit}\n')
    
    healthLabel = input('Do you have any health restrictions/requirements? \n(e.g. Dairy-Free, Gluten-Free/Kosher/Pescatarian/Pork-Free/Vegan/Vegetarian): ')
    
    results = recipe_search(ingredient, healthLabel)

    if not results:
        return  # Terminate the function

    # RecipeSearch results
    for output in results:
        meal = output['recipe']
        label = meal['label']
        url = meal['url']
        print(f'{label}\n{url}\n')

    choice = input(f'Which meal would you like to make?\t')

    for output in results:
        meal = output['recipe']
        label = meal['label']
        url = meal['url']
        if choice == label:
            quantity = []
            measure = []
            food = []
            ingr = meal['ingredients']
            for i in ingr:
                quant = i['quantity']
                quantity.append(quant)
                meas = i['measure']
                measure.append(meas)
                foo = i['food']
                food.append(foo)
        if choice == label:
            print(f'{label}\n'
                f'You can access your recipe through the link below:\n'
                f'{url}\n'
                f'This recipe is: {meal["healthLabels"]}\n'
                f'To make this you will need:\n'
                f'{meal["ingredientLines"]}\n'
                f'Bon appétit!\n')

            with open(f'{choice}.txt', 'w') as file_name:
                pprint.pprint(label, file_name)
                pprint.pprint(url, file_name)
                pprint.pprint(meal['ingredientLines'], file_name)
            
            print(f'The recipe you selected has been exported to a file, named: {choice}.txt')
            
            with open(f'{choice}_groceries.csv', 'w') as csv_file_name:
                spreadsheet = csv.writer(csv_file_name)
                for value in range(len(food)):
                    spreadsheet.writerow([food[value], quantity[value], measure[value]])
            
            print(f'Your grocery list has been exported to a file, named: {choice}_groceries.csv')

choose_ingredient()