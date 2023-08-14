from lib.cost_function import cost_function


class GREEDY:

    def __init__(self, opt_list, small_better=True, num_total=3, cost_function_name='compile_size'):
        self.num_total = num_total
        self.cost_function_name = cost_function_name
        self.opt_list = opt_list
        self.small_better = small_better

    def run(self, program_dict):
        program_dict['compile_flag'] = '-O0'
        best_result = cost_function(self.cost_function_name, program_dict)
        best_compile_flag = ''
        compile_flag_list = []

        for compile_dict in self.opt_list:
            cur_compile_flag = (best_compile_flag + ' ' + compile_dict['compile_flag'][1]).strip()
            program_dict['compile_flag'] = cur_compile_flag
            result = cost_function(self.cost_function_name, program_dict)
            if self.small_better:
                if result < best_result:
                    best_result = result
                    best_compile_flag = cur_compile_flag
                    compile_flag_list.append(compile_dict['flag_id'])
            else:
                if result > best_result:
                    best_result = result
                    best_compile_flag = cur_compile_flag
                    compile_flag_list.append(compile_dict['flag_id'])
            if len(compile_flag_list) >= self.num_total:
                break

        return {'best_result': best_result, 'compile_flag': best_compile_flag}
