import argparse
import datetime
import json
import os
import yaml
import shutil
import pandas as pd

from models import model_select

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--dataset", type=str, default="cbench")
    parser.add_argument("-m", "--model", type=str, default="AGENTGA")
    args = parser.parse_args()

    dataset = args.dataset
    model_name = args.model.upper()
    model_class = model_select(model_name)

    now = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    original_path = os.getcwd()
    path = f"./save/{model_name}/{model_name}-{dataset}-{now}"
    if not os.path.exists(path):
        os.makedirs(path)

    with open(f"./configs/{model_name}.yaml", "r") as f:
        cfg = yaml.safe_load(f)
    cfg = cfg[dataset]

    shutil.copy2(f'./configs/{model_name}.yaml', path)
    shutil.copy2(f'./models/{model_name}.py', path)

    if cfg['use_opt']:
        with open(cfg['optimization_file']) as f:
            opt_list = json.load(f)
        cfg['model_args']['opt_list'] = opt_list

    model = model_class(**cfg["model_args"])

    with open(f'./data/{dataset}-program_list.json') as f:
        program_list = json.load(f)

    result_list = []

    for i in range(2, 3):
        program_dict = program_list[i]
        if i > 0 and program_dict['program'] == program_list[i-1]['program']:
            continue
        result = model.run(program_dict)
        print(program_dict['program_name'], result)
        result_dict = program_dict
        result_dict['result'] = result
        result_list.append(result_dict)

        os.chdir(original_path)
        result_df = pd.DataFrame(result_list)
        result_df.to_csv(path + '/'+program_dict['program_name']+'-agent-result.csv', index=False)

    # os.chdir(original_path)
    # result_df = pd.DataFrame(result_list)
    # result_df.to_csv(path + '/result.csv', index=False)
