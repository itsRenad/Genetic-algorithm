import random
import sys
import math

#Lists to store initial population and ideal population
container_list = []
ideal_container_list = []

#Ask user for requared inputs
def input_func():
    items = int(input("Enter the number of items:  "))
    containers = int(input("Enter the number of containers:  "))
    option = int(input("Press 1 if you want items' weights to be as item weight/2 \nOr press 2 for weights as (item weight^2)/2: "))
    if containers==1:
        sys.exit("You have only one container, it is obvious!")
    return items,containers,option


def create_initial_population(items,containers,option):
    #Create list of lists for each container (Chromosomes)
    for i in range(0,containers):
        container_list.append([])
    #Fill containers with items weight(Genes)
    for i in range(1,items+1):
        index = random.randint(0,containers-1)
        if option == 1:
            container_list[index].append((i/2))
        else:
            container_list[index].append(((i**2)/2))

#Function to calculate mean weight difference between containers
def compute_mean_weight_difference(container):

    each_container_weight_sum = []

    for i in range(0,len(container)):
        sum = 0
        for j in range (0,len(container[i])):
            #Calculate the sum of weights in each container
            sum += container[i][j]

        each_container_weight_sum.append(sum)
    #Calculate difference between the sum of weights of each container
    #weight_of_container[i] - weight_of_container[i+1]
    for i, j in zip(each_container_weight_sum[:-1], each_container_weight_sum[1:]):
        weight_diff_between_containers = [abs(j-i)]
    #Find the mean difference of weights
    mean_fitness = math.fsum(weight_diff_between_containers)/len(weight_diff_between_containers)
    return mean_fitness

#Function to find the ideal placement of weights in containers
def find_ideal_setting(items,containers):

    #Convert the containers list of lists to a 1 dimensional weight list
    #We have used this source for the list:
    #https://stackoverflow.com/questions/2961983/how-does-sum-flatten-lists

    weight_list = [j for item in container_list for j in item]
    weight_list.sort()
    element = 0
    count = items - 1

    #Create list of lists for each container (Chromosomes)
    for i in range(0,containers):
        ideal_container_list.append([])

    #Fill containers with items weight(Genes)
    for j in range(0,containers):
        #Check if equal number of items is possible or not
        div = items%containers
        if div == 0:                                 #It is possible
            total = int(items/containers)
            each_item = int(total/2)
            #Add first and last elements in the list to containers
            while each_item > 0:
                ideal_container_list[j].append(weight_list[element])
                ideal_container_list[j].append(weight_list[count])
                count -= 1
                element += 1
                each_item -= 1

        else:                                      #It is impossible

            if j < containers - 1 and (items - element) > 0 :
                ideal_container_list[j].append(weight_list[element])
                element += 1

        #Last container reached and stil have items
        if j == containers - 1 and (items - element) > 0:
            for i in range(0,items - element):
                summ = []
                min_sum =0
                min_index=0

                #Add each of the remaining items to the minimum container weight
                for i in range(0,len(ideal_container_list)):
                    summ.append(sum(ideal_container_list[i]) + weight_list[count])

                if element <= count:
                    for i in range(0,len(summ)):
                        #if the weight sum at an index is less than the min_sum we swap the values
                        if i == 0:
                            min_sum=summ[i]

                        if summ[i] < min_sum:
                            min_sum = summ[i]
                            min_index = i

                    ideal_container_list[min_index].append(weight_list[count])    #decrementing the count of remaining items
                    count -= 1

def calculate_fitness(items,containers):
    #Call the function to find ideal solution
    find_ideal_setting(items,containers)
    
    print("")
    print("The solution is: ",container_list)
    print("The fitness value of the solution is: ",compute_mean_weight_difference(container_list))
    
    #if the fitness value of our current solution is less than or equal to the fitness threshold value only then its a good distribution of weights across containers
    if compute_mean_weight_difference(container_list) <= compute_mean_weight_difference(ideal_container_list):

        print("The containers' weights are distributed in a good way.")
        print("The ideal solution is: ",ideal_container_list)

    else:

        print("The containers' weights are not distributed well.")
        print("The ideal solution is: ",ideal_container_list)


#Start
items,containers,option = input_func()
create_initial_population(items,containers,option)
calculate_fitness(items,containers)

import random
import string

# Number of individuals in each generation
POPIN=input("Enter the Populations you want to test")
POPULATION_SIZE =int(POPIN)

# Valid genes
GENES = '''abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOP
QRSTUVWXYZ 1234567890, .-;:_!"#%&/()=?@${[]}'''

# Target string to be generated
TARGET=input("Enter the dimensions to check fitness ")
 
class Individual(object):
	'''
	Class representing individual in population
	'''
	def __init__(self, chromosome):
		self.chromosome = chromosome
		self.fitness = self.cal_fitness()

	@classmethod
	def mutated_genes(self):
		'''
		create random genes for mutation
		'''
		global GENES
		gene = random.choice(GENES)
		return gene

	@classmethod
	def create_gnome(self):
		'''
		create chromosome or string of genes
		'''
		global TARGET
		gnome_len = len(TARGET)
		return [self.mutated_genes() for _ in range(gnome_len)]

	def mate(self, par2):
		'''
		Perform mating and produce new offspring
		'''

		# chromosome for offspring
		child_chromosome = []
		for gp1, gp2 in zip(self.chromosome, par2.chromosome):	

			# random probability
			prob = random.random()

			# if prob is less than 0.45, insert gene
			# from parent 1
			if prob < 0.45:
				child_chromosome.append(gp1)

			# if prob is between 0.45 and 0.90, insert
			# gene from parent 2
			elif prob < 0.90:
				child_chromosome.append(gp2)

			# otherwise insert random gene(mutate),
			# for maintaining diversity
			else:
				child_chromosome.append(self.mutated_genes())

		# create new Individual(offspring) using
		# generated chromosome for offspring
		return Individual(child_chromosome)

	def cal_fitness(self):
		'''
		Calculate fitness score, it is the number of
		characters in string which differ from target
		string.
		'''
		global TARGET
		fitness = 0
		for gs, gt in zip(self.chromosome, TARGET):
			if gs != gt: fitness+= 1
		return fitness

# Driver code
def main():
	global POPULATION_SIZE

	#current generation
	generation = 1

	found = False
	population = []

	# create initial population
	for _ in range(POPULATION_SIZE):
				gnome = Individual.create_gnome()
				population.append(Individual(gnome))

	while not found:

		# sort the population in increasing order of fitness score
		population = sorted(population, key = lambda x:x.fitness)

		# if the individual having lowest fitness score ie.
		# 0 then we know that we have reached to the target
		# and break the loop
		if population[0].fitness <= 0:
			found = True
			break

		# Otherwise generate new offsprings for new generation
		new_generation = []

		# Perform Elitism, that mean 10% of fittest population
		# goes to the next generation
		s = int((10*POPULATION_SIZE)/10)
		new_generation.extend(population[:s])

		# From 50% of fittest population, Individuals
		# will mate to produce offspring
		s = int((90*POPULATION_SIZE)/10)
		for _ in range(s):
			parent1 = random.choice(population[:50])
			parent2 = random.choice(population[:50])
			child = parent1.mate(parent2)
			new_generation.append(child)

		population = new_generation

		print("Generation: {}\tString: {}\tFitness: {}".\
			format(generation,
			"".join(population[0].chromosome),
			population[0].fitness))

		generation += 1

	
	print("Generation: {}\tString: {}\tFitness: {}".\
		format(generation,
		"".join(population[0].chromosome),
		population[0].fitness))

if __name__ == '__main__':
	main()
 