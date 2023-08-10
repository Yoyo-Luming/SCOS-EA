import subprocess
import json


def get_gcc_optimizations():
    try:
        result = subprocess.run(["gcc", "--help=optimizers"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        if result.returncode == 0:
            optimization_list = []
            flag_id = 1
            # print(result.stdout.split('\n'))
            for line in result.stdout.splitlines():

                line = line.strip()
                if line.startswith("-f"):
                    compile_flag = line.split(" ", 1)[0]
                    explanation = line.split(" ", 1)[1].strip()
                    if "=" in compile_flag:
                        if compile_flag == "-ffp-contract=":
                            optimization_list.append({'compile_flag': compile_flag + "off", 'explanation': explanation, 'flag_id': flag_id})
                            optimization_list.append({'compile_flag': compile_flag + "fast", 'explanation': explanation, 'flag_id': flag_id})
                            optimization_list.append({'compile_flag': compile_flag + "on", 'explanation': explanation, 'flag_id': flag_id})
                        elif compile_flag == "-fira-algorithm=":
                            optimization_list.append({'compile_flag': compile_flag + "CB", 'explanation': explanation, 'flag_id': flag_id})
                            optimization_list.append({'compile_flag': compile_flag + "priority", 'explanation': explanation, 'flag_id': flag_id})
                        elif compile_flag == "-fira-region=":
                            optimization_list.append({'compile_flag': compile_flag + "one", 'explanation': explanation, 'flag_id': flag_id})
                            optimization_list.append({'compile_flag': compile_flag + "all", 'explanation': explanation, 'flag_id': flag_id})
                            optimization_list.append({'compile_flag': compile_flag + "mixed", 'explanation': explanation, 'flag_id': flag_id})
                        elif compile_flag == "-flifetime-dse=":
                            optimization_list.append({'compile_flag': compile_flag + "0", 'explanation': explanation, 'flag_id': flag_id})
                            optimization_list.append({'compile_flag': compile_flag + "1", 'explanation': explanation, 'flag_id': flag_id})
                            optimization_list.append({'compile_flag': compile_flag + "2", 'explanation': explanation, 'flag_id': flag_id})
                        elif compile_flag == "-fpack-struct=<number>":
                            continue
                        elif compile_flag == "-freorder-blocks-algorithm=":
                            optimization_list.append({'compile_flag': compile_flag + "simple", 'explanation': explanation, 'flag_id': flag_id})
                            optimization_list.append({'compile_flag': compile_flag + "stc", 'explanation': explanation, 'flag_id': flag_id})
                        elif compile_flag == "-fsched-stalled-insns-dep=<number>":
                            continue
                        elif compile_flag == "-fsched-stalled-insns=<number>":
                            continue
                        elif compile_flag == "-fsimd-cost-models=":
                            optimization_list.append({'compile_flag': compile_flag + "dynamic", 'explanation': explanation, 'flag_id': flag_id})
                            optimization_list.append({'compile_flag': compile_flag + "cheap", 'explanation': explanation, 'flag_id': flag_id})
                            optimization_list.append({'compile_flag': compile_flag + "unlimited", 'explanation': explanation, 'flag_id': flag_id})
                        elif compile_flag == "-fstack-reuse=":
                            optimization_list.append({'compile_flag': compile_flag + "none", 'explanation': explanation, 'flag_id': flag_id})
                            optimization_list.append({'compile_flag': compile_flag + "named_vars", 'explanation': explanation, 'flag_id': flag_id})
                            optimization_list.append({'compile_flag': compile_flag + "all", 'explanation': explanation, 'flag_id': flag_id})
                        elif compile_flag == "-ftree-parallelize-loops=":
                            continue
                            # optimizations.append({'compile_flag': compile_flag + "disable", 'explanation': explanation, 'flag_id': flag_id})
                            # optimizations.append({'compile_flag': compile_flag + "basic", 'explanation': explanation, 'flag_id': flag_id})
                            # optimizations.append({'compile_flag': compile_flag + "interleave", 'explanation': explanation, 'flag_id': flag_id})
                            # optimizations.append({'compile_flag': compile_flag + "all", 'explanation': explanation, 'flag_id': flag_id})
                        elif compile_flag == "-fvect-cost-models=":
                            optimization_list.append({'compile_flag': compile_flag + "unlimited", 'explanation': explanation, 'flag_id': flag_id})
                            optimization_list.append({'compile_flag': compile_flag + "dynamic", 'explanation': explanation, 'flag_id': flag_id})
                            optimization_list.append({'compile_flag': compile_flag + "cheap", 'explanation': explanation, 'flag_id': flag_id})
                            # optimizations.append({'compile_flag': compile_flag + "very-cheap", 'explanation': explanation, 'flag_id': flag_id})
                        else:
                            continue
                    else:
                        if compile_flag == "-fnothrow-opt":
                            continue
                        if compile_flag == "-fassociative-math":
                            continue
                        if compile_flag == "-fhandle-exceptions":
                            continue
                        if compile_flag == "-fdelayed-branch":
                            continue
                        if compile_flag == "-frtti":
                            continue
                        if compile_flag == "-fsection-anchors":
                            continue
                        if compile_flag == "-fstrict-enums":
                            continue
                        if compile_flag == "-fno-threadsafe-statics":
                            continue
                        if compile_flag == "-fvar-tracking":
                            continue
                        if compile_flag == "-fvar-tracking-uninit":
                            continue
                        optimization_list.append({'compile_flag': compile_flag, 'explanation': explanation, 'flag_id': flag_id})
                    flag_id += 1
                elif not line.startswith("-") and len(optimization_list):
                    for i in optimization_list:
                        if i['flag_id'] == flag_id - 1:
                            i['explanation'] += line
            return optimization_list
        else:
            print(f"Error: {result.stderr}")
            return None

    except FileNotFoundError:
        print("Error: gcc not found. Please ensure GCC is installed and in the system PATH.")
        return None


if __name__ == '__main__':
    optimizations = get_gcc_optimizations()
    print(len(optimizations))
    if optimizations:
        print("GCC Optimizations:")
        for opt in optimizations:
            print(opt)
    with open('../data/optimization_list.json', 'w') as f:
        json.dump(optimizations, f)
