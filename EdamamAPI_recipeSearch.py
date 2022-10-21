import csv
import requests
import pprint

#BEFORE RUNNING EDAMAM API, ONE NEEDS TO SUBSCRIBE TO IT AND OBTAIN A KEY AND ID HERE: https://rapidapi.com/edamam/api/edamam-nutrition-analysis/pricing

def recipe_search(ingredient, healthLabel):
    #app_id = 'ENTER YOUR ID HERE'
    #app_key = 'ENTER YOUR KEY HERE'
    recipe = requests.get('https://api.edamam.com/api/recipes/v2?type=public&q={}%20{}%20free&app_id={}&app_key={}'.format(ingredient, healthLabel, app_id,
app_key))
    data_r = recipe.json()
    return data_r['hits']

def nutrition_data(ingredient):
    #app_id = 'ENTER YOUR ID HERE'
    #app_key = 'ENTER YOUR KEY HERE'
    quantity = '100 g ' + str(ingredient)
    nutritions = requests.get('https://api.edamam.com/api/nutrition-data?app_id={}&app_key={}&nutrition-type=cooking&ingr={}'.format(app_id,
app_key, quantity))
    data_n = nutritions.json()
    return data_n

def choose_ingredient():
    ingredient = input('Enter an Ingredient:')
    print(f'100 g of {ingredient} contains:')
    n_results = nutrition_data(ingredient) 
    n_values = n_results['totalNutrients']
    kcal = n_values['ENERC_KCAL']
    proteins = n_values['PROCNT']
    sugar = n_values['SUGAR']
    fat = n_values['FAT']
    print(f'KCAL: {kcal}')
    print(f'SUGAR: {sugar}')
    print(f'FAT: {fat}')
    print(f'PROTEINS: {proteins}')
    print()
    healthLabel = input('Do you have any health restrictions/requirements? /n (e.g. Dairy-Free,Gluten-Free/Kosher/Pescatarian/Pork-Free/Vegan/Vegetarian): ')
    print()
    results = recipe_search(ingredient, healthLabel)
    for output in results:
        meal = output['recipe']
        label = meal['label']
        url = meal['url']
        print(label)
        print(url)
        print()
    choice = input('Which meal would you like to make?')
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
            print()
            print(label)
            print()
            print('You can access your recipe through the link below:')
            print(url)
            print()
            print('This recipe is: {}'.format(meal['healthLabels']))
            print()
            print('To make this you will need: \n{}'.format(meal['ingredientLines']))
            print()
            print('Bon appetit!')
            print()   
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