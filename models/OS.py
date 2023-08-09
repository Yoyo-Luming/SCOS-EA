from lib.cost_function import cost_function


class OS:

    def __init__(self, cost_function_name='compile_size'):
        # self.program_dict = program_dict
        self.cost_function_name = cost_function_name
        self.compile_flag = '-Os'

    def run(self, program_dict):
        program_dict['compile_flag'] = self.compile_flag
        result = cost_function(self.cost_function_name, program_dict)
        return result
