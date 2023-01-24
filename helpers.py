import os

from tqdm import tqdm

config_default_values = {"return_errors": False, "print_errors": True}


def param_list(exec_data):
    func = exec_data[0]
    chunk_id = exec_data[1]
    params = exec_data[2]
    config = exec_data[3]

    results = []
    errors = []
    for param in tqdm(params, desc=f"processing: - chunk_num[{str(chunk_id)}] pid[{str(os.getpid())}]"):
        try:
            results.append(func(param))
        except Exception as e:
            if config["print_errors"]:
                print(e)
            errors.append(e)
    return results, errors
