# import repository configuration file
import importlib
import os
import shutil

from conf import (BREAK_NAME, BREAK_TYPE, DEFAULT_PROJECT_NAME,  # noqa: F401
                  LONG_BREAK_DURATION, LONG_TOMATO_DURATION, PROJECT_EXTENSION,  # noqa: F401
                  PYTOMATO_CONFIG_FILE, PYTOMATO_PROJECTS_DIR,  # noqa: F401
                  SHORT_BREAK_DURATION, SHORT_TOMATO_DURATION, TOMATO_NAME,  # noqa: F401
                  TOMATO_TYPE)  # noqa: F401


def update_variables(module):
    global_vars = globals()
    for var in filter(lambda entry: "__" not in entry, dir(module)):
        global_vars[var] = getattr(module, var)


PYTOMATO_PROJECTS_DIR = os.path.expanduser(PYTOMATO_PROJECTS_DIR)

user_config_file = os.path.join(PYTOMATO_PROJECTS_DIR, PYTOMATO_CONFIG_FILE)

# check if user conf file exists
if not os.path.isfile(user_config_file):
    # rewrite the values of the variables above
    if not os.path.isdir(PYTOMATO_PROJECTS_DIR):
        os.mkdir(PYTOMATO_PROJECTS_DIR)
    # copy the conf.py file to user_config
    package_dir = os.path.dirname(__file__)
    package_config_file = os.path.join(package_dir, PYTOMATO_CONFIG_FILE)
    shutil.copyfile(package_config_file, user_config_file)

conf_module_name = os.path.splitext(PYTOMATO_CONFIG_FILE)[0]
user_config_module = importlib.import_module(conf_module_name, PYTOMATO_PROJECTS_DIR)
update_variables(user_config_module)

# expand it again because it might get overwritten from the user config
PYTOMATO_PROJECTS_DIR = os.path.expanduser(PYTOMATO_PROJECTS_DIR)
del update_variables, user_config_file, conf_module_name, user_config_module
