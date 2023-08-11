import ck.kernel as ck


def cost_function(name, program_dict):
    if name == 'compile_size':
        program = program_dict['program']
        compile_flag = program_dict['compile_flag']
        return compile_size(program, compile_flag)
    elif name == 'run_time':
        program = program_dict['program']
        compile_flag = program_dict['compile_flag']
        cmd_key = program_dict['cmd_key']
        data_uoa = program_dict['data_uoa']
        return run_time(program, compile_flag, cmd_key, data_uoa)
    else:
        print('Error cost function selection!')


def compile_size(program, compile_flag):
    compile_result = ck.access({'action': "compile",
                                'module_uoa': 'program',
                                'data_uoa': program,
                                'flags': compile_flag,
                                'out': 'con'})

    if compile_result['return'] > 0:
        ck.err(compile_result)

    return compile_result['characteristics']['obj_size']


def run_time(program, compile_flag, cmd_key, data_uoa):
    compile_result = ck.access({'action': "compile",
                                'module_uoa': 'program',
                                'data_uoa': program,
                                'flags': compile_flag,
                                'out': 'con'})
    if compile_result['return'] > 0:
        ck.err(compile_result)

    run_result = ck.access({'action': "run",
                            'module_uoa': 'program',
                            'data_uoa': program,
                            'cmd_key': cmd_key,
                            'dataset_uoa': data_uoa,
                            'out': 'con'})

    if run_result['return'] > 0:
        ck.err(run_result)

    return run_result['characteristics']['execution_time_kernel_0']
