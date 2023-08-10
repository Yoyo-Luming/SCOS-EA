from lib.cost_function import cost_function
import random


class GA:

    def __init__(self, opt_list, small_better=True, population_size=3, generations=500, mutation_rate=0.1,
                 cost_function_name='compile_size'):

        self.population_size = population_size
        self.generations = generations
        self.mutate_ratio = mutation_rate
        self.cost_function_name = cost_function_name
        self.opt_list = opt_list
        self.gene_length = len(opt_list)
        self.small_better = small_better
        self.base_result = 0

    def get_opt(self, individual):
        """根据01串获取编译序列"""
        compile_flag = ''
        for i in range(len(individual)):
            if individual[i] == '1':
                compile_flag += ' ' + self.opt_list[i]['compile_flag']
        return compile_flag.strip()

    def generate_individual(self):
        """生成一个个体（随机编译优化选项）"""
        individual = ''
        for _ in range(self.gene_length):
            bit = random.choice(["0", "1"])
            individual += bit
        return individual

    def fitness(self, individual, program_dict):
        """计算个体的适应度"""
        program_dict['compile_flag'] = self.get_opt(individual)
        cost = cost_function(self.cost_function_name, program_dict)
        if self.small_better:
            return 1 - cost / self.base_result
        else:
            return cost / self.base_result

    def mutate(self, individual):
        """对个体进行变异"""
        mutated_individual = list(individual)
        for i in range(self.gene_length):
            if random.random() < self.mutate_ratio:
                if mutated_individual[i] == '0':
                    mutated_individual[i] = '1'
                else:
                    mutated_individual[i] = '0'
        return ''.join(mutated_individual)

    def crossover(self, parent1, parent2):
        """进行交叉操作，生成两个新个体"""
        crossover_point = random.randint(1, self.gene_length - 1)
        child1 = parent1[:crossover_point] + parent2[crossover_point:]
        child2 = parent2[:crossover_point] + parent1[crossover_point:]
        return child1, child2

    def select_parents(self, population, program_dict):
        """选择两个父代个体，使用轮盘赌选择"""
        total_fitness = sum(self.fitness(individual, program_dict) for individual in population)
        selection_probs = [self.fitness(individual, program_dict) / total_fitness for individual in population]
        parent1 = random.choices(population, weights=selection_probs)[0]
        parent2 = random.choices(population, weights=selection_probs)[0]
        return parent1, parent2

    def run(self, program_dict):
        program_dict['compile_flag'] = '-O0'
        self.base_result = cost_function(self.cost_function_name, program_dict)

        # 初始化种群
        population = [self.generate_individual() for _ in range(self.population_size)]

        for _ in range(self.generations):
            new_population = []
            while len(new_population) < self.population_size:
                parent1, parent2 = self.select_parents(population, program_dict)
                child1, child2 = self.crossover(parent1, parent2)
                child1 = self.mutate(child1)
                child2 = self.mutate(child2)
                new_population.extend([child1, child2])

            population = new_population

        best_individual = max(population, key=self.fitness)
        best_result = cost_function(best_individual, program_dict)
        best_compile_flag = self.get_opt(best_individual)

        return {'best_result': best_result, 'compile_flag': best_compile_flag}
