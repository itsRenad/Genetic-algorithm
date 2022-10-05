import random
import math


#lists to store initial population and ideal population
container_list = []
ideal_container_list = []

#function to take input from the user
def input_func():
    items = int(input("Enter the number of items:  "))
    containers = int(input("Enter the number of containers:  "))
    option = int(input("Press 1 if you want items weight to be as i/2, Press 2 for weights as (i^2)/2: "))
    return items,containers,option

#function to create initial population
def create_initial_population(items,containers,option):
    #creating list of lists upto the number of containers, one list for each container to store weights
    for i in range(0,containers):
        container_list.append([])
    #iterating till the number of items
    for i in range(1,items+1):
        #selecting a random container
        index = random.randint(0,containers-1)
        #adding weight to the container based on user's option for weight selection
        if option == 1:
            container_list[index].append((i/2))
        else:
            container_list[index].append(((i**2)/2))

#function to calculate mean weight difference between containers
def compute_mean_weight_difference(container):
    #list to store the sum of weights for each container
    each_container_weight_sum = []
    #iterating till the number of containers
    for i in range(0,len(container)):
        #variable to store sum of each container weights
        sum = 0
        #iterating till the length of each container
        for j in range (0,len(container[i])):
            #adding up weights in the container
            sum += container[i][j]
        #appending the weight sum to list
        each_container_weight_sum.append(sum)
    #calculating difference between the total weights of each container 
    # weight_of_container[i] - weight_of_container[i+1]
    weight_diff_between_containers = [abs(j-i) for i, j in zip(each_container_weight_sum[:-1], each_container_weight_sum[1:])]
    #finding the mean difference of weights
    mean_fitness = math.fsum(weight_diff_between_containers)/len(weight_diff_between_containers)
    #returning the fitness value
    return mean_fitness

#function to find the ideal placement of weights in containers
def find_ideal_setting(items,containers):
    #converting the containers list of lists to a 1 dimensional weight list
    weight_list = [j for item in container_list for j in item]
    #sorting the weight list
    weight_list.sort()
    #setting element count to 0
    ele = 0
    #setting the total item count to items - 1 as ele is starting from zero
    item_count = items - 1
    #iterating till the number of containers
    for i in range(0,containers):
        #creating list of lists, one list for each container to store weights
        ideal_container_list.append([])
    
    #iterating till the number of containers
    for j in range(0,containers):
        #checking if a even distribution of weights is possible
        div = items%containers
        if div == 0:
            #finding the number of items that can go in each container
            total = int(items/containers)
            #finding the number of times item will be added
            each_item = int(total/2)
            #doing this in order to avoid situations of iterating with zero
            if each_item == 0:
                each_item = 1
            #adding one element from the start of sorted weight list and one from end to balance the weight distribution
            while each_item > 0:
                ideal_container_list[j].append(weight_list[ele])
                ideal_container_list[j].append(weight_list[item_count])
                #decrementing the item count and each item and incrementing the element count
                item_count -= 1
                ele += 1
                each_item -= 1
        #if a even distribution of weights is not possible
        else:
            #adding items to the containers linearly
            if j < containers - 1:
                ideal_container_list[j].append(weight_list[ele])
                ele += 1
        #if we'e reached the last container and we still have items remaining to add to container
        if j == containers - 1 and (items - ele) > 0:
            #iterate till the number of remaining items
            for i in range(0,items - ele):
                #list to store the sum of weights
                summ = []
                #setting min value to a large number
                min_sum = 9999
                #initialising minimum index with zero
                min_index=0
                #iterating till the length of containers
                for i in range(0,len(ideal_container_list)):
                    #calculating the sum of weights of container and adding the current item weight in it as well 
                    summ.append(sum(ideal_container_list[i]) + weight_list[item_count])
                if ele <= item_count:
                    #iterating till the length of summ list containing sum of weights of containers
                    for i in range(0,len(summ)):
                        #if the weight sum at a particular index is less than the min_sum we swap the values
                        if summ[i] < min_sum:
                            min_sum = summ[i]
                            #storing index containing minimum sum
                            min_index = i
                    #adding the elements weight to the minimum sum index
                    ideal_container_list[min_index].append(weight_list[item_count])
                    #decrementing the count of remaining items
                    item_count -= 1

#function to caluclate fitness
def calculate_fitness(items,containers):
    #calling the function to find ideal setting
    find_ideal_setting(items,containers)
    #if the fitness value of our current solution is less than or equal to the fitness threshold value only then its a good distribution of weights across containers
    if compute_mean_weight_difference(container_list) <= compute_mean_weight_difference(ideal_container_list):
        print("Your containers have a good weight distribution")
        print("Your solution is :  ",container_list)
        print("Ideal solution is :  ",ideal_container_list)
    else:
        print("Weights are not smartly distributed across containers")
        print("Your solution is :  ",container_list)
        print("Ideal solution is :  ",ideal_container_list)
            

#calling the functions
items,containers,option = input_func()
create_initial_population(items,containers,option)
calculate_fitness(items,containers)

