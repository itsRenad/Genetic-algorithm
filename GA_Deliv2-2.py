import random
import copy
import matplotlib.pyplot as plt

Scontainer = "container"
Sitem = "item"

class CargoLoading:
    #Add the items to the containers
    def Add_Item(self, container, item, opt, Chromo):
        #if the user selects option A
        if opt == "A":
            weight = item / 2
        # if the user selects option B
        elif opt == "B":
            weight = (item ** 2) / 2
        Chromo[container].append((Sitem + str(item), weight))
    
    def Find_Weight_Diff_Each_Population(self, pop):
        #list to store the sum of weights in each container
        sum_weights = []
        #iterating over the dictionary containing container and weights and calculating the sum of weights in each container
        for _, value in pop.items():
            summ = 0
            #as we have (item,weight) tuple 
            for (_,weight) in value:
                #adding up weights in each container
                summ += weight
            #adding summed weights to list
            sum_weights.append(summ)
        max_weight = max(sum_weights)
        min_weight = min(sum_weights)
        return max_weight - min_weight
    
    """creates n number of random populations"""
    def Create_nRandom_Populations(self,num,items, containers, option):
        Population = []
        while num > 0:
            Population.append(self.Create_Random_Population(items, containers, option))
            num -= 1
        return Population
    
    """creates a random chromosome, which is randomly adds items to the containers"""
    def Create_Random_Population(self, items, containers, option):
        Chromosome={}
        for i in range(1, containers + 1):
            # Perparing the containers name to be as  container1,container2...
            ContainerName = Scontainer + str(i)
            Chromosome[ContainerName] = []
        # Store the number of the items
        i = items
        while i > 0:
            # To distribute the items randomly generate a value between 1 and 2
            prob = random.randint(1, 2)
            d = list(Chromosome)
            if prob > 1:
                # Chose a container in even index
                rand = random.randrange(0, containers, 2)
                # Add the item to the even container
                self.Add_Item(d[rand], i, option, Chromosome)
            # if prob value is greater than 1
            else:
                # Chose a container in odd index
                rand = random.randrange(1, containers, 2)
                # Add the item to the odd container
                self.Add_Item(d[rand], i, option, Chromosome)
            i -= 1
        return Chromosome
    
    """calculates fitness of a given chromosome"""
    def Calculate_Fitness(self,chromosome):
        fit = self.Find_Weight_Diff_Each_Population(chromosome)
        return fit
    
    """calculates fitness of all the chromosomes in the population"""
    def Get_All_Fitness(self,pop):
        fitness = []
        for chrom in pop:
            fitness.append(self.Calculate_Fitness(chrom))
        return fitness
    
    def Single_Point_Crossover(self,randPopA, randPopB):
        """this function performs the single point cross over at a random selected point within the categories."""
        point = random.randint(1, len(randPopA)-1)
        i = 0
        aa = []
        bb = []
        l1 = list(randPopA.items())
        l2 = list(randPopB.items())
        while i != point:
            aa.append(l1[i])
            bb.append(l2[i])
            i += 1
        while i < len(randPopA):
            aa.append(l2[i])
            bb.append(l1[i])
            i += 1
        aa = dict(aa)
        bb = dict(bb)
        return aa, bb
    
    def Mutate(self,pop, randPopA, PhenotypeMutationRate):
        '''This function performs mutation on the population. The initial mutation rate is first selected that 
        is the phenotype mutation rate. 
        then a genotype mutation rate is selected. if that G_mutation rate is less than P_mutation rate, then the 
        genotype gets swapped. '''
        pop1 = list(randPopA.items())
        pop2 = list(pop.items())
        i=random.randint(0,len(randPopA)-1)
        GenemutationR = random.uniform(0, 1)
        if GenemutationR < PhenotypeMutationRate:
            pop1[i] = pop2[i]
        return dict(pop1)
    
    """creates a random population and mutates the given population with the random population"""
    def Perform_Mutation(self,randPopA, randPopB, items,containers):
        rand = random.uniform(0,1)
        randomPoP = None
        #creating a random population to mutate the population with. 
        if rand > 0.5:
            randomPoP = self.Create_Random_Population(items, containers,"A")
        else:
            randomPoP = self.Create_Random_Population(items, containers,"B")
        #mutating both of the population
        randPopA = self.Mutate(randomPoP, randPopA, random.uniform(0, 1))
        randPopB = self.Mutate(randomPoP, randPopB, random.uniform(0, 1))
        return randPopA, randPopB
    
    def Roulette_Wheel_Selection(self,Population):
        ''' This Function randomly selects two individual population from the entire population
        and returns them. this technique is known as roulette wheel'''
        index1 = random.randint(0, len(Population)-1 )
        index2 = random.randint(0, len(Population)-1 )
        #just to make sure that both random individuals are not the same population
        while index2 == index1:
            index2 = random.randint(0, len(Population)-1 )
        return Population[index1], Population[index2]
    
    """This function is used to add the newly created random chromosomes to the population
        This function works in a way that it first adds the chromosomes and their fitness values to the 
        population and fitness. It then sorts them in ascending order of fitness value and 
        removes the last 2 chromosomes from population,the two worst chromosome having the maximum weight differences
        are removed"""
    def Add_Back_To_Population(self,fitA, randPopA, fitB, randPopB, fitness,Population):
        fitness.append(fitA)
        fitness.append(fitB)
        Population.append(randPopA)
        Population.append(randPopB)
        for i in range(0,len(fitness)):
            for j in range(0,len(fitness)-i-1):
                if fitness[j] > fitness[j+1]:
                    temp = fitness[j]
                    temp1 = Population[j]
                    fitness[j] = fitness[j+1]
                    Population[j] = Population[j+1]
                    fitness[j+1] = temp
                    Population[j+1] = temp1
        for i in range(0,2):
            fitness.pop()
            Population.pop()
        return fitness,Population
    """function to get input from the user"""
    def Get_Input(self):
        containers = int(input("Please enter the number of containers:  "))
        items = int(input("Please enter the number of items in containers:  "))
        option = str(input("Choose A if you want item`s weight to be as i/2 OR choose B if you want item weight as (i^2)/2: "))
        num = int(input("Enter the number of random populations to want to create: "))
        condition = int(input("Enter 1 for Crossover and 2 for No-Crossover: "))
        times = int(input("Enter the number of times you wish to perform mutation: "))
        return containers,items,option,num,times,condition
    
    """working of genetic algorithm"""
    def Genetic_Algorithm(self,trials,containers,items,fitness,pop,times,condition):
        #stores the best overall fitness value
        bestOVERALL = [float('inf'), None]
        #if crossover is to be applied
        if condition == "Crossover":
            while trials > 0:
                #selects to best chromosomes
                randPopA,randPopB = self.Roulette_Wheel_Selection(pop)
                randPopA, randPopB = self.Single_Point_Crossover(randPopA, randPopB)#crosover
                #applies mutation as per the mutation operator
                while times > 0:
                    randPopA, randPopB = self.Perform_Mutation(randPopA, randPopB,items,containers)#mutation
                    times -= 1
                #calculates fitness values
                fitA = self.Calculate_Fitness(randPopA)
                fitB = self.Calculate_Fitness(randPopB)
                #adding the chromosomes back to population
                fitness,pop = self.Add_Back_To_Population(fitA, randPopA, fitB, randPopB, fitness,pop)
                #updating the result
                if fitA < bestOVERALL[0]:
                    bestOVERALL = (fitA, randPopA)
                if fitB < bestOVERALL[0]:
                    bestOVERALL = (fitB, randPopB)
                trials -= 1
            return bestOVERALL[0]
        #if no crossover is to be applied
        else:
            while trials > 0:
                #selects to best chromosomes
                randPopA,randPopB,fitness = self.Ellitist_Wheel_Selection(fitness,pop) 
                #applies mutation as per the mutation operator
                while times > 0:
                    randPopA, randPopB = self.Perform_Mutation(randPopA, randPopB,items,containers)#mutation
                    times -= 1
                #calculates fitness values
                fitA = self.Calculate_Fitness(randPopA)
                fitB = self.Calculate_Fitness(randPopB)
                #adding the chromosomes back to population
                fitness,pop = self.Add_Back_To_Population(fitA, randPopA, fitB, randPopB, fitness,pop)
                #updating the result
                if fitA < bestOVERALL[0]:
                    bestOVERALL = (fitA, randPopA)
                if fitB < bestOVERALL[0]:
                    bestOVERALL = (fitB, randPopB)
                trials -= 1
            return bestOVERALL[0]

"""This fuction is used to run a given experiment for k trials"""
def Experimentation_Instance(pop_size,mutation_k,condition,instance):
    #if experiment for instance 1 is to be done
    if instance == 1:
        containers,items,option = 10,200,"A"
    #if experiment for instance 2 is to be done
    else:
        containers,items,option = 100,200,"B"
    all_fitness = []
    #generation values
    exp_trials = [1000,2000,3000,4000,5000,6000,7000,8000,9000,10000]
    SCL = CargoLoading() 
    #doing for 8 trials
    counter = 8
    while counter > 0:
        exp_fitness=[]
        for i in range(0,len(exp_trials)):
            pop = SCL.Create_nRandom_Populations(pop_size,items,containers,option)
            fitness = SCL.Get_All_Fitness(pop)
            res = SCL.Genetic_Algorithm(exp_trials[i],containers,items,fitness,pop,mutation_k,condition)
            exp_fitness.append(res)
        counter -= 1
        all_fitness.append(exp_fitness)
    return all_fitness

"""function to perform all 6 experiments for a given instance"""
def Result_Experimentation_Instance(instance):
    #creating a dictionary to store results for each expeiment
    all_results_instance = {}
    for i in range(1,7):
        key = "exp"+str(i)
        all_results_instance[key] = []
    #experiment1
    exp1_fitness = Experimentation_Instance(10,1,"Crossover",instance)
    all_results_instance["exp1"].append(exp1_fitness) 
    #experiment2
    exp2_fitness = Experimentation_Instance(100,1,"Crossover",instance)
    all_results_instance["exp2"].append(exp2_fitness) 
    #experiment3
    exp3_fitness = Experimentation_Instance(10,5,"Crossover",instance)
    all_results_instance["exp3"].append(exp3_fitness) 
    #experiment4
    exp4_fitness = Experimentation_Instance(100,5,"Crossover",instance)
    all_results_instance["exp4"].append(exp4_fitness) 
    #experiment5
    exp5_fitness = Experimentation_Instance(10,5,"None",instance)
    all_results_instance["exp5"].append(exp5_fitness) 
    #experiment6
    exp6_fitness = Experimentation_Instance(10,0,"Crossover",instance)
    all_results_instance["exp6"].append(exp6_fitness) 
    return all_results_instance

"""function to plot graphs for all trials of each experiment"""
def Plot_Graphs(result):
    for count in range(0,len(result)):
        t = "Graphs for Experiment" + str(count+1)
        print(t)
        key = "exp" + str(count+1)
        for i in range(0,len(result.get(key)[0])):
            exp_trials = [1000,2000,3000,4000,5000,6000,7000,8000,9000,10000]
            plt.plot(exp_trials, result.get(key)[0][i], color='red', marker='o')
            title = "Plot for trial " + str(i+1)
            plt.title(title, fontsize=14)
            plt.xlabel('Generation', fontsize=14)
            plt.ylabel('Fitness', fontsize=14)
            plt.grid(True)
            plt.show()

"""function to get the best fitness value for each trial of each experiment"""
def Get_Best_Fitness(result,):
    exp_trials = [1000,2000,3000,4000,5000,6000,7000,8000,9000,10000]
    for count in range(0,len(result)):
        key = "exp" + str(count+1)
        print("Experiment ",count+1)
        for i in range(0,len(result.get(key)[0])):
            min_val = min(result.get(key)[0][i])
            min_index = result.get(key)[0][i].index(min_val)
            gen = exp_trials[min_index]
            print("Best Fitness for trial",i+1,"is: ",min_val,"for Generation",gen)
        print()

"""IF YOU WANT USER DEFINED INPUT"""
def call_algo():
    all_fitness = []
    #generation values
    exp_trials = [1000,2000,3000,4000,5000,6000,7000,8000,9000,10000]
    SCL = CargoLoading() 
    containers,items,option,pop_size,mutation_k,cond = SCL.Get_Input()
    if cond == 1:
        condition = "Crossover"
    elif cond == 2:
        condition == "None"
    #doing for 8 trials
    counter = 8
    while counter > 0:
        exp_fitness=[]
        for i in range(0,len(exp_trials)):
            pop = SCL.Create_nRandom_Populations(pop_size,items,containers,option)
            fitness = SCL.Get_All_Fitness(pop)
            res = SCL.Genetic_Algorithm(exp_trials[i],containers,items,fitness,pop,mutation_k,condition)
            exp_fitness.append(res)
        counter -= 1
        all_fitness.append(exp_fitness)
    return all_fitness

def Plot_Graphs_UserDefined(result):
    for i in range(0,len(result)):
        exp_trials = [1000,2000,3000,4000,5000,6000,7000,8000,9000,10000]
        plt.plot(exp_trials, result[i], color='red', marker='o')
        title = "Plot for trial " + str(i+1)
        plt.title(title, fontsize=14)
        plt.xlabel('Generation', fontsize=14)
        plt.ylabel('Fitness', fontsize=14)
        plt.grid(True)
        plt.show()

print("Plotting results for Instance 1")
print()
instance1_results = Result_Experimentation_Instance(1)
Plot_Graphs(instance1_results)
print()
print("---------------------------------------------------------------------------------")
print()
print("Plotting results for Instance 2")
print()
instance2_results = Result_Experimentation_Instance(2)
Plot_Graphs(instance2_results)

print("Best Fitness values for Instance 1")
print()
Get_Best_Fitness(instance1_results)
print()
print()
print("Best Fitness values for Instance 2")
print()
Get_Best_Fitness(instance2_results)

"""for user defined"""
res = call_algo()
Plot_Graphs_UserDefined(res)