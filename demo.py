import argparse
import datetime
import json
import os
import yaml
import shutil
import pandas as pd
import numpy as np

from models import model_select

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--dataset", type=str, default="cbench")
    parser.add_argument("-m", "--model", type=str, default="O0")
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

    # print(**cfg["model_args"])
    print(cfg)
    print(os.getcwd())
    # model = model_class(**cfg["model_args"])
    model = model_class()
    # model = model_class(cost_function_name='compile_size')
    # TODO 解决模型初始化报错问题

    with open(f'./data/{dataset}-program_list.json') as f:
        program_list = json.load(f)

    result_list = []

    for program_dict in program_list:
        result = model.run(program_dict)
        print(program_dict['program_name'], result)
        result_dict = program_dict
        result_dict['result'] = result
        result_list.append(result_dict)
        os.getcwd()
        # break

    os.chdir(original_path)
    result_df = pd.DataFrame(result_list)
    result_df.to_csv(path + '/result.csv', index=False)