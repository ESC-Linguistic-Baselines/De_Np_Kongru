import yaml
import os

expanded_path = os.path.expanduser("~/repo/Python/De_NP_Kongru/config.yaml")

def get_config_data():
    with open (expanded_path) as config_file:
        config = yaml.safe_load(config_file)
    return config