import subprocess
import json


def get_gcc_optimizations():
    try:
        result = subprocess.run(["gcc", "--help=optimizers"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        if result.returncode == 0:
            optimizations = []
            id = 0
            # print(result.stdout.split('\n'))
            for line in result.stdout.splitlines():

                line = line.strip()
                if line.startswith("-f"):
                    flag = line.split(" ", 1)[0]
                    explanation = line.split(" ", 1)[1].strip()
                    if "=" in flag:
                        if flag == "-ffp-contract=":
                            optimizations.append({'flag': flag + "off", 'explanation': explanation, 'id': id})
                            optimizations.append({'flag': flag + "fast", 'explanation': explanation, 'id': id})
                            optimizations.append({'flag': flag + "on", 'explanation': explanation, 'id': id})
                        elif flag == "-fira-algorithm=":
                            optimizations.append({'flag': flag + "CB", 'explanation': explanation, 'id': id})
                            optimizations.append({'flag': flag + "priority", 'explanation': explanation, 'id': id})
                        elif flag == "-fira-region=":
                            optimizations.append({'flag': flag + "one", 'explanation': explanation, 'id': id})
                            optimizations.append({'flag': flag + "all", 'explanation': explanation, 'id': id})
                            optimizations.append({'flag': flag + "mixed", 'explanation': explanation, 'id': id})
                        elif flag == "-flifetime-dse=":
                            optimizations.append({'flag': flag + "0", 'explanation': explanation, 'id': id})
                            optimizations.append({'flag': flag + "1", 'explanation': explanation, 'id': id})
                            optimizations.append({'flag': flag + "2", 'explanation': explanation, 'id': id})
                        elif flag == "-fpack-struct=<number>":
                            continue
                        elif flag == "-freorder-blocks-algorithm=":
                            optimizations.append({'flag': flag + "simple", 'explanation': explanation, 'id': id})
                            optimizations.append({'flag': flag + "stc", 'explanation': explanation, 'id': id})
                        elif flag == "-fsched-stalled-insns-dep=<number>":
                            continue
                        elif flag == "-fsched-stalled-insns=<number>":
                            continue
                        elif flag == "-fsimd-cost-model=":
                            optimizations.append({'flag': flag + "dynamic", 'explanation': explanation, 'id': id})
                            optimizations.append({'flag': flag + "cheap", 'explanation': explanation, 'id': id})
                            optimizations.append({'flag': flag + "unlimited", 'explanation': explanation, 'id': id})
                        elif flag == "-fstack-reuse=":
                            optimizations.append({'flag': flag + "none", 'explanation': explanation, 'id': id})
                            optimizations.append({'flag': flag + "named_vars", 'explanation': explanation, 'id': id})
                            optimizations.append({'flag': flag + "all", 'explanation': explanation, 'id': id})
                        elif flag == "-ftree-parallelize-loops=":
                            continue
                            # optimizations.append({'flag': flag + "disable", 'explanation': explanation, 'id': id})
                            # optimizations.append({'flag': flag + "basic", 'explanation': explanation, 'id': id})
                            # optimizations.append({'flag': flag + "interleave", 'explanation': explanation, 'id': id})
                            # optimizations.append({'flag': flag + "all", 'explanation': explanation, 'id': id})
                        elif flag == "-fvect-cost-model=":
                            optimizations.append({'flag': flag + "unlimited", 'explanation': explanation, 'id': id})
                            optimizations.append({'flag': flag + "dynamic", 'explanation': explanation, 'id': id})
                            optimizations.append({'flag': flag + "cheap", 'explanation': explanation, 'id': id})
                            # optimizations.append({'flag': flag + "very-cheap", 'explanation': explanation, 'id': id})
                        else:
                            continue
                    else:
                        if flag == "-fnothrow-opt":
                            continue
                        if flag == "-fassociative-math":
                            continue
                        if flag == "-fhandle-exceptions":
                            continue
                        if flag == "-fdelayed-branch":
                            continue
                        if flag == "-frtti":
                            continue
                        if flag == "-fsection-anchors":
                            continue
                        if flag == "-fstrict-enums":
                            continue
                        if flag == "-fno-threadsafe-statics":
                            continue
                        if flag == "-fvar-tracking":
                            continue
                        if flag == "-fvar-tracking-uninit":
                            continue
                        optimizations.append({'flag': flag, 'explanation': explanation, 'id': id})
                    id += 1
                elif not line.startswith("-") and len(optimizations):
                    for i in optimizations:
                        if i['id'] == id - 1:
                            i['explanation'] += line
            return optimizations
        else:
            print(f"Error: {result.stderr}")
            return None

    except FileNotFoundError:
        print("Error: gcc not found. Please ensure GCC is installed and in the system PATH.")
        return None


if __name__ == '__main__':
    optimizations = get_gcc_optimizations()
    print(len(optimizations))
    id = 0
    if optimizations:
        print("GCC Optimizations:")
        for opt in optimizations:
            opt['id'] = id
            id += 1
            print(opt)
    with open('optimizations.json', 'w') as f:
        json.dump(optimizations, f)
