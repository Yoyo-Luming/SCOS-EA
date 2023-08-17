from lib.cost_function import cost_function
import random
import time
import numpy as np


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
        compile_flag = '-Os'
        for i in range(len(individual)):
            conflict_list = self.opt_list[i]['conflict_list']
            conflict_flag = False
            for fid in conflict_list:
                if int(individual[fid - 1]) == 1:
                    individual[i] = 0
                    conflict_flag = True
            if conflict_flag:
                continue
            cur_flag = self.opt_list[i]['compile_flag'][individual[i]]
            if cur_flag != '':
                compile_flag += ' ' + cur_flag

        return compile_flag

    # def check_conflict(self, individual):
    #     for i in range(len(individual)):
    #         conflict_list = self.opt_list[i]['conflict_list']
    #         conflict_flag = False
    #         for fid in conflict_list:
    #             if int(individual[fid - 1]) == 1:
    #                 individual[i] = 0
    #                 conflict_flag = True
    #         if conflict_flag:
    #             continue

    def generate_individual(self, program_dict):
        """生成一个个体（随机编译优化选项）"""
        value = []
        for _ in range(self.gene_length):
            bit = random.choice([0, 1])
            value.append(bit)
        individual = {'value': value, 'cost': self.get_cost(value, program_dict)}
        return individual

    def get_cost(self, value, program_dict):
        """计算个体的适应度"""
        program_dict['compile_flag'] = self.get_opt(value)
        cost = cost_function(self.cost_function_name, program_dict)

        return cost

        # if self.small_better:
        #     return - cost
        # else:
        #     return cost

    def mutate(self, individual, program_dict):
        """对个体进行变异"""
        # mutated_value = list(individual['value'])
        mutated_value = individual['value']
        for i in range(self.gene_length):
            if random.random() < self.mutate_ratio:
                if mutated_value[i] == 0:
                    mutated_value[i] = 1
                else:
                    mutated_value[i] = 0
        # mutated_value = ''.join(mutated_value)
        mutated_individual = {'value': mutated_value, 'cost': self.get_cost(mutated_value, program_dict)}
        return mutated_individual

    def crossover(self, parent1, parent2, program_dict):
        """进行交叉操作，生成两个新个体，然后变异"""
        crossover_point = random.randint(1, self.gene_length - 1)
        child1, child2 = {}, {}
        child1['value'] = parent1['value'][:crossover_point] + parent2['value'][crossover_point:]
        child2['value'] = parent2['value'][:crossover_point] + parent1['value'][crossover_point:]
        child1 = self.mutate(child1, program_dict)
        child2 = self.mutate(child2, program_dict)

        return child1, child2

    def crossover_pmx(self, parent1, parent2, program_dict):
        # crossover_point = random.randint(1, self.gene_length - 1)
        cxpoint1, cxpoint2 = np.random.randint(0, self.gene_length - 1, 2)
        if cxpoint1 >= cxpoint2:
            cxpoint1, cxpoint2 = cxpoint2, cxpoint1 + 1
        child1, child2 = {}, {}
        child1['value'] = parent1['value'][:cxpoint1] + parent2['value'][cxpoint1:cxpoint2] + parent1['value'][cxpoint2:]
        child2['value'] = parent2['value'][:cxpoint1] + parent1['value'][cxpoint1:cxpoint2] + parent2['value'][cxpoint2:]
        child1 = self.mutate(child1, program_dict)
        child2 = self.mutate(child2, program_dict)

        return child1, child2

    def select_parents(self, population):
        """选择两个父代个体，使用轮盘赌选择"""
        total_fitness = sum(individual['fitness'] for individual in population)
        selection_probs = [individual['fitness'] / total_fitness for individual in population]
        parent1 = random.choices(population, weights=selection_probs)[0]
        parent2 = random.choices(population, weights=selection_probs)[0]
        return parent1, parent2

    def run(self, program_dict):
        program_dict['compile_flag'] = '-O0'
        self.base_result = cost_function(self.cost_function_name, program_dict)

        best_result = -1
        best_compile_flag = ''
        result_list = []

        # 初始化种群
        population = [self.generate_individual(program_dict) for _ in range(self.population_size)]

        for _ in range(self.generations):
            start_time = time.time()
            min_cost = min(population, key=lambda x: x['cost'])['cost']
            max_cost = max(population, key=lambda x: x['cost'])['cost']
            for p in population:
                if self.small_better:
                    p['fitness'] = max_cost - p['cost'] + 1
                else:
                    p['fitness'] = p['cost'] - min_cost + 1

            new_population = []
            while len(new_population) < self.population_size:
                parent1, parent2 = self.select_parents(population)
                # child1, child2 = self.crossover(parent1, parent2, program_dict)
                child1, child2 = self.crossover_pmx(parent1, parent2, program_dict)

                new_population.extend([child1, child2])

            population = new_population

            if self.small_better:
                best_individual = min(population, key=lambda x: x['cost'])
            else:
                best_individual = max(population, key=lambda x: x['cost'])

            best_compile_flag = self.get_opt(best_individual['value'])
            program_dict['compile_flag'] = best_compile_flag
            best_result = cost_function(self.cost_function_name, program_dict)
            result_list.append({'best_result': best_result, 'value': best_individual['value'], 'generations': _})
            end_time = time.time()
            print(f'generation {_}, population_size {self.population_size}, run time {end_time - start_time} s, best result {best_result}')

        return {'best_result': best_result, 'compile_flag': best_compile_flag, 'result_list': result_list}
