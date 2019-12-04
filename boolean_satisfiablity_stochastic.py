import random
import time
import os

TIME_EXCEED = False
TIME_END = time.time() + 300

class Node(object):
    def __init__(self, state, arr):
        self.state = state
        self.fitness = self.cal_fitness(arr)

    @classmethod
    def generate_gen(self):
        list = [0, 1]
        return random.choice(list)

    @classmethod
    def initial_state(self):
        global n
        self.state = [self.generate_gen() for _ in range(n)]
        return self.state

    @classmethod
    def neghbor_x(self, i):
        global n
        neighbor = []
        for j in range(n):
            if j == i:
                if self.state[j] == 0:
                    neighbor.append(1)
                else:
                    neighbor.append(0)
            else:
                neighbor.append(self.state[j])
        return neighbor

    def cal_fitness(self, arr):
        global k
        fit = 0
        i = 0
        while i < k:
            if arr[3 * i] < 0:
                arr[3 * i] = -1 * arr[3 * i]
                if int(self.state[arr[3 * i] - 1]) == 0:
                    a = 1
                else:
                    a = 0
            else:
                a = int(self.state[arr[3 * i] - 1])
            if arr[3 * i + 1] < 0:
                arr[3 * i + 1] = -1 * arr[3 * i + 1]
                if int(self.state[arr[3 * i + 1] - 1]) == 0:
                    b = 1
                else:
                    b = 0
            else:
                b = int(self.state[arr[3 * i + 1] - 1])
            if arr[3 * i + 2] < 0:
                arr[3 * i + 2] = -1 * arr[3 * i + 2]
                if int(self.state[arr[3 * i + 2] - 1]) == 0:
                    c = 1
                else:
                    c = 0
            else:
                c = int(self.state[arr[3 * i + 2] - 1])
            if a + b + c == 0:
                i += 1
            else:
                fit += 1
                i += 1
        return fit



def main(k, arr):
    generation = 1
    global n
    global TIME_END
    global TIME_EXCEED
    global START_TIME
    initial_state = Node.initial_state()
    initial_node = Node(initial_state, arr)
    found = False
    neighbors = []
    p = 0.6
    current = initial_node
    visited = None
    history = []
    sequential = 0
    while not found:
        neighbors = []
        random_choose = int.from_bytes(os.urandom(8), byteorder="big") / ((1 << 64) - 1)
        if current.fitness >= k:
            TIME_EXCEED = False
            break
        elif time.time() > TIME_END:
            TIME_EXCEED = True
            break
        for i in range(n):
            s = current.neghbor_x(i)
            neighbors.append(Node(s, arr))
        if random_choose > p:
            neighbors = sorted(neighbors, key=lambda x: x.fitness, reverse=True)
            if neighbors[0] == visited:
                sequential += 1
                if sequential > 5:
                    current = Node(Node.initial_state(arr), arr)
                    print("RANDOM RESTART")

            else:
                sequential = 0
                next_node = neighbors[0]
        else:
            sequential = 0
            rand = int(random.uniform(0, n))
            next_node = neighbors[rand]
        visited = current
        history.append(current)
        current = next_node
        if generation % 100 == 0:
            print("generation: {}\tString: {}\n fitness: {}".format(generation,current.state, current.fitness))
        generation += 1
    if TIME_EXCEED:
        history = sorted(history, key=lambda x: x.fitness, reverse=True)
        best_answer = history[0]
        print("***************\nTime Exceed\n best String: {}\n best String fitness:{}".format(best_answer.state, best_answer.fitness))
        print(len(history))
    else:
        print("***************\nTime: {} \n best String: {}\n best String fitness:{}".format(time.time() - START_TIME, current.state, current.fitness))


if __name__ == "__main__" :
    START_TIME = time.time()
    n, k = map(int, input().split())
    arr = []
    for i in range(k):
        a, b, c = map(int, input().split())
        arr.append(a)
        arr.append(b)
        arr.append(c)
    main(k, arr)