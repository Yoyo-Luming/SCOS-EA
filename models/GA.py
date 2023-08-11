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

    def get_opt(self, individual):
        """根据01串获取编译序列"""
        compile_flag = ''
        for i in range(len(individual)):
            if individual[i] == '1':
                compile_flag += ' ' + self.opt_list[i]['compile_flag']
        return compile_flag.strip()

    def generate_individual(self, program_dict):
        """生成一个个体（随机编译优化选项）"""
        value = ''
        for _ in range(self.gene_length):
            bit = random.choice(["0", "1"])
            value += bit
        individual = {'value': value, 'fitness': self.fitness(value, program_dict)}
        return individual

    def fitness(self, value, program_dict):
        """计算个体的适应度"""
        program_dict['compile_flag'] = self.get_opt(value)
        cost = cost_function(self.cost_function_name, program_dict)
        if self.small_better:
            return - cost
        else:
            return cost

    def mutate(self, individual, program_dict):
        """对个体进行变异"""
        mutated_value = list(individual['value'])
        for i in range(self.gene_length):
            if random.random() < self.mutate_ratio:
                if mutated_value[i] == '0':
                    mutated_value[i] = '1'
                else:
                    mutated_value[i] = '0'
        mutated_value = ''.join(mutated_value)
        mutated_individual = {'value': mutated_value, 'fitness': self.fitness(mutated_value, program_dict)}
        return mutated_individual

    def crossover(self, parent1, parent2, program_dict):
        """进行交叉操作，生成两个新个体"""
        crossover_point = random.randint(1, self.gene_length - 1)
        child1, child2 = {}, {}
        child1['value'] = parent1['value'][:crossover_point] + parent2['value'][crossover_point:]
        child2['value'] = parent2['value'][:crossover_point] + parent1['value'][crossover_point:]
        child1['fitness'] = self.fitness(child1['value'], program_dict)
        child2['fitness'] = self.fitness(child1['value'], program_dict)
        return child1, child2

    def select_parents(self, population):
        """选择两个父代个体，使用轮盘赌选择"""
        total_fitness = sum(individual['fitness'] for individual in population)
        selection_probs = [individual['fitness'] / total_fitness for individual in population]
        parent1 = random.choices(population, weights=selection_probs)[0]
        parent2 = random.choices(population, weights=selection_probs)[0]
        return parent1, parent2

    def run(self, program_dict):
        best_result = -1
        best_compile_flag = ''
        result_list = []

        # 初始化种群
        population = [self.generate_individual(program_dict) for _ in range(self.population_size)]

        for _ in range(self.generations):
            new_population = []
            while len(new_population) < self.population_size:
                parent1, parent2 = self.select_parents(population)
                child1, child2 = self.crossover(parent1, parent2, program_dict)
                child1 = self.mutate(child1, program_dict)
                child2 = self.mutate(child2, program_dict)
                new_population.extend([child1, child2])

            population = new_population

            best_individual = max(population, key=lambda x: x['fitness'])

            best_compile_flag = self.get_opt(best_individual['value'])
            program_dict['compile_flag'] = best_compile_flag
            best_result = cost_function(self.cost_function_name, program_dict)
            result_list.append({'best_result': best_result, 'value': best_individual['value'], 'generations': _})

        return {'best_result': best_result, 'compile_flag': best_compile_flag,'result_list': result_list}
