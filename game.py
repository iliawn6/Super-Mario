import random;
import matplotlib.pyplot as plt

class Game:
    def __init__(self, levels):
        # Get a list of strings as levels
        # Store level length to determine if a sequence of action passes all the steps

        self.levels = levels
        self.current_level_index = -1
        self.current_level_len = 0
    
    def load_next_level(self):
        self.current_level_index += 1
        self.current_level_len = len(self.levels[self.current_level_index])
    
    def get_score(self, actions):
        # Get an action sequence and determine the steps taken/score
        # Return a tuple, the first one indicates if these actions result in victory
        # and the second one shows the steps taken

        current_level = self.levels[self.current_level_index]
        steps = 0
        score = 0
        for i in range(self.current_level_len - 1):
            # TODO: Make some changes
            current_step = current_level[i]

            if (current_step == '_'):
                if i > 0:
                    if(actions[i - 1] == '1' or actions[i - 1] == '2'):
                        steps += 1
                        score += 0.5
                    else:
                        if(actions[i] == '1' and i == self.current_level_len - 1):
                            score += 1
                        steps += 1
                        score += 1    
                else:
                    steps += 1
                    score += 1        

            elif (current_step == 'G' and actions[i - 1] == '1' and actions[i - 2] == '0'):
                steps += 1
                score += 1        

            elif (current_step == 'G' and actions[i - 2] == '1'):
                steps += 1
                score += 3

            elif (current_step == 'L' and actions[i - 1] == '2' and actions[i - 2] == '0' ):
                steps += 1
                score += 1
            elif (current_step == 'M' and actions[i-1] != '1'):
                steps += 1
                score += 3


            else:
                break
        return (steps == self.current_level_len - 1, score)
    
    def bubbleSort(self, arr, arr2):

        n = len(arr)
        swapped = False
        for i in range(n-1):
            for j in range(0, n-i-1):
                if arr[j] > arr[j + 1]:
                    swapped = True
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
                    arr2[j], arr2[j + 1] = arr2[j + 1], arr2[j]
            
            if not swapped:
                return

    def average(self, list, n):
        tmp = 0
        for i in range(n):
            tmp = tmp + list[i]
        return tmp / n   

    def roulette_wheel(self, population, scores):
        sum = 0
        for i in range(200):
            sum = sum + scores[i]

        roulette = []
        roulette.append(scores[0] * 1.0 / sum)

        for i in range(199):
            tmp = roulette[i] + (scores[i + 1] * 1.0 / sum)
            roulette.append(tmp)

        res = []
        for i in range(100):
            rand = random.random()
            for j in range(500):
                if rand <= roulette[j]:
                    res.append(population[j])
                    break

        return res        

    
    def evolution(self):
        
        worst_val = []
        best_val = []
        avg = []

        #First population
        population = []
        for i in range(200):
            chromosome = ""
            for j in range(self.current_level_len):
                chromosome = chromosome + str(random.randint(0, 2))
            population.append(chromosome)
        
        #Evaluation    
        scores = []
        for i in range(len(population)):
            score = self.get_score(population[i])
            if score[0] == True:
                # calculate value
                scores.append(score[1] + 5)
            else:
                # calculate value
                scores.append(score[1])

        self.bubbleSort(scores, population)

        
        arg = self.average(scores, len(scores))
        avg.append(arg)

        epsilon = avg[0]
        
        #elimination decision
        for k in range(10):
            
            #if(epsilon < 1):
            #    break
            
            children = []
            #Selection
            selected = population[100:200]

            #selected = self.roulette_wheel(population, scores)

            #Crossover
            for i in range(100):
                n = len(selected[0])
                rand1 = random.randint(0,99)
                rand2 = random.randint(0,99)

                child1 = selected[rand1][0:int(n/2)] + selected[rand2][int(n/2):n]
                child2 = selected[rand2][0:int(n/2)] + selected[rand1][int(n/2):n]
                children.append(child1)
                children.append(child2)

                """    
                child1 = selected[rand1][0:int(n/3)] + selected[rand2][int(n/3):int(2 * n/3)] + selected[rand1][int(2 * n/3): n]
                children.append(child1)

                child2 = selected[rand2][0:int(n/3)] + selected[rand1][int(n/3):int(2 * n/3)] + selected[rand2][int(2 * n/3): n]
                children.append(child2)
                """

            #mutation
            for i in range(200):
                rand = random.random()
                if rand < 0.1:
                    n = len(children[i])
                    bound = random.randint(0, n - 1)
                    random_num = random.randint(0, 2)
                    #if bound != n - 1:
                        #children[i] = str(children[0:bound]) + str(random_num) + str(children[bound + 1: n])
                    new = list(children[i])
                    new[bound] = str(random_num)
                    children[i] = str(new)
                    #else:
                        #children[i] = str(children[0:bound]) + str(random_num)
                    #TODO make change on mutation method    


            #children's evaluation           
            children_scores = []
            for i in range(len(children)):
                score = self.get_score(children[i])
                if score[0] == True:
                    # calculate value
                    children_scores.append(score[1] + 5)
                else:
                    # calculate value
                    children_scores.append(score[1])

            #self.bubbleSort(children_scores, children)
            
            generation = children + population
            generation_scores = children_scores + scores

            self.bubbleSort(generation_scores, generation)
            population = generation[200:400]
            scores = generation_scores[200:400]
            
            #population = children
            #scores = children_scores

            best_val.append(scores[199])
            worst_val.append(scores[0])
            
            tmp = self.average(scores, 200)
            avg.append(tmp)
            #epsilon =abs(avg[i + 1] - avg[i])

        x = [1,2,3,4,5,6,7,8,9,10]
      

        figure, axis= plt.subplots(2, 2)
        axis[0, 0].plot(x, avg[1::])
        axis[0, 0].set_title("average value!")

        axis[0, 1].plot(x, best_val)
        axis[0, 1].set_title("best value!")

        axis[1, 0].plot(x, worst_val)
        axis[1, 0].set_title("worst value!")


        plt.show()

        

            




g = Game(["__M_____", "____G_____", "__G___L_", "__G__G_L___", "____G_ML__G_", 
          "____G_MLGL_G_", "_M_M_GM___LL__G__L__G_M__", "____G_G_MMM___L__L_G_____G___M_L__G__L_GM____L____"
          , "___M____MGM________M_M______M____L___G____M____L__G__GM__L____ML__G___G___L___G__G___M__L___G____M__",
           "_G___M_____LL_____G__G______L_____G____MM___G_G____LML____G___L____LMG___G___GML______G____L___MG___"])

g.load_next_level()
g.load_next_level()
g.load_next_level()
g.load_next_level()
g.load_next_level()
g.load_next_level()
g.load_next_level()
g.load_next_level()

g.evolution()

# This outputs (False, 4)
#print(g.get_score("0000000000"))

#for i in range(10):
#    g.load_next_level()
#    g.evolution()

