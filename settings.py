import os
import utils

CONF_FILENAME = "conf.json"
BASE_PATH = os.path.join(os.getcwd(), CONF_FILENAME)

configs = utils.load_json(BASE_PATH)

DRIVER_PATH = configs["driverPath"]
SELECTOR = configs["selector"]
BROWSER = configs["browser"]
BROWSER_VERSION = configs["browserVersion"]
TASK_DIR = configs["taskDir"]
IS_TASK_SET = configs["taskSet"]
