import ck.kernel as ck
import json
import subprocess


def get_pro_list():
    # 执行命令
    command = 'ck list program'  # 要执行的命令
    output = subprocess.check_output(command, shell=True, universal_newlines=True)

    output = output.splitlines()
    programs = []
    id = 1

    for line in output:
        line = line.strip()
        if line.startswith("polybench-cpu") or line.startswith("cbench"):
            programs.append({'program': line.strip(), 'id': id, 'cmd_key': '', 'dataset_uoa': ''})
            id = id + 1
    # for p in programs:
    #     r = ck.access({'action': "compile",
    #                    'module_uoa': 'program',
    #                    'data_uoa': p,
    #                    'flags': '-Os',
    #                    # 'cmd_key': compiler_flags,
    #                    'out': 'con'})

    # if r['return']>0:
    #     ck.err(r)
    return programs


if __name__ == '__main__':
    programs = get_pro_list()
    with open('programs.json', 'w') as f:
        json.dump(programs, f)
