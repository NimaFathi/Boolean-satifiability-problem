import random
import time

TIMEEXCEPTION = True
POPULATION_SIZE = 500
T_end = time.time() + 550


class Individual(object):
    def __init__(self, chromosome, arr):
        self.chromosome = chromosome
        self.fitness = self.calculate_fitness(arr)

    @classmethod
    def mutated_genes(self):
        list = [0, 1]
        state = random.choice(list)
        return state

    @classmethod
    def create_chromosome(self):
        global n
        self.chromosome = [self.mutated_genes() for _ in range(0, n)]
        return self.chromosome

    def crossover(self, parent2):
        global n
        child1 = []
        child2 = []
        crossover_point = random.randint(1, n - 1)
        for i in range(crossover_point):
            child1.append(self.chromosome[i])
            child2.append(parent2.chromosome[i])
        for i in range(crossover_point, n):
            child1.append(parent2.chromosome[i])
            child2.append(self.chromosome[i])
        return Individual(child1, arr), Individual(child2, arr)

    def mutation(self):
        global n
        p = float(1/n)
        randnumber = random.uniform(0, 1)
        if randnumber < p:
            mutation_element = random.randint(1, n - 1)
            if self.chromosome[mutation_element] == 1:
                self.chromosome[mutation_element] = 0
            else:
                self.chromosome[mutation_element] = 1

    def calculate_fitness(self, arr):
        global k
        fit = 0
        i = 0
        while i < k:
            if (arr[3 * i] < 0):
                arr[3 * i] = -1 * arr[3 * i]
                if (int(self.chromosome[arr[3 * i] - 1]) == 0):
                    a = 1
                else:
                    a = 0
            else:
                a = int(self.chromosome[arr[3 * i] - 1])
            if (arr[3 * i + 1] < 0):
                arr[3 * i + 1] = -1 * arr[3 * i + 1]
                if (int(self.chromosome[arr[3 * i + 1] - 1]) == 0):
                    b = 1
                else:
                    b = 0
            else:
                b = int(self.chromosome[arr[3 * i + 1] - 1])
            if (arr[3 * i + 2] < 0):
                arr[3 * i + 2] = -1 * arr[3 * i + 2]
                if (int(self.chromosome[arr[3 * i + 2] - 1]) == 0):
                    c = 1
                else:
                    c = 0
            else:
                c = int(self.chromosome[arr[3 * i + 2] - 1])
            if (a + b + c == 0):
                i += 1
            else:
                fit += 1
                i += 1
        return fit


def main(k, arr):
    global TIMEEXCEPTION
    global POPULATION_SIZE
    global T_end
    maxbest = []
    generation = 1
    found = False
    population = []
    for _ in range(POPULATION_SIZE):
        gnome = Individual.create_chromosome()
        population.append(Individual(gnome, arr))
    while not found:
        if time.time() > T_end:
            print("Time Exceed")
            TIMEEXCEPTION = True
            break
        # population = sorted(population, key=lambda x: x.fitness, reverse=True)
        if population[0].fitness >= k:
            found = True
            TIMEEXCEPTION = False
            break
        selected = []
        new_generation = []
        sum_fitness = 0
        for i in range(POPULATION_SIZE):
            sum_fitness += population[i].fitness
        for i in range(POPULATION_SIZE):
            random_fit = random.randint(0, sum_fitness)
            summation = random_fit
            j = 0
            while summation <= sum_fitness:
                if j >= POPULATION_SIZE:
                    j = j % POPULATION_SIZE
                summation += population[j].fitness
                if (summation >= sum_fitness):
                    parent = population[j]
                    selected.append(parent)
                    break
                j += 1
        i = 0
        while i < POPULATION_SIZE:
            parent1 = selected[i]
            i += 1
            parent2 = selected[i]
            i += 1
            child1, child2 = parent1.crossover(parent2)
            child1.mutation()
            new_generation.append(child1)
            child2.mutation()
            new_generation.append(child2)
        population = new_generation
        population = sorted(population, key=lambda x: x.fitness, reverse=True)
        maxbest.append(population[0])
        if (generation % 10 == 0):
            print("Generation: {}\tString: {}\tFitness: {}, time from start: {}".
                  format(generation,
                         population[0].chromosome,
                         population[0].fitness, time.time() - start_time))
        generation += 1

    population = sorted(population, key=lambda x: x.fitness, reverse=True)
    maxbest.append(population[0])
    if TIMEEXCEPTION == True:
        maxbest = sorted(maxbest, key=lambda x: x.fitness, reverse=True)
        print("*******************\nTime exception\n best String: {} \n best Fitness {}".format(maxbest[0].chromosome,
                                                                                                maxbest[0].fitness))
    else:
        print("*******************\nGeneration: {}\nString: {}\nFitness: {} \t Execution {} S".
              format(generation,
                     population[0].chromosome,
                     population[0].fitness, time.time() - start_time))


if __name__ == '__main__':
    start_time = time.time()
    n, k = map(int, input().split())
    arr = []
    for i in range(k):
        a, b, c = map(int, input().split())
        arr.append(a)
        arr.append(b)
        arr.append(c)
    main(k, arr)
