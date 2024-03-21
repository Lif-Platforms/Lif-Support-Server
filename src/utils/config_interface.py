# ----------------------------------
# Title: Config Interface
# Description: Responsible for interfacing with the "config.yml".
# Author: Superior126
# Date: 11/22/23
# ----------------------------------

# Imports
from resources.config_template import default_config
import yaml
import os


# Handle configuration loading
def load_config():
    # Check if config.yml exists
    if not os.path.isfile('config.yml'):
        with open('config.yml', 'a') as file:
            file.close()
            
    with open("config.yml", "r") as config:
        contents = config.read()
        configurations = yaml.safe_load(contents)
        config.close()

    # Ensure the configurations are not None
    if configurations == None:
        configurations = {}

    if not os.path.isfile('access-control.yml'):
        with open("access-control.yml", 'x') as config:
            config.close()

    # Compare config with json data
    for option in default_config:
        if not option in configurations:
            configurations[option] = default_config[option]

    # Open config in write mode to write the updated config
    with open("config.yml", "w") as config:
        new_config = yaml.safe_dump(configurations)
        config.write(new_config)
        config.close()

    return configurations