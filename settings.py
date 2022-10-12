from enum import Enum
from selenium.webdriver.common.by import By
import os
import utils

CONF_FILENAME = "conf.json"
BASE_PATH = os.path.join(os.getcwd(), CONF_FILENAME)

configs = utils.load_json(BASE_PATH)

INSUFFICIENT_DATA = "Insuficientes datos para especificar la instrucción"

APP_GEOMETRY = "800x600"
DRIVER_PATH = configs["driverPath"]
DRIVER_PATH_KEY = "driverPath"
DOWNLOAD_PATH = configs["downloadPath"]
SELECTOR = configs["selector"]
BROWSER = configs["browser"]
BROWSER_VERSION = configs["browserVersion"]
TASK_DIR = configs["taskDir"]
IS_TASK_SET = configs["taskSet"]

DATE_FORMAT = "yyyy-mm-dd hh:mm:ss"
LOGS_FILE = "logs.txt"
SCRIPT_PATH = "script.py"
ENCODING = "utf-8"
SLEEPY_TIME = 1000 * 10

CHROME = "chrome"


SELENIUM_TYPE_CLICK = 'Clickear'
SELENIUM_TYPE_FILL = 'Llenar'
SELENIUM_TYPE_SELECT = 'Seleccionar'

SELENIUM_TYPE_LIST = [
    SELENIUM_TYPE_CLICK,
    SELENIUM_TYPE_FILL,
    SELENIUM_TYPE_SELECT
]

BY_ID = 'HTML id: <tag id=$id></tag>'
BY_NAME = 'HTML name: <tag name=$name></tag>'
BY_TAG_NAME = 'HTML tag: <$tag></$tag>'
BY_CLASS_NAME = "HTML class: <tag class=$class></tag>"
BY_XPATH = "xpath"
BY_LINK_TEXT = 'El texto de un link HTML: <a href=...> $texto</a>'
BY_PARTIAL_LINK_TEXT = ('Texto en un link HTML: <a href=...>'
                        ' The quick $texto fox jumps...</a>')
BY_CSS_SELECTOR = "Selector CSS"

SELENIUM_BY = {
    BY_ID: By.ID,
    BY_XPATH: By.XPATH,
    BY_LINK_TEXT: By.LINK_TEXT,
    BY_PARTIAL_LINK_TEXT: By.PARTIAL_LINK_TEXT,
    BY_NAME: By.NAME,
    BY_TAG_NAME: By.TAG_NAME,
    BY_CLASS_NAME: By.CLASS_NAME,
    BY_CSS_SELECTOR: By.CSS_SELECTOR,
}

BY_LIST = [
    BY_ID,
    BY_NAME,
    BY_TAG_NAME,
    BY_CLASS_NAME,
    BY_XPATH,
    BY_LINK_TEXT,
    BY_PARTIAL_LINK_TEXT,
    BY_CSS_SELECTOR
]
SELECTION_HMTL_TEXT = 'Texto de opción: <option> $texto$ </option>'
SELECTION_HTML_VALUE = ('Valor de opción: <option value='
                        '"$valor$"> texto </option>')

SELECTION_HTML_LIST = [
    SELECTION_HMTL_TEXT,
    SELECTION_HTML_VALUE
]

TTK_SEPARATOR_PADDING_Y = 10


class Seleniums(Enum):
    @classmethod
    def human_text(cls, val) -> str:
        raise NotImplementedError("This method should be overriden.")


class SeleniumType(Seleniums):
    CLICK = 'Clickear'
    FILL = 'Llenar'
    SELECT = 'Seleccionar'

    @classmethod
    def human_text(cls, val) -> str:
        return {cls.CLICK: 'Clickear',
                cls.FILL: 'Llenar',
                cls.SELECT: 'Seleccionar'}[val]


SELENIUM_TYPES = [elem.value for elem in SeleniumType]


class SeleniumBy(Seleniums):
    ID = By.ID
    NAME = By.NAME
    TAG_NAME = By.TAG_NAME
    CLASS_NAME = By.CLASS_NAME
    XPATH = By.XPATH
    LINK_TEXT = By.LINK_TEXT
    PARTIAL_LINK_TEXT = By.PARTIAL_LINK_TEXT
    CSS_SELECTOR = By.CSS_SELECTOR

    @classmethod
    def human_text(cls, val):
        return {cls.ID: "id attribute",
                cls.NAME: "name attribute",
                cls.TAG_NAME: "html tag",
                cls.CLASS_NAME: "class name",
                cls.XPATH: "xpath",
                cls.LINK_TEXT: "texto DE un link",
                cls.PARTIAL_LINK_TEXT: "texto EN un link",
                cls.CSS_SELECTOR: "selector CSS"}[val]

    @classmethod
    def from_suggestion(cls, val: str) -> str:
        return {
            BY_ID: cls.ID,
            BY_NAME: cls.NAME,
            BY_TAG_NAME: cls.TAG_NAME,
            BY_CLASS_NAME: cls.CLASS_NAME,
            BY_XPATH: cls.XPATH,
            BY_LINK_TEXT: cls.LINK_TEXT,
            BY_PARTIAL_LINK_TEXT: cls.PARTIAL_LINK_TEXT,
            BY_CSS_SELECTOR: cls.CSS_SELECTOR
        }[val]


for e in SeleniumBy:
    print(e)


class SeleniumSelectionType(Seleniums):
    TEXT = 'Text'
    VALUE = 'Value'

    @classmethod
    def human_text(cls, val) -> str:
        return {
            cls.TEXT: "texto de un <option></option>",
            cls.VALUE: "valor (value attribute) de un <option></option>"
        }[val]


def save_setting(key: str, value=None) -> None:
    configs = utils.load_json(BASE_PATH)
    configs[key] = value
    utils.save_json(configs, BASE_PATH)
