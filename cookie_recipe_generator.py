import json
import pprint
import random
import math
import matplotlib.pyplot as plt


def fitness_function(recipes):
	for r in recipes:
		r['fitness'] = len(r['ingredients'])

def select_recipe(recipes):
	sum_fitness = sum([recipe['fitness'] for recipe in recipes])
	f = random.randint(0, sum_fitness)
	for recipe in recipes:
		if f < recipe['fitness']:
			return recipe
		f -= recipe['fitness']
	return recipes[-1]

def crossover_recipes(r1, r2):
	global recipe_number
	p1 = random.randint(1, len(r1['ingredients'])-1)
	p2 = random.randint(1, len(r2['ingredients'])-1)
	r1a = r1['ingredients'][0:p1]
	r2b = r2['ingredients'][p2:-1]
	r = dict()
	r['name'] = "recipe {}".format(recipe_number)
	recipe_number += 1
	r['ingredients'] = r1a + r2b
	return r

def mutate_recipe(r):
	m = random.randint(0, 3)
	if m == 0:
		i = random.randint(0, len(r['ingredients'])-1)
		r['ingredients'][i] = r['ingredients'][i].copy()
		r['ingredients'][i]['amount'] += math.floor(r['ingredients'][i]['amount'] * 0.1)
		r['ingredients'][i]['amount'] = max(1, r['ingredients'][i]['amount'])
	elif m == 1:
		j = random.randint(0, len(r['ingredients'])-1)
		r['ingredients'][j] = r['ingredients'][j].copy()
		r['ingredients'][j]['ingredient'] = random.choice(all_ingredients)['ingredient']
	elif m == 2:
		r['ingredients'].append(random.choice(all_ingredients).copy())
	else:
		if len(r['ingredients']) > 1:
			r['ingredients'].remove(random.choice(r['ingredients']))

def normalise_recipe(r):
	unique_ingredients = dict()
	for i in r['ingredients']:
		if i['ingredient'] in unique_ingredients:
			n = unique_ingredients[i['ingredient']]
			n['amount'] += i['amount']
		else:
			unique_ingredients[i['ingredient']] = i.copy()
	r['ingredients'] = list(unique_ingredients.values())

	sum_amounts = sum([i['amount'] for i in r['ingredients']])
	scale = 1000 / sum_amounts
	for i in r['ingredients']:
		i['amount'] = max(1, math.floor(i['amount'] * scale))

def generate_recipes(size, population):
	R = []
	while len(R) < size:
		r1 = select_recipe(population)
		r2 = select_recipe(population)
		r = crossover_recipes(r1, r2)
		mutate_recipe(r)
		normalise_recipe(r)
		R.append(r)
		fitness_function(R)
	return R

def select_population(P, R):
	R = sorted(R, reverse = True, key = lambda r: r['fitness'])
	P = P[0:len(P)//2] + R[0:len(R)//2]
	P = sorted(P, reverse = True, key = lambda r: r['fitness'])
	return P

def generate_recipes_loop(recipes, population_size):
	population = random.choices(recipes, k=population_size)
	fitness_function(population)
	population = sorted(population, reverse = True, key = lambda r: r['fitness'])

	max_fitnesses = []
	min_fitnesses = []
	for i in range(1000):
		R = generate_recipes(population_size, population)
		population = select_population(population, R)
		max_fitnesses.append(population[0]['fitness'])
		min_fitnesses.append(population[-1]['fitness'])

	return population, max_fitnesses, min_fitnesses

def plot_fitness(max_fitnesses, min_fitnesses):
	x  = range(1000)
	plt.plot(x, max_fitnesses, label="line L")
	plt.fill_between(x, min_fitnesses, max_fitnesses, alpha=0.2)
	plt.plot()

	plt.xlabel("generation")
	plt.ylabel("fitness")
	plt.title("fitness over time")
	plt.legend()
	plt.show()

def main():
	f = open('data.json')
	data = json.load(f)

	recipes = data['recipes']

	global all_ingredients
	all_ingredients = []
	for recipe in recipes:
		all_ingredients.extend(recipe['ingredients'])

	# pprint.PrettyPrinter(indent=2, depth=3).pprint(recipes[0])
	# pprint.PrettyPrinter(indent=2, depth=2).pprint(all_ingredients)

	population_size = 20
	population = random.choices(recipes, k=population_size)
	
	global recipe_number
	recipe_number = 1

	fitness_function(population)
	population = sorted(population, reverse = True, key = lambda r: r['fitness'])

	population, max_fitnesses, min_fitnesses = generate_recipes_loop(recipes, population_size)

	plot_fitness(max_fitnesses, min_fitnesses)


if __name__ == "__main__":
	main()


