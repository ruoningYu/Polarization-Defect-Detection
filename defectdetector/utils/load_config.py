import json


def save_config(config):
    save_path = "/config/FLIR_BFS_US_51S5P.json"

    with open(save_path, 'w') as f:
        json.dump(config, f)


def load_config(config: str = None):
    with open(config, 'r') as f:
        _config = json.load(f)

    return _config
