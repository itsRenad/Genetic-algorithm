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
    option = int(input("Press 1 if you want items weight to be as i/2, Press 2 for weights as (i^2)/2: "))
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
    # weight_of_container[i] - weight_of_container[i+1]
    #weight_diff_between_containers = [abs(j-i) for i, j in zip(each_container_weight_sum[:-1], each_container_weight_sum[1:])]
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
    print("The Fitness value of the solution is: ",compute_mean_weight_difference(container_list))
    
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