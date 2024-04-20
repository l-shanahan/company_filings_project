#this code extracts relevant parameters from the config file. It then loops over all files in the relevant directory and applies the functions in the
#utils file to create outputs for all the required information types specified in the config file and save them as JSON in the output folder.

import os
import json

from utils import info_to_result

with open('config.json', 'r') as config_file:
    config = json.load(config_file)

info_dict = config['info_dict']
data_directory = config['data_directory']
openai_key = config['openai_key']

filepath_list = []

for filename in os.listdir(data_directory):
    if filename.endswith('.html'):
        filepath = os.path.join(data_directory, filename)
        filepath_list.append(filepath)

info_to_result(filepath_list, info_dict, openai_key)