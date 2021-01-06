import time
import random
import sys
import yaml
import os
import json

def touch(filename):
    with open(filename, 'w'):
        pass

dct = yaml.load(open(os.getenv('USER_INPUT'), 'r'))
SELF = json.load(open(os.getenv('SELF')))['name']
for org, details in dct['ServiceProviders'][SELF]['Organizations'].items():
    sleep_time = random.randint(0, 30)
    print 'Onboarding Organization', org
    touch('/root/JFM-Testing/testing/artefacts/Organizations/%s.json'%org)
    time.sleep(sleep_time)
